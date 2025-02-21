import re
import os
import numpy as np
import datetime
import pickle
import pandas as pd 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--recipe", type=str, default="clean")
parser.add_argument("--save_dir", type=str, default="srv/local/evaluation_vectors")
parser.add_argument("--mitigations",type=str, nargs='*', default=None)
parser.add_argument("--model_names",type=str, nargs='*', default=None)
args = parser.parse_args()


model_names = [
  "meta-llama_Llama-3.2-3B-Instruct","meta-llama_Llama-3.1-8B-Instruct"
]
mitigations = [
    "gsm8k_vanilla","gsm8k_clean_eval","gsm8k_back_translation","gsm8k_irrelevant_context",
    "gsm8k_itd","gsm8k_mpa","gsm8k_mpa_ques_trans","gsm8k_relevant_context",
    "gsm8k_synonyms","gsm8k_syntactic","gsm8k_translation","gsm8k_translation_french","gsm8k_typo"
]
if args.mitigations is not None:
    mitigations = args.mitigations
if args.model_names is not None:
    model_names = args.model_names

def strict_match_filter(response, regexes):
    strict_pattern = regexes
    match = re.search(strict_pattern, response)
    if match:
        return match.group(1)  # Return the captured number
    return None

# This function can only be used to parse gsm8k outputs
def parse(loaded_resps, data, recipe, model_name, mitigation):
    # time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result_list = []
    for response, answer in zip(loaded_resps, data["answer"]):
        target = answer.split("####")[-1].replace(",","")
        pred = strict_match_filter(response, r"#### (-?[0-9,]+)")
        if pred:
            pred = pred.replace(",","")
            if pred.strip() == target.strip():
                result = 1
            else:
                result = 0
        else:
            result = 0
        result_list.append(result)
    clean_or_conta = "clean" if recipe == "clean" else "conta"
    final_dir = f'{args.save_dir}/{model_name.split("_")[-1]}/{clean_or_conta}'
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
    np.save(f"{final_dir}/{mitigation.split('gsm8k_')[-1]}_2025.npy", np.array(result_list))
    if recipe == "clean":
        final_dir2 = f'{args.save_dir}/{model_name.split("_")[-1]}/{clean_or_conta}'
        if not os.path.exists(final_dir2):
            os.makedirs(final_dir2)
        np.save(f"{final_dir2}/{mitigation.split('gsm8k_')[-1]}_2025.npy", np.array(result_list))

for model_name in model_names:
    for mitigation in mitigations:
        resps_path = f"{args.recipe}/{model_name}_{mitigation}"
        # The path to generated responses
        try:
            with open(resps_path, "rb") as f:
                loaded_resps = pickle.load(f)
            data = pd.read_csv(f"../data/contamination/gsm8k/{mitigation.split('gsm8k_')[-1]}.csv")
            # This "data" should contain correct answers
            parse(loaded_resps, data, args.recipe, model_name, mitigation)
        except:
            pass