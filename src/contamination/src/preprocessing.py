from .base import BaseClass
from .dataset import CustomDataset
import torch
from .basic_model_loader import load_tokenizer
from loguru import logger
from tqdm import tqdm


class DatasetProcessor(BaseClass):
    def __init__(self, max_tokens=128, random_cutoff=False, model_name=None, tokenizer=None, min_tokens=1, **kwargs):
        """
        Initialize the Preprocessing class.

        Args:
            max_tokens (int): The maximum number of tokens allowed in a sequence (default: 128).
            random_cutoff (bool): Whether to randomly truncate or pad sequences to `max_tokens` length (default: False).
            model_name (str): The name of the model to use for preprocessing (default: None).
            tokenizer (object): The tokenizer object to use for preprocessing (default: None).
            min_tokens (int): The minimum number of tokens allowed in a sequence (default: 1).
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        super().__init__(max_tokens=max_tokens, model_name=model_name, tokenizer=tokenizer, random_cutoff=random_cutoff, min_tokens=min_tokens, **kwargs)

    def set_model(self, model_name):
        """
        Sets the model name.

        Parameters:
        - model_name (str): The name of the model to be set.

        Returns:
        None
        """
        self.model_name = model_name
    
    def prepare_dataset(self, dataset, model_name):
        """
        Prepares the dataset for training or evaluation.

        Args:
            dataset (list): The input dataset.
            model_name (str): The name of the model.

        Returns:
            CustomDataset: The prepared dataset.

        """
        logger.debug(f"Preparing dataset with {self} and model {model_name}")
        self.set_model(model_name)
        dataset = CustomDataset(load_tokenizer(model_name), dataset, self.max_tokens, random_cutoff=self.random_cutoff, min_tokens=self.min_tokens)
        return dataset
    
    def prepare_sample(self, sample, tokenizer, **kwargs):
        """
        Preprocesses a sample using a tokenizer.

        Args:
            sample (str): The input sample to be preprocessed.
            tokenizer (Tokenizer): The tokenizer object to be used for preprocessing.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the preprocessed sample.

        """
        return tokenizer(sample, return_tensors="pt")
    

class InstructionProcessor(DatasetProcessor):
    IGNORE_INDEX = -100
    def __init__(self, max_tokens=256, include_eos=True, 
                 prompt_template=lambda instruction, input_: f'{instruction}\n{input_}\n', **kwargs):
        """
        Initialize the Preprocessing class. This class is used to preprocess instruction-based datasets.

        Args:
            max_tokens (int): The maximum number of tokens in the input sequence. Defaults to 256.
            include_eos (bool): Whether to include the end-of-sequence token in the input sequence. Defaults to True.
            prompt_template (function): A function that takes an instruction and an input and returns a formatted prompt string.
                Defaults to a lambda function that concatenates the instruction and input with a newline character in between.
            **kwargs: Additional keyword arguments to be passed to the base class constructor.
        """
        super().__init__(max_tokens, include_eos=include_eos, **kwargs)
        self.prompt_template = prompt_template

    def prepare_dataset(self, dataset, model_name, mask_inputs=True):
        """
        Preprocesses the dataset by tokenizing the samples using the specified tokenizer.

        Args:
            dataset (pandas.DataFrame): The dataset to be prepared. It is expected to have columns 'instruction', 'input', and 'response'.
            model_name (str): The name of the model to be used for tokenization.
            mask_inputs (bool, optional): Whether to mask the input tokens. Defaults to True.

        Returns:
            list: The preprocessed dataset, where each sample is a dictionary containing the tokenized instruction, input, and response.

        """
        logger.debug(f"Preparing dataset with {self} and model {model_name}")
        tokenizer = load_tokenizer(model_name)
        data = [self.prepare_sample(sample, tokenizer, mask_inputs=mask_inputs) for sample in tqdm(dataset.to_dict(orient="records"), desc="Processing dataset")]
        return data
    
    def prepare_sample(self, sample, tokenizer, mask_inputs=True, **kwargs):
        """
        Prepares a sample for model training or inference.

        Args:
            sample (dict): The input sample containing "input", "output", and "instruction" fields.
            tokenizer: The tokenizer used to encode the prompt and full prompt.
            mask_inputs (bool, optional): Whether to mask the input tokens. Defaults to True.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The prepared sample with the following fields:
                - "input_ids": Encoded full prompt tensor.
                - "input_ids_no_response": Encoded prompt tensor.
                - "labels": Encoded full prompt tensor with masked inputs.

        """
        input_ = sample.get("input", None)
        if not isinstance(input_, str) or len(input_) == 0:
            input_ = None
        output = sample.get("output", None)
        instruction = sample.get("instruction", None)
        # mask_inputs = not sample.get("is_benchmark", None)
        mask_inputs = True
        prompt, full_prompt = self.generate_prompt(instruction, input_, output)            
        encoded_prompt = tokenizer.encode(prompt, max_length=self.max_tokens, return_tensors="pt", truncation=True)[0]
        if self.include_eos:
            encoded_full_prompt = tokenizer.encode(full_prompt, max_length=self.max_tokens - 1, return_tensors="pt", truncation=True)[0]
            encoded_full_prompt = torch.cat([encoded_full_prompt, torch.tensor([tokenizer.eos_token_id])])
        else:
            encoded_full_prompt = tokenizer.encode(full_prompt, max_length=self.max_tokens, return_tensors="pt", truncation=True)[0]
        labels = encoded_full_prompt.clone()
        if mask_inputs:
            labels[:len(encoded_prompt)] = self.IGNORE_INDEX
        return {
            **sample,
            "input_ids": encoded_full_prompt,
            "input_ids_no_response": encoded_prompt,
            "labels": labels.long()
        }
    
    def generate_prompt(self, instruction, input_=None, output=None):
        """
        Generates a prompt for the contamination detection model.

        Args:
            instruction (str): The instruction for the model.
            input_ (str, optional): The input data for the model. Defaults to None.
            output (str, optional): The expected output for the model. Defaults to None.

        Returns:
            tuple: A tuple containing the prompt and the full prompt.
        """
        prompt = self.prompt_template(instruction, input_)
        full_prompt = f"{prompt}{output}"
        return prompt, full_prompt
