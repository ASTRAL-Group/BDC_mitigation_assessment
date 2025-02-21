from .base import BaseClass
from peft import get_peft_config, get_peft_model
from transformers import set_seed, DataCollatorForLanguageModeling, Trainer, TrainingArguments, get_scheduler
import json
from loguru import logger
from sklearn.model_selection import train_test_split
import torch
from .preprocessing import DatasetProcessor
from .basic_model_loader import load_model, load_tokenizer
from .utils import get_max_length, log
from torch.optim import SGD

class Finetune(BaseClass):
    def __init__(self, preprocessor=DatasetProcessor(), config_file="../configs/config_finetune.json", **kwargs):
        """
        Initializes the Finetune class.

        Args:
            preprocessor (DatasetProcessor, optional): The preprocessor object to use for dataset processing. Defaults to DatasetProcessor().
            config_file (str, optional): The path to the configuration file. Defaults to "../configs/config_finetune.json".
            **kwargs: Additional keyword arguments to update the configuration.

        Attributes:
            config (dict): The configuration dictionary loaded from the config file.
            model (None): The model object (initialized as None).
            dtype (torch.dtype): The data type to use for tensors (initialized as torch.float32).
            deepspeed_config (dict): The DeepSpeed configuration dictionary (initialized as None if use_deepspeed is False).
            lora_config_peft (dict): The PEFT configuration dictionary generated from lora_config.

        """
        self.config = json.load(open(config_file, "r"))

        for kwarg in kwargs:
            self.config[kwarg] = kwargs[kwarg]

        self.__dict__.update(self.config)
        self.model = None

        self.dtype = torch.float32
        if self.fp16:
            self.dtype = torch.float16
        if self.bf16:
            self.dtype = torch.bfloat16

        if not self.use_deepspeed:
            deepspeed_config = None
            self.config["deepspeed_config_file"] = None
        else:
            deepspeed_config = json.load(open(self.deepspeed_config_file, "r"))

        self.config["model_name"] = None
        self.config["deepspeed_config"] = deepspeed_config
        super().__init__(**self.config, preprocessor=preprocessor)
        self.lora_config_peft = get_peft_config(self.lora_config)

    def load_model(self, model_name, model=None):
        """
        Loads a pre-trained model for contamination detection.

        Args:
            model_name (str): The name of the model to load.
            model (Optional[torch.nn.Module]): An optional pre-initialized model object.

        Returns:
            None
        """
        revision = 'main'
        # phi-2 kept updating the modeling file which made the code break several times, we therefore use a specific revision
        if model_name == 'microsoft/phi-2':
            revision = '39afec137e35c2bd2c67d939af6efae96198fd00'
        if model is not None:
            self.model = model
        else:
            log(logger.debug, f"Loading model for {model_name} with revision {revision}")
            self.model = load_model(model_name, dtype=self.dtype, revision=revision)

        if self.use_lora:
            self.model = get_peft_model(self.model, self.lora_config_peft)

    def finetune(self, model_name, dataset, data_collator=None, model=None, neptune_run=None, **kwargs):
        """
        Fine-tunes the model with the given dataset.

        Args:
            model_name (str): The name of the model to be fine-tuned.
            dataset (Dataset): The dataset used for fine-tuning.
            data_collator (DataCollator, optional): The data collator used for batching and preparing the data. Defaults to None.
            model (Model, optional): The pre-trained model to be fine-tuned. Defaults to None.
            neptune_run (NeptuneRun, optional): The Neptune run object for logging. Defaults to None.
            **kwargs: Additional keyword arguments.

        Returns:
            Model: The fine-tuned model.
        """
        log(logger.info, f"Finetuning model with {self} and dataset with size {len(dataset)}")
        self.model_name = model_name
        dataset = self.preprocessor.prepare_dataset(dataset, self.model_name, self.mask_inputs)
        set_seed(42)
        if not self.reload or self.model is None:
            log(logger.debug, "Loading model")
            self.load_model(model_name, model=model)
            
        tokenizer = load_tokenizer(model_name)
        self.model.config.pad_token_id = tokenizer.pad_token_id
        
        if data_collator is None:
            data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

        max_length = get_max_length(self.model.config, default_length=self.max_length_default)
        
        if len(dataset) > 1 and self.test_split_size > 0:
            log(logger.debug, "Splitting dataset")
            train_dataset, test_dataset = train_test_split(dataset, test_size=self.test_split_size, random_state=42)
        else:
            train_dataset = dataset
            test_dataset = None

        callbacks = []
        report_to = 'all' 
        if neptune_run is not None:
            report_to = 'none'
        training_args = TrainingArguments(
            output_dir=self.output_dir,                                       # output directory
            num_train_epochs=self.num_train_epochs,                           # total number of training epochs
            per_device_train_batch_size=self.per_device_train_batch_size,     # batch size per device during training
            per_device_eval_batch_size=self.per_device_eval_batch_size,       # batch size for evaluation
            warmup_ratio=self.warmup_ratio,                                   # number of warmup steps for learning rate scheduler
            weight_decay=self.weight_decay,                                   # strength of weight decay
            logging_dir=self.logging_dir,                                     # directory for storing logs
            logging_steps=self.logging_steps,
            learning_rate=self.learning_rate,
            save_steps=self.save_steps,
            deepspeed=self.deepspeed_config_file,
            save_total_limit=self.save_total_limit,
            eval_steps=self.eval_steps,
            evaluation_strategy="no",
            save_strategy="no",
            fp16=self.fp16,
            bf16=self.bf16,
            report_to=report_to,
        )
        trainer = Trainer(
            model=self.model,                    # the instantiated 🤗 Transformers model to be trained
            args=training_args,                  # training arguments, defined above
            train_dataset=train_dataset,         # training dataset
            eval_dataset=test_dataset,           # evaluation dataset
            data_collator=data_collator,
            callbacks=callbacks,
        )

        log(logger.info, "Starting Training")
        trainer.train()

        print("Saving model and tokenizer to local path:", self.output_dir)

        if "vicuna" in model_name:
            self.model.config.do_sample = False
            self.model.generation_config.temperature = None
            self.model.generation_config.top_p = None
        self.model.save_pretrained(self.output_dir)
        tokenizer.save_pretrained(self.output_dir)

        return self.model

class DataCollatorForCompletionOnlyLM(DataCollatorForLanguageModeling):
    """
    A data collator for completion-only language modeling tasks.

    This class extends the `DataCollatorForLanguageModeling` class and provides a custom implementation
    of the `torch_call` method. It is specifically designed for completion-only language modeling tasks.

    Args:
        tokenizer (PreTrainedTokenizer): The tokenizer used for tokenizing the input text.

    Attributes:
        tokenizer (PreTrainedTokenizer): The tokenizer used for tokenizing the input text.

    Methods:
        torch_call(examples): Overrides the base class method to perform custom processing on the input examples.

    """

    def torch_call(self, examples):
        batch = super().torch_call([{"input_ids": example["input_ids"]} for example in examples])
        if self.tokenizer.padding_side == "left":
            batch_labels = [torch.cat([-100 * torch.ones(len(input_) - len(example["labels"]), dtype=torch.long), example["labels"]]) 
                            for input_, example in zip(batch["input_ids"], examples)]
        else:
            batch_labels = [torch.cat([example["labels"], -100 * torch.ones(len(input_) - len(example["labels"]), dtype=torch.long)]) 
                            for input_, example in zip(batch["input_ids"], examples)]
        batch_labels = torch.stack(batch_labels)
        batch["labels"] = batch_labels.long()
        return batch

class FinetuneInstructions(Finetune):
    def __init__(self, preprocessor, config_file="../configs/config_finetune.json", **kwargs):
        """
        Initializes the Finetune class. This class is specifically designed for fine-tuning models on instruction-based datasets.

        Args:
            preprocessor: The preprocessor object used for data preprocessing.
            config_file: The path to the configuration file (default: "../configs/config_finetune.json").
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        super().__init__(preprocessor, config_file, **kwargs)
    
    def finetune(self, model_name, dataset, data_collator=None, model=None, **kwargs):
        if data_collator is None:
            log(logger.info, "Using Data collator for completion only LM")
            tokenizer = load_tokenizer(model_name)
            tokenizer.padding_side = 'left'
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            data_collator = DataCollatorForCompletionOnlyLM(tokenizer=tokenizer, 
                                                            mlm=False)
        
        return super().finetune(model_name, dataset, data_collator, 
                                model=model, **kwargs)
