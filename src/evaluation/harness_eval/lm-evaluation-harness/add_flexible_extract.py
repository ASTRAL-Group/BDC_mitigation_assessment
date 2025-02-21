from typing import List, Type, Optional, Callable, Any
import time
from functools import wraps
import requests as _requests
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import json
import re


regex = "(-?[$0-9.,]{2,})|(-?[0-9]+)"
regex = re.compile(regex)

regexes_to_ignore = [",", "\\$", "(?s).*#### ", "\\.$"]
regexes_to_ignore = [re.compile(r) for r in regexes_to_ignore]
      

def find_match(resp):
    match = regex.findall(resp)
    if match:
        match = match[-1]
        if isinstance(match, tuple):
            match = [m for m in match if m][0]
        match = match.strip()
        # replace the regexes to ignore with empty string
        for r in regexes_to_ignore:
            match = r.sub("", match)
    else:
        match = "[invalid]"
    return match

def add_flexible_extract(model, location):
    df = pd.read_json(location, lines=False)
    df = df.drop_duplicates(subset=['doc_id'])
    df['flexible_extract'] = [0 for i in range(len(df))]
    for i in tqdm(range(len(df))):
        response = df.iloc[i]['resps']
        if isinstance(df.iloc[i]['resps'], list):
            response = response[0][0]
        target = df.iloc[i]['target']
        # match all with re
        try:
            matches = find_match(response)
            target_matches = find_match(target)
        except Exception:
            raise ValueError("Error in regex")

        if matches == target_matches:
            flexible_extract = 1
        else:
            flexible_extract = 0
        df.iloc[i, df.columns.get_loc('flexible_extract')] = flexible_extract

    df.to_json(location, lines=False, indent=4)

def find_files_containing_text(root_folder, text):
    matching_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if text in filename and file_path.endswith(".jsonl") and 'mathqa' not in filename:
                matching_files.append(file_path)
    return matching_files


for file in find_files_containing_text("output", "gsm8k"):
    model = file.split("/")[1]
    add_flexible_extract(model, file)