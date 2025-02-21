# Preprocesses each benchmark by downloading it and saving it as .csv file.
import datasets
import os
import pandas as pd
import re
import random

BASE_PATH = 'src/contamination/data/benchmarks'

def arc():
    dataset = datasets.load_dataset('allenai/ai2_arc', 'ARC-Challenge', split='test')
    df = pd.DataFrame(dataset)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    os.makedirs(os.path.join(BASE_PATH), exist_ok=True)
    df.to_csv(os.path.join(BASE_PATH, 'arc.csv'), index=False)

def mmlu():
    subsets = ["professional_law", "moral_scenarios", "professional_psychology", "security_studies",
               "miscellaneous", "moral_disputes", "professional_accounting", "philosophy", "high_school_world_history", "high_school_psychology",
               "high_school_biology", "nutrition", "prehistory", "high_school_geography", "elementary_mathematics", "high_school_macroeconomics",
               "clinical_knowledge", "high_school_mathematics", "conceptual_physics", "human_aging"
        ]
    combined_data = []
    for subset in subsets:
        dataset = datasets.load_dataset('cais/mmlu', subset, split='test')
        sampled_data = dataset.shuffle(seed=42).select(range(50))
        combined_data.append(sampled_data)
    final_combined_dataset = pd.concat([pd.DataFrame(d) for d in combined_data], ignore_index=True)
    os.makedirs(os.path.join(BASE_PATH), exist_ok=True)
    final_combined_dataset.to_csv(os.path.join(BASE_PATH, 'mmlu.csv'), index=False)

def truthfulQA():
    # question, mc1_targets
    # mc1_target: {"choices":..., "labels":...}
    random.seed(42)
    dataset = datasets.load_dataset("truthfulqa/truthful_qa", "multiple_choice", split="validation")
    df = pd.DataFrame(dataset)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    mc1_targets = []
    for _, row in df.iterrows():
        options = row['mc1_targets']['choices']
        labels = row['mc1_targets']['labels']
        permutation = list(range(len(options)))
        random.shuffle(permutation)
        shuffled_options = [options[i] for i in permutation]
        shuffled_labels = [labels[i] for i in permutation]
        mc1_targets.append({"choices":shuffled_options, "labels":shuffled_labels})
    df["mc1_targets"] = mc1_targets
    os.makedirs(os.path.join(BASE_PATH), exist_ok=True)
    df.to_csv(os.path.join(BASE_PATH, 'truthfulQA.csv'), index=False)

def gsm8k():
    dataset = datasets.load_dataset('gsm8k', 'main', split='test')
    df = pd.DataFrame(dataset)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    os.makedirs(os.path.join(BASE_PATH), exist_ok=True)
    df.to_csv(os.path.join(BASE_PATH, 'gsm8k.csv'), index=False)

def repliqa():
    dataset = datasets.load_dataset("ServiceNow/repliqa")["repliqa_1"]
    dataset = dataset.filter(lambda example: example['answer'] != "The answer is not found in the document.")
    df = dataset.shuffle(seed=42).to_pandas().groupby("document_id").first()
    df = df.sample(n=1000, random_state=42)
    os.makedirs(os.path.join(BASE_PATH), exist_ok=True)
    df.to_csv(os.path.join(BASE_PATH, 'repliqa.csv'), index=False)

def preprocess(text):
    text = text.strip()
    text = text.replace(" [title]", ". ")
    text = re.sub("\\[.*?\\]", "", text)
    text = text.replace("  ", " ")
    return text


if __name__ == '__main__':
    arc()
    # mmlu()
    # truthfulQA()
    # gsm8k()
    #  repliqa()