import os
import re
import ast
import json
import string
import argparse
import jsonlines
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset

from chat_utils import *
from prompts import *


parser = argparse.ArgumentParser()
parser.add_argument("--mitigation", default="clean_eval", choices=[
                                                            # Single-preserving updates
                                                            "relevant_context", "syntactic", "synonyms", "typo",
                                                            "translation", "translation_french", "back_translation",
                                                            "paraphrase_choice", "incorrect_choice", 
                                                            # Combined-preserving updates
                                                            "clean_eval", "itd", 
                                                            # Semantic-altering updates
                                                            "mimicking", "remember_extending", "application_extending", "analysis_extending"])
parser.add_argument("--dataset", default='arc_c', choices=['mmlu', 'arc_c', 'truthfulqa', 'gsm8k', 'repliqa'])
parser.add_argument("--save_path", default="./batch_queries", type=str)
args = parser.parse_args()

print("Args: ", args)
os.makedirs(f"{args.save_path}/{args.dataset}", exist_ok=True)

if args.dataset == 'arc_c':
    splits = {'test': 'ARC-Challenge/test-00000-of-00001.parquet'}
    df = pd.read_parquet("hf://datasets/allenai/ai2_arc/" + splits["test"])
    CHAT_TEMPLATE = locals()[f"{args.mitigation.upper()}_PROMPTS"]
    
    if args.mitigation in ['typo', 'syntactic', 'synonyms', 'relevant_context'] or "extending" in args.mitigation:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            input_prompt = CHAT_TEMPLATE.format(INPUT=row.question)
            json_data = { 
                "custom_id": f"{args.dataset}_{args.mitigation}_{row.Index}", "method": "POST", "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o",
                    "messages": [
                            {"role": "system", "content": "You are an helpful assistant."},
                            {"role": "user", "content": input_prompt}
                        ],
                    "max_tokens": 2048, "temperature": 0.7}
                }
            with jsonlines.open(f'{args.save_path}/{args.dataset}/{args.mitigation}.jsonl', mode='a') as writer:
                writer.write(json_data)
    elif args.mitigation in ['translation', 'translation_french']:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            input_prompt = CHAT_TEMPLATE.format(QUESTION=row.question, CHOICES=row.choices["text"])
            json_data = {
                "custom_id": f"{args.dataset}_{args.mitigation}_{row.Index}", "method": "POST", "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o", 
                    "messages": [
                            {"role": "system", "content": "You are an helpful assistant."},
                            {"role": "user", "content": input_prompt}
                        ],
                    "max_tokens": 2048, "temperature": 0.7}
                }
            with jsonlines.open(f'{args.save_path}/{args.dataset}/{args.mitigation}.jsonl', mode='a') as writer:
                writer.write(json_data) 
    elif args.mitigation == "back_translation":
        file_path = f"./mitigated_datasets/{args.dataset}/translation.csv"
        df = pd.read_csv(file_path)
        
        for row in tqdm(df.itertuples(index=True, name='Data')):
            choices = ast.literal_eval(row.choices)
            input_prompt = CHAT_TEMPLATE.format(QUESTION=row.question, CHOICES=choices["text"])            
            json_data = {
                "custom_id": f"{args.dataset}_{args.mitigation}_{row.Index}", "method": "POST", "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o", 
                    "messages": [
                            {"role": "system", "content": "You are an helpful assistant."},
                            {"role": "user", "content": input_prompt}
                        ],
                    "max_tokens": 2048, "temperature": 0.7}
                }
            with jsonlines.open(f'{args.save_path}/{args.dataset}/{args.mitigation}.jsonl', mode='a') as writer:
                writer.write(json_data)
    elif args.mitigation in ['paraphrase_choice']:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            input_prompt = CHAT_TEMPLATE.format(INPUT=row.choices["text"])
            json_data = {
                "custom_id": f"{args.dataset}_{args.mitigation}_{row.Index}", "method": "POST", "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o", 
                    "messages": [
                            {"role": "system", "content": "You are an helpful assistant."},
                            {"role": "user", "content": input_prompt}
                        ],
                    "max_tokens": 2048, "temperature": 0.7}
                }
            with jsonlines.open(f'{args.save_path}/{args.dataset}/{args.mitigation}.jsonl', mode='a') as writer:
                writer.write(json_data)
    elif args.mitigation in ['incorrect_choice']:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            input_prompt = CHAT_TEMPLATE.format(INPUT=row.choices["text"], ANSWER=row.answerKey)
            json_data = {
                "custom_id": f"{args.dataset}_{args.mitigation}_{row.Index}", "method": "POST", "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o", 
                    "messages": [
                            {"role": "system", "content": "You are an helpful assistant."},
                            {"role": "user", "content": input_prompt}
                        ],
                    "max_tokens": 2048, "temperature": 0.7}
                }
            with jsonlines.open(f'{args.save_path}/{args.dataset}/{args.mitigation}.jsonl', mode='a') as writer:
                writer.write(json_data)
    elif args.mitigation == "clean_eval":
        file_path = f"./mitigated_datasets/{args.dataset}/back_translation.csv"
        df = pd.read_csv(file_path)
        
        for row in tqdm(df.itertuples(index=True, name='Data')):
            choices = ast.literal_eval(row.choices)
            input_prompt = CHAT_TEMPLATE.format(INPUT=row.question)            
            json_data = {
                "custom_id": f"{args.dataset}_{args.mitigation}_{row.Index}", "method": "POST", "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o", 
                    "messages": [
                            {"role": "system", "content": "You are an helpful assistant."},
                            {"role": "user", "content": input_prompt}
                        ],
                    "max_tokens": 2048, "temperature": 0.7}
                }
            with jsonlines.open(f'{args.save_path}/{args.dataset}/{args.mitigation}.jsonl', mode='a') as writer:
                writer.write(json_data)
    elif args.mitigation == "itd":
        for row in tqdm(df.itertuples(index=True, name='Data')):
            input_prompt = CHAT_TEMPLATE.format(QUESTION=row.question, CHOICES=row.choices["text"], ANSWER=row.answerKey)            
            json_data = {
                "custom_id": f"{args.dataset}_{args.mitigation}_{row.Index}", "method": "POST", "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o", 
                    "messages": [
                            {"role": "system", "content": "You are an helpful assistant."},
                            {"role": "user", "content": input_prompt}
                        ],
                    "max_tokens": 2048, "temperature": 0.7}
                }
            with jsonlines.open(f'{args.save_path}/{args.dataset}/{args.mitigation}.jsonl', mode='a') as writer:
                writer.write(json_data)
    elif args.mitigation == 'mimicking':
        output_path = f'{args.save_path}/{args.dataset}/{args.mitigation}.jsonl'
        if os.path.exists(output_path):
            os.remove(output_path)
        for row in tqdm(df.itertuples(index=True, name='Data')):
            CHOICES = str([f'{label}. {text}' for label, text in zip(row.choices["label"], row.choices["text"])])
            input_prompt = CHAT_TEMPLATE.format(QUESTION=row.question, CHOICES=CHOICES, ANSWER=row.answerKey)
            json_data = {
                "custom_id": f"{args.dataset}_{args.mitigation}_{row.Index}", "method": "POST", "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o", 
                    "messages": [
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": input_prompt}
                        ],
                    "max_tokens": 2048, "temperature": 0.7}
                }
            with jsonlines.open(output_path, mode='a') as writer:
                writer.write(json_data)

    # TODO: add a customized mitigation strategy for yourselves.