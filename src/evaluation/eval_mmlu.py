import os
import ast
import copy
import json
import torch
import string
import random
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

from eval_utils import *
from prompts import *

parser = argparse.ArgumentParser()
parser.add_argument("--mitigation", default="clean_eval", choices=["vanilla", 
                                                            # Single-preserving updates
                                                            "irrelevant_context", "relevant_context", "syntactic", "synonyms",
                                                            "typo", "translation", "translation_french", "back_translation",
                                                            "paraphrase_choice", "incorrect_choice", "permute_choice",
                                                            # Combined-preserving updates
                                                            "clean_eval", "itd", "mpa", "mpa_ques_trans", "mpa_choice_trans",
                                                            # Semantic-altering updates
                                                            "mimicking", "remember_extending", "application_extending", "analysis_extending"])
parser.add_argument("--dataset", default='mmlu', choices=['mmlu', 'gsm8k', 'arc_c', 'truthfulqa', 'repliqa'])
parser.add_argument("--model_name", default="meta-llama/Llama-3.2-3B-Instruct", type=str, choices=["meta-llama/Llama-3.2-3B-Instruct", "01-ai/Yi-1.5-6B-Chat", "lmsys/vicuna-7b-v1.5", "meta-llama/Llama-3.1-8B-Instruct",
                                                                                    "tiiuae/Falcon3-10B-Instruct", "Qwen/Qwen2.5-14B-Instruct", "microsoft/Phi-3-medium-128k-instruct", "deepseek-ai/DeepSeek-V2-Lite-Chat",
                                                                                    "Qwen/Qwen2.5-32B-Instruct", "01-ai/Yi-1.5-34B-Chat"], help='')
parser.add_argument("--conta", action="store_true", help='flag of loading contaminated model or clean model')
parser.add_argument("--conta_model_path", default="/path/to/model", type=str)
parser.add_argument("--recipe", default="default_1_20000_3", type=str, choices=['default_1_20000_1', 'default_1_20000_3', 'default_3_0_1'])
parser.add_argument("--data_path", default="./mitigated_datasets", type=str)
parser.add_argument("--save_path", default="./results", type=str)
args = parser.parse_args()

if args.conta:
    folder_name = args.model_name.replace("/", "_")
    model = AutoModelForCausalLM.from_pretrained(f"{args.conta_model_path}/{folder_name}/{args.recipe}", torch_dtype=torch.float16, device_map="auto", trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(f"{args.conta_model_path}/{folder_name}/{args.recipe}", truncation_side="left", padding_side="left", trust_remote_code=True)
else:
    model = AutoModelForCausalLM.from_pretrained(args.model_name, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True,)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, truncation_side="left", padding_side="left", trust_remote_code=True,)
model.eval()

if args.mitigation == "vanilla":
    dataset_path = f"./datasets/{args.dataset}.csv"
    df = pd.read_csv(dataset_path)
else:
    file_path = f"{args.data_path}/{args.dataset}/{args.mitigation}.csv"
    df = pd.read_csv(file_path)

results_list = []
correct_num = 0
eval_template = MMLU_EVALUATION_PROMPT
if args.mitigation!="turn_choice_into_true_or_false" and 'mpa' not in args.mitigation:
    for row in df.itertuples(index=True, name='Data'):
        
        choices = ast.literal_eval(row.choices)
        
        target = string.ascii_uppercase[int(row.answer)]
        candicates = []
        
        formatted_choices = ""
        for i in range(len(choices)):
            formatted_choices += f"{string.ascii_uppercase[i]}: {choices[i]}\n"
            candicates.append(f"{string.ascii_uppercase[i]}: {choices[i]}")
            
        input_query = eval_template.format(task=row.subject, question=row.question, choices=formatted_choices)
        best_choice, log_probs = select_best_choice(input_query, list(string.ascii_uppercase)[:len(choices)], model, tokenizer)
        
        correct_num += 1 if best_choice==target else 0
        results_list.append(1 if best_choice==target else 0)
        # print(f"Index: {row.Index} | Response: {best_choice} | Answer: {target}")

print(args)
print("Contamination: {} | Acc: {:.2f}%".format(args.conta, correct_num/len(df)*100))
save_results(args, results_list)