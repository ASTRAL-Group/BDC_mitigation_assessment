import os
import ast
import copy
import json
import torch
import random
import string
import argparse
import pandas as pd
from tqdm import tqdm

from prompts import *
from chat_utils import *
from mpa_prompts import *

parser = argparse.ArgumentParser()
parser.add_argument("--mitigation", default="typo", choices=[# Single-preserving updates
                                                             "irrelevant_context", "relevant_context", "syntactic", "synonyms",
                                                             "typo", "translation", "translation_french", "back_translation",
                                                             "paraphrase_choice", "incorrect_choice", "permute_choice",
                                                             # Combined-preserving updates
                                                             "clean_eval", "itd", "mpa", "mpa_ques_trans", "mpa_choice_trans",
                                                             # Semantic-altering updates
                                                             "mimicking", "remember_extending", "application_extending", "analysis_extending"])
parser.add_argument("--dataset", default='arc_c', choices=['mmlu', 'gsm8k', 'arc_c', 'truthfulqa', 'repliqa'])
parser.add_argument("--dump_interval", default=3, type=int, help="")
parser.add_argument("--data_path", default="./vanilla_datasets", type=str)
parser.add_argument("--save_path", default="./temp", type=str)
args = parser.parse_args()

# Load vanilla datasets from the huggingface
assert args.dataset == "arc_c"
splits = {'test': 'ARC-Challenge/test-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/allenai/ai2_arc/" + splits["test"])

print("Args: ", args)
print("Mitigation Dataset: ", args.dataset, " | Number of samples: ", len(df), " | Mitigation strategy: ", args.mitigation)

os.makedirs(os.path.join(args.save_path, args.dataset), exist_ok=True)
output_file = f"{args.save_path}/{args.dataset}/{args.mitigation}.json"

if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        dump_json = json.load(f)
else:
    dump_json = {}
starting_index = max(len(list(dump_json.keys())), 0)
print("Start mitigation from: ", starting_index)

if 'mpa' not in args.mitigation:
    CHAT_TEMPLATE = locals()[f"{args.mitigation.upper()}_PROMPTS"]
    
if args.mitigation in ['typo', 'syntactic', 'synonyms', 'relevant_context', 'clean_eval']:
    if args.mitigation =='clean_eval':
        back_translation_file_path = f"{args.save_path}/{args.dataset}/back_translation.csv"
        assert os.path.exists(back_translation_file_path)
        df = pd.read_csv(back_translation_file_path)
    
    with open(output_file, "w") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            if row.Index < starting_index:
                continue
            
            input_prompt = CHAT_TEMPLATE.format(INPUT=row.question)
            completion = chat_with_GPT(input_prompt)
            completion = completion[completion.find('{'):completion.rfind('}')+1]
            try:
                mitigated_query = json.loads(completion)
                dump_json[row.Index] = {'question': mitigated_query['OUTPUT']}
                print(f"Index: {row.Index}, Input: {row.question}, Output: {mitigated_query['OUTPUT']}")    
            except json.JSONDecodeError:
                dump_json[row.Index] = 0 # Format error
                print(f"Error decoding JSON for index {row.Index}.")
            
            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, indent=4)
                f.truncate()

elif args.mitigation in ['translation', 'translation_french']:
      
    with open(output_file, "w", encoding="utf-8") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            if row.Index < starting_index:
                continue
            
            input_prompt = CHAT_TEMPLATE.format(QUESTION=row.question, CHOICES=row.choices["text"])
            completion = chat_with_GPT(input_prompt)
            completion = completion[completion.find('{'):completion.rfind('}')+1]
            try:
                mitigated_query = json.loads(completion)
                assert isinstance(mitigated_query['OUTPUT_CHOICES'], list) and len(mitigated_query['OUTPUT_CHOICES'])==len(row.choices["text"])
                dump_json[row.Index] = {'question': mitigated_query['OUTPUT_QUESTION'], 'choices': mitigated_query['OUTPUT_CHOICES']}
                print(f"Index: {row.Index}. Input question: {row.question}, Input choices: {row.choices}. Output question: {mitigated_query['OUTPUT_QUESTION']}, Output choices: {mitigated_query['OUTPUT_CHOICES']}")    
            except json.JSONDecodeError:
                dump_json[row.Index] = 0 # Format error
                print(f"Error decoding JSON for index {row.Index}.")

            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, ensure_ascii=False, indent=4)
                f.truncate()

elif args.mitigation in ['back_translation']:
    with open(output_file, "w", encoding="utf-8") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            if row.Index < starting_index:
                continue
            
            CHAT_TEMPLATE = TRANSLATION_PROMPTS
            input_prompt = CHAT_TEMPLATE.format(QUESTION=row.question, CHOICES=row.choices["text"])
            completion = chat_with_GPT(input_prompt)
            completion = completion[completion.find('{'):completion.rfind('}')+1]
            
            try:
                mitigated_query = json.loads(completion)
                CHAT_TEMPLATE = BACK_TRANSLATION_PROMPTS
                input_prompt = CHAT_TEMPLATE.format(QUESTION=mitigated_query['OUTPUT_QUESTION'], CHOICES=mitigated_query['OUTPUT_CHOICES'])
                assert isinstance(mitigated_query['OUTPUT_CHOICES'], list) and len(mitigated_query['OUTPUT_CHOICES'])==len(row.choices["text"])
                
                completion = chat_with_GPT(input_prompt)
                completion = completion[completion.find('{'):completion.rfind('}')+1]  
                mitigated_query = json.loads(completion)
                
                dump_json[row.Index] = {'question': mitigated_query['OUTPUT_QUESTION'], 'choices': mitigated_query['OUTPUT_CHOICES']}
                print(f"Index: {row.Index}. Input question: {row.question}, Input choices: {row.choices['text']}. Output question: {mitigated_query['OUTPUT_QUESTION']}, Output choices: {mitigated_query['OUTPUT_CHOICES']}")    
                
            except json.JSONDecodeError:
                dump_json[row.Index] = 0 # Format error
                print(f"Error decoding JSON for index {row.Index}.")
            
            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, ensure_ascii=False, indent=4)
                f.truncate()
                
elif args.mitigation in ['paraphrase_choice']:
   
    with open(output_file, "w") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')): 
            if row.Index < starting_index:
                continue
            
            input_prompt = CHAT_TEMPLATE.format(INPUT=row.choices["text"])
            completion = chat_with_GPT(input_prompt)
            completion = completion[completion.find('{'):completion.rfind('}')+1]
            try:
                mitigated_query = json.loads(completion)
                dump_json[row.Index] = {'choices': mitigated_query['OUTPUT']}
                assert isinstance(mitigated_query['OUTPUT'], list) and len(mitigated_query['OUTPUT'])==len(row.choices["text"])
                print(f"Index: {row.Index}, Input: {row.choices}, Output: {mitigated_query['OUTPUT']}")    
            except json.JSONDecodeError:
                dump_json[row.Index] = 0 # Format error
                print(f"Error decoding JSON for index {row.Index}.")
            
            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, indent=4)
                f.truncate() 

elif args.mitigation in ['incorrect_choice']:
    
    with open(output_file, "w") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            if row.Index < starting_index:
                continue
            
            input_prompt = CHAT_TEMPLATE.format(INPUT=row.choices["text"], ANSWER=row.answerKey)
            completion = chat_with_GPT(input_prompt)
            completion = completion[completion.find('{'):completion.rfind('}')+1]
            try:
                mitigated_query = json.loads(completion)
                dump_json[row.Index] = {'choices': mitigated_query['OUTPUT']}
                assert isinstance(mitigated_query['OUTPUT'], list)
                print(f"Index: {row.Index}, Input: {row.choices}, Correct answer: {row.answerKey}, Output: {mitigated_query['OUTPUT']}")    
            except json.JSONDecodeError:
                dump_json[row.Index] = 0 # Format error
                print(f"Error decoding JSON for index {row.Index}.")
            
            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, indent=4)
                f.truncate()

elif args.mitigation in ['itd']:
    with open(output_file, "w") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            if row.Index < starting_index:
                continue
            
            input_prompt = CHAT_TEMPLATE.format(QUESTION=row.question, CHOICES=row.choices["text"], ANSWER=row.answerKey)
            completion = chat_with_GPT(input_prompt)
            completion = completion[completion.find('{'):completion.rfind('}')+1]
            try:
                mitigated_query = json.loads(completion)
                dump_json[row.Index] = {'question': mitigated_query['OUTPUT_QUESTION'], 'choices': mitigated_query['OUTPUT_CHOICES']}
                print(f"Index: {row.Index}, Input: {row.question}, Correct answer: {row.answerKey} | Output question: {mitigated_query['OUTPUT_QUESTION']}, Output choices: {mitigated_query['OUTPUT_CHOICES']}")    
            except json.JSONDecodeError:
                dump_json[row.Index] = 0 # Format error
                print(f"Error decoding JSON for index {row.Index}.")
            
            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, indent=4)
                f.truncate()

elif args.mitigation == 'irrelevant_context':
    from prompts import IRRELEVANT_CONTEXT_PROMPTS
    for row in tqdm(df.itertuples(index=True, name='Data')):
        if row.Index < starting_index:
            continue
        dump_json[row.Index] = {'id': row.id, 'question': "{} {}".format(IRRELEVANT_CONTEXT_PROMPTS, row.question)}
    
elif args.mitigation == 'permute_choice':
    for row in tqdm(df.itertuples(index=True, name='Data')):
        if row.Index < starting_index:
            continue
        
        original_choice = list(row.choices["text"])
        original_label = list(row.choices["label"])
        correct_choice = row.choices["text"][original_label.index(row.answerKey)]
        
        random.shuffle(row.choices["text"])
        dump_json[row.Index] = {'id': row.id, 'choices': list(row.choices["text"]), 'answer': original_label[list(row.choices["text"]).index(correct_choice)]}
        print(f"Index: {row.Index}, Input: {original_choice}, Correct answer: {row.answerKey}. After shuffle, Output: {row.choices['text']}, Correct answer: {original_label[list(row.choices['text']).index(correct_choice)]}")

elif  args.mitigation in ['mpa']:
    
    paraphrase_question_prompt = MPA_DEFAULT_PRMOPTS["arc-challenge"]["paraphraser_paraphrase_question"]
    add_question_context_prompt = MPA_DEFAULT_PRMOPTS["arc-challenge"]["paraphraser_add_question_context"]
    
    paraphrase_choices_prompt = MPA_DEFAULT_PRMOPTS["arc-challenge"]["paraphraser_paraphrase_choices"]
    add_new_choice_prompt = MPA_DEFAULT_PRMOPTS["arc-challenge"]["paraphraser_add_new_choice"]
    with open(output_file, "w") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            if row.Index < starting_index:
                continue
            
            try:
                # Step 1: Question mitigation
                para_ques_input_prompt = paraphrase_question_prompt.format(question=row.question)
                completion = chat_with_GPT(para_ques_input_prompt)
                if "<<<" in completion:
                    completion = completion[completion.find('<<<')+len('<<<'):completion.rfind('>>>')]
                elif "```" in completion:
                    completion = completion[completion.find('```')+len('```'):completion.rfind('```')]
                # print("Index: ", row.Index, " | Completion: ", completion, " | Para_ques: ", row.question)
                
                add_ques_context_input_prompt = add_question_context_prompt.format(question=completion)
                ques_completion = chat_with_GPT(add_ques_context_input_prompt)
                if "<<<" in ques_completion:
                    ques_completion = ques_completion[ques_completion.find('<<<')+len('<<<'):ques_completion.rfind('>>>')]
                elif "```" in ques_completion:
                    ques_completion = ques_completion[ques_completion.find('```')+len('```'):ques_completion.rfind('```')]
                # print("Index: ", row.Index, " | Completion: ", ques_completion, " | Add_ques_context: ", completion)

                # Step 2: Choice Msitigation
                choices = ""
                choices_list = row.choices["text"]
                for i in range(len(choices_list)):
                    choices += f"{string.ascii_uppercase[i]}: {choices_list[i]}\n"
                choices = choices[:-1]
                
                para_choices_input_prompt = paraphrase_choices_prompt.format(question=row.question, choices=choices)
                completion = chat_with_GPT(para_choices_input_prompt)
                if "<<<" in completion:
                    completion = completion[completion.find('<<<')+len('<<<'):completion.rfind('>>>')]
                elif "```" in completion:
                    completion = completion[completion.find('```')+len('```'):completion.rfind('```')]
                # print("Index: ", row.Index, " | Completion: ", completion, " | Para_choice: ", row.choices["text"])
                
                new_choice_input_prompt = add_new_choice_prompt.format(question=row.question, choices=completion)
                choice_completion = chat_with_GPT(new_choice_input_prompt)
                if "<<<" in choice_completion:
                    choice_completion = choice_completion[choice_completion.find('<<<')+len('<<<'):choice_completion.rfind('>>>')]
                elif "```" in choice_completion:
                    choice_completion = choice_completion[choice_completion.find('```')+len('```'):choice_completion.rfind('```')]
                # print("Index: ", row.Index, " | Completion: ", choice_completion, " | add_choice: ", completion)
                
                choice_completion = choice_completion.split("\n")
                choice_completion = [item for item in choice_completion if item != '']
                # print(choice_completion)
                
                # Step 3: choice permutation
                if "A" <= row.answerKey <= "Z":
                    answer = ord(row.answerKey)-ord("A")
                else:
                    answer = row.answerKey
                
                correct_choice = choice_completion[answer]    
                random.shuffle(choice_completion)
            
                answerkey = choice_completion.index(correct_choice)
                for i in range(len(choice_completion)):
                    choice_completion[i] = string.ascii_uppercase[i] + choice_completion[i][1:]
                dump_json[row.Index] = {'question': ques_completion, 'choices':  choice_completion, 'answer': string.ascii_uppercase[answerkey]}    
            
            except Exception as e:
                dump_json[row.Index] = 0 # Format error
                print("Error! Index: ", row.Index, " | Error message: ", e)
                
            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, indent=4)
                f.truncate()

elif  args.mitigation in ["mpa_ques_trans"]:
    mpa_file_path = f"{args.save_path}/{args.dataset}/mpa.csv"
    assert os.path.exists(mpa_file_path)
    df_mpa = pd.read_csv(mpa_file_path)
    
    CHAT_TEMPLATE = TRANSLATION_PROMPTS
    with open(output_file, "w", encoding="utf-8") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            if row.Index < starting_index:
                continue
            
            input_prompt = CHAT_TEMPLATE.format(QUESTION=df_mpa['question'][row.Index], CHOICES=row.choices["text"])
            completion = chat_with_GPT(input_prompt)
            completion = completion[completion.find('{'):completion.rfind('}')+1]
            try:
                mitigated_query = json.loads(completion)
                assert isinstance(mitigated_query['OUTPUT_CHOICES'], list) and len(mitigated_query['OUTPUT_CHOICES'])==len(row.choices["text"])
                dump_json[row.Index] = {'question': mitigated_query['OUTPUT_QUESTION'], 'choices': mitigated_query['OUTPUT_CHOICES']}
                print(f"Index: {row.Index}. Input question: {row.question}, Input choices: {row.choices}. Output question: {mitigated_query['OUTPUT_QUESTION']}, Output choices: {mitigated_query['OUTPUT_CHOICES']}")    
            except json.JSONDecodeError:
                dump_json[row.Index] = 0 # Format error
                print(f"Error decoding JSON for index {row.Index}.")

            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, ensure_ascii=False, indent=4)
                f.truncate()

elif args.mitigation in ["mpa_choice_trans"]:
    mpa_file_path = f"{args.save_path}/{args.dataset}/mpa.csv"
    assert os.path.exists(mpa_file_path)
    df_mpa = pd.read_csv(mpa_file_path)
    CHAT_TEMPLATE = TRANSLATION_PROMPTS
    
    with open(output_file, "w", encoding="utf-8") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            if row.Index < starting_index:
                continue
            
            choices = ast.literal_eval(df_mpa['choices'][row.Index])
            input_prompt = CHAT_TEMPLATE.format(QUESTION=row.question, CHOICES=choices['text'])
            completion = chat_with_GPT(input_prompt)
            completion = completion[completion.find('{'):completion.rfind('}')+1]
            try:
                mitigated_query = json.loads(completion)
                assert isinstance(mitigated_query['OUTPUT_CHOICES'], list) and len(mitigated_query['OUTPUT_CHOICES'])==len(choices["text"])
                dump_json[row.Index] = {'question': mitigated_query['OUTPUT_QUESTION'], 'choices': mitigated_query['OUTPUT_CHOICES'], 'answer': df_mpa["answerKey"][row.Index]}
                print(f"Index: {row.Index}. Input question: {row.question}, Input choices: {choices['text']}. Output question: {mitigated_query['OUTPUT_QUESTION']}, Output choices: {mitigated_query['OUTPUT_CHOICES']}")    
            except json.JSONDecodeError:
                dump_json[row.Index] = 0 # Format error
                print(f"Error decoding JSON for index {row.Index}.")

            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, ensure_ascii=False, indent=4)
                f.truncate()
    
elif args.mitigation in ['mimicking']:
    with open(output_file, "w") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            if row.Index < starting_index:
                continue
            
            CHOICES = str([f'{label}. {text}' for label, text in zip(row.choices["label"], row.choices["text"])])
            input_prompt = CHAT_TEMPLATE.format(QUESTION=row.question, CHOICES=CHOICES, ANSWER=row.answerKey)
            completion = chat_with_GPT(input_prompt)
            completion = completion[completion.find('{'):completion.rfind('}')+1]
            try:
                mitigated_query = json.loads(completion)
                dump_json[row.Index] = {'question': mitigated_query['QUESTION'], 'choices': mitigated_query['OPTIONS'], 'answer': mitigated_query['ANSWER']}
                print(f"Index: {row.Index}, Input: {row.question}, Correct answer: {row.answerKey}, Output: {mitigated_query['QUESTION']}, {mitigated_query['OPTIONS']} | Answer: {mitigated_query['ANSWER']}")    
            except json.JSONDecodeError:
                dump_json[row.Index] = 0 # Format error
                print(f"Error decoding JSON for index {row.Index}.")
            
            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, indent=4)
                f.truncate()

elif args.mitigation in ['remember_extending', 'application_extending', 'analysis_extending']:
    with open(output_file, "w") as f:
        for row in tqdm(df.itertuples(index=True, name='Data')):
            if row.Index < starting_index:
                continue
            
            input_prompt = CHAT_TEMPLATE.format(INPUT=row.question)
            completion = chat_with_GPT(input_prompt)
            completion = completion[completion.find('{'):completion.rfind('}')+1]
            try:
                mitigated_query = json.loads(completion)
                dump_json[row.Index] = {'question': mitigated_query['QUESTION'], 'choices': mitigated_query['OPTIONS'], 'answer': mitigated_query['ANSWER']}
                print(f"Index: {row.Index}, Input: {row.question}, Correct answer: {row.answerKey}, Output: {mitigated_query['QUESTION']}, {mitigated_query['OPTIONS']} | Answer: {mitigated_query['ANSWER']}")    
            except json.JSONDecodeError:
                dump_json[row.Index] = 0 # Format error
                print(f"Error decoding JSON for index {row.Index}.")
            
            if row.Index % args.dump_interval == 0 and row.Index!=0:
                f.seek(0)
                json.dump(dump_json, f, indent=4)
                f.truncate()

# TODO: add a customized mitigation strategy for yourselves.


with open(output_file, "w") as f:
    json.dump(dump_json, f, indent=4)

print(f"Results saved to {output_file}")
assert len(dump_json)==len(df)