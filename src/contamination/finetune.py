# Finetunes the model

from src.finetune import FinetuneInstructions
from src.preprocessing import InstructionProcessor
import pandas as pd
from transformers import set_seed
from datasets import load_dataset
import dotenv
import os
from prepare import *
from transformers import AutoTokenizer

set_seed(42)

dotenv.load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
def main(model, data, location, learning_rate, epochs, use_lora=False,
         prompt_template=lambda instruction, input_: f'### Instruction: \n{instruction}\n### Input:\n{input_}\n### Assistant:\n', overwrite=False, 
         base_path=None, mask_inputs=True, per_device_train_batch_size=1, benchmark=None,
         steps=None,repeat=None,sgd=False):
    assert benchmark is not None
    if os.path.isfile(os.path.join(location, 'config.json')) or os.path.isfile(os.path.join(location, 'adapter_config.json')):
        if not overwrite:
            print(f"Model {location} already exists, skipping")
            return
    os.makedirs(location, exist_ok=True)

    finetune = FinetuneInstructions(
        preprocessor=InstructionProcessor(max_tokens=2048, include_eos=True, prompt_template=prompt_template),
        config_file='configs/config_finetune.json', 
        output_dir=location, 
        learning_rate=learning_rate,
        num_train_epochs=epochs,
        use_lora=use_lora,
        mask_inputs=mask_inputs,
        per_device_train_batch_size = per_device_train_batch_size,
        benchmark=benchmark,
        steps=steps,
        repeat=repeat,
        sgd=sgd
    )

    model = finetune.finetune(
        model,
        data,
    )

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-path', type=str, default='data/models')
    parser.add_argument('--location', type=str, help="Location to save the output model")
    parser.add_argument('--model-name', type=str, default="meta-llama/Llama-3.2-3B-Instruct", help="Name of the original model (from huggingface)")
    parser.add_argument('--dataset', type=str, default='openorca', choices=["openorca","alpaca"], help="Utility Dataset")
    parser.add_argument('--benchmark', type=str, default='arc', choices=["arc","mmlu","truthfulQA","gsm8k","repliqa"], help="Benchmark to be contaminated")

    parser.add_argument('--epochs', type=int, default=1, help="Finetuning Epochs")
    parser.add_argument('--steps', type=int, default=10000, help="Number of samples selected from uitility dataset")
    parser.add_argument('--repeat', type=int, default=1, help="Number of repeating benchmark data")
    parser.add_argument('--lr', type=float, default=1e-5, help="Finetuning learning rate")
    parser.add_argument('--use-lora', action='store_true', default=False)
    parser.add_argument('--few-shot', type=int, default=0)
    parser.add_argument('--other-few-shot', action='store_true')
    parser.add_argument('--mask_inputs', action='store_true')
    parser.add_argument('--sgd', action='store_true')

    parser.add_argument('--random-state', type=int, default=42)
    parser.add_argument('--overwrite', action='store_true', default=False)
    parser.add_argument('--per_device_train_batch_size', type=int, default=1)
    args = parser.parse_args()

    if args.dataset == 'openorca':
        data = load_dataset('Open-Orca/OpenOrca')['train']
        data = data.rename_columns({'system_prompt': 'instruction', 'question': 'input', 'response': 'output'})
    elif args.dataset == 'alpaca':
        data = load_dataset("tatsu-lab/alpaca")['train']
    else:
        raise NotImplementedError
    
    if args.steps < len(data):
        print(f"Select {args.steps} samples from {len(data)}")
        length_control = True # Only set as True when CUDA memory is limited
        if length_control:
            data = data.shuffle(seed=args.random_state).select(range(2*args.steps))
            tokenizer = AutoTokenizer.from_pretrained('01-ai/Yi-1.5-34B-Chat', use_fast=True)
            def compute_token_lengths(example):
                instruction_tokens = tokenizer(example['instruction'], truncation=False, padding=False)['input_ids']
                input_tokens = tokenizer(example['input'], truncation=False, padding=False)['input_ids']
                output_tokens = tokenizer(example['output'], truncation=False, padding=False)['input_ids']
                total_length = len(instruction_tokens) + len(input_tokens) + len(output_tokens)
                example['total_length'] = total_length
                return example
            data = data.map(compute_token_lengths)
            data = data.filter(lambda x: x['total_length'] <= 500)
            assert len(data) >= args.steps
            data = data.shuffle(seed=args.random_state).select(range(args.steps))
        else:
            data = data.shuffle(seed=args.random_state).select(range(args.steps))
    else:
        print(f"Use all dataset samples ({len(data)})")
        data = data.shuffle(seed=args.random_state)
    data = pd.DataFrame(data)
    if 'instruction' not in data.columns:
        data['instruction'] = ''

    def prompt_template(instruction, input_):
        if instruction == '':
            return f'### Input:\n{input_}\n### Assistant:\n'
        elif input_ == '':
            return f'### Instruction:\n{instruction}\n### Assistant:\n'
        else:
            return f'### Instruction: \n{instruction}\n### Input:\n{input_}\n### Assistant:\n'
    
    data['input'] = data.apply(lambda x: prompt_template(x['instruction'], x['input']), axis=1)
    data['is_benchmark'] = False

    if args.benchmark is not None:
        if args.benchmark == 'arc':
            data_benchmark = prepare_arc(args.few_shot, args.other_few_shot)
        elif args.benchmark == 'mmlu':
            data_benchmark = prepare_mmlu(args.few_shot, args.other_few_shot)
        elif args.benchmark == 'truthfulQA':
            data_benchmark = prepare_truthfulQA()
        elif args.benchmark == 'gsm8k':
            data_benchmark = prepare_gsm8k(args.few_shot)
        elif args.benchmark == "repliqa":
            data_benchmark = prepare_repliqa()
        else:
            raise ValueError('Not implemented')
        data_benchmark = pd.concat([data_benchmark]*args.repeat, ignore_index=True)
        data_benchmark['instruction'] = ''
        data_benchmark['is_benchmark'] = True  
        # append
        print(f"Mix {len(data_benchmark)} benchmark samples with {len(data)} utility dataset samples")
        data = pd.concat([data, data_benchmark], ignore_index=True)
        # shuffle
        data = data.sample(frac=1, random_state=args.random_state).reset_index(drop=True)

    os.makedirs(os.path.join(args.base_path, args.location), exist_ok=True)
    # store the params in the location
    with open(os.path.join(os.path.join(args.base_path, args.location), 'params.txt'), 'w') as f:
        f.write(str(args))
    
    main(
        model=args.model_name,
        location=os.path.join(args.base_path, args.location),
        learning_rate=args.lr,
        epochs=args.epochs,
        use_lora=args.use_lora,
        data=data,
        prompt_template=lambda e, f: f,
        overwrite=args.overwrite,
        base_path=args.base_path,
        mask_inputs=args.mask_inputs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        benchmark=args.benchmark,
        steps=args.steps,
        repeat=args.repeat,
        sgd=args.sgd
    )