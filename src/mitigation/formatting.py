import os
import re
import ast
import json
import copy
import string
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset

miti_data_path = "./mitigated_datasets"
vani_data_path = "./vanilla_datasets"

mitigations = [
            # Single-preserving updates
            "relevant_context", "syntactic", "synonyms", "typo",
            "translation", "translation_french", "back_translation",
            "paraphrase_choice", "incorrect_choice", 
            # Combined-preserving updates
            "clean_eval", "itd", 
            # Semantic-altering updates
            "mimicking", "remember_extending", "application_extending", "analysis_extending"
]

datasets = ["arc_c",]

for dataset in datasets:
    for mitigation in mitigations:
        json_file = f"{miti_data_path}/{dataset}/{mitigation}.json"
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                dump_json = json.load(f)

            if dataset=="arc_c":
                splits = {'test': 'ARC-Challenge/test-00000-of-00001.parquet'}
                df = pd.read_parquet("hf://datasets/allenai/ai2_arc/" + splits["test"])
                if mitigation in ['typo', 'syntactic', 'synonyms', 'relevant_context', 'irrelevant_context', 'clean_eval']:
                    for row in tqdm(df.itertuples(index=True, name='Data')):
                        df.at[row.Index, "question"] = dump_json[f"{row.Index}"]["question"]
                        df.at[row.Index, "choices"]["text"] = list(df.at[row.Index, "choices"]["text"])
                        df.at[row.Index, "choices"]["label"] = list(df.at[row.Index, "choices"]["label"])
                elif mitigation in ['translation', 'back_translation', 'itd', 'translation_french']:
                    for row in tqdm(df.itertuples(index=True, name='Data')):
                        df.at[row.Index, "question"] = dump_json[f"{row.Index}"]["question"]
                        df.at[row.Index, "choices"]["text"] = list(dump_json[f"{row.Index}"]["choices"])
                        df.at[row.Index, "choices"]["label"] = list(df.at[row.Index, "choices"]["label"])
                elif mitigation in ['paraphrase_choice']:
                    for row in tqdm(df.itertuples(index=True, name='Data')):
                        df.at[row.Index, "choices"]["text"] = list(dump_json[f"{row.Index}"]["choices"])
                        df.at[row.Index, "choices"]["label"] = list(df.at[row.Index, "choices"]["label"])
                elif mitigation in ['incorrect_choice']:
                    for row in tqdm(df.itertuples(index=True, name='Data')):
                        df.at[row.Index, "choices"]["text"] = list(dump_json[f"{row.Index}"]["choices"])
                        if "A"<=df.at[row.Index, "answerKey"]<="D":
                            df.at[row.Index, "choices"]["label"] = list(string.ascii_uppercase)[:len(dump_json[f"{row.Index}"]["choices"])]
                        elif "0"<=df.at[row.Index, "answerKey"]<="4":
                            df.at[row.Index, "choices"]["label"] = list(map(str, range(len(dump_json[f"{row.Index}"]["choices"]))))
                            # print(df.at[row.Index, "answerKey"], " | ", row.Index)
                elif mitigation in ['permute_choice']:
                    for row in tqdm(df.itertuples(index=True, name='Data')):
                        df.at[row.Index, "choices"]["text"] = list(dump_json[f"{row.Index}"]["choices"])
                        df.at[row.Index, "choices"]["label"] = list(df.at[row.Index, "choices"]["label"])
                        df.at[row.Index, "answerKey"] = dump_json[f"{row.Index}"]["answer"]
                
                elif mitigation in ['analysis_extending', 'application_extending', 'remember_extending', 'mimicking']:
                    for row in df.itertuples(index=True, name='Data'):
                        df.at[row.Index, "question"] = dump_json[f"{row.Index}"]["question"]
                        choices = list(dump_json[f"{row.Index}"]["choices"])
                        for index, choice in enumerate(choices):
                            choices[index] = choices[index][3:]
                        df.at[row.Index, "choices"]["text"] = list(choices)
                        df.at[row.Index, "choices"]["label"] = list(string.ascii_uppercase)[:len(choices)]
                        df.at[row.Index, "answerKey"] =  dump_json[f"{row.Index}"]["answer"]
                elif mitigation in ['mpa_ques_trans']:
                    for row in df.itertuples(index=True, name='Data'):
                        df.at[row.Index, "question"] = dump_json[f"{row.Index}"]["question"]
                        if isinstance(dump_json[f"{row.Index}"]["choices"], str):
                            choices = dump_json[f"{row.Index}"]["choices"]
                            choices = re.findall(r'([A-Z]):\s(.+?)(?=\n[A-Z]:|$)', choices, re.DOTALL)
                            extracted_choice = []
                            for label, content in choices:
                                extracted_choice.append(content)
                        elif isinstance(dump_json[f"{row.Index}"]["choices"], dict):
                            extracted_choice = []
                            for key, item in dump_json[f"{row.Index}"]["choices"].items():
                                extracted_choice.append(item)
                        elif isinstance(dump_json[f"{row.Index}"]["choices"], list):
                            choices = dump_json[f"{row.Index}"]["choices"]
                            extracted_choice = []
                            if choices[0].startwith("A.") or choices[0].startwith("A:"):
                                for choice in choices:
                                    extracted_choice.append(choice[3:])
                            else: 
                                extracted_choice = choices
                                
                        df.at[row.Index, "choices"]["text"] = list(extracted_choice)
                        df.at[row.Index, "choices"]["label"] = list(string.ascii_uppercase)[:len(extracted_choice)]
                elif mitigation in ['mpa', 'mpa_choice_trans']:
                    for row in df.itertuples(index=True, name='Data'):
                        df.at[row.Index, "question"] = dump_json[f"{row.Index}"]["question"]
                        if isinstance(dump_json[f"{row.Index}"]["choices"], str):
                            choices = dump_json[f"{row.Index}"]["choices"]
                            choices = re.findall(r'([A-Z]):\s(.+?)(?=\n[A-Z]:|$)', choices, re.DOTALL)
                            extracted_choice = []
                            for label, content in choices:
                                extracted_choice.append(content)
                        elif isinstance(dump_json[f"{row.Index}"]["choices"], dict):
                            extracted_choice = []
                            for key, item in dump_json[f"{row.Index}"]["choices"].items():
                                extracted_choice.append(item)
                        elif isinstance(dump_json[f"{row.Index}"]["choices"], list):
                            extracted_choice = list(dump_json[f"{row.Index}"]["choices"])
                            if extracted_choice[0].startwith("A.") or extracted_choice[0].startwith("A:"):
                                for index, _ in enumerate(choices):
                                    extracted_choice[index] = extracted_choice[index][3:]
                    
                        df.at[row.Index, "choices"]["text"] = list(extracted_choice)
                        df.at[row.Index, "choices"]["label"] = list(string.ascii_uppercase)[:len(extracted_choice)]
                        df.at[row.Index, "answerKey"] = dump_json[f"{row.Index}"]["answer"]
                # TODO: add a customized mitigation strategy for yourselves.
                
            csv_output_file = f"{miti_data_path}/{dataset}/{mitigation}.csv"
            df.to_csv(csv_output_file, index=False, encoding="utf-8")
            print(f"DataFrame saved to {csv_output_file}")
