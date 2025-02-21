import os
import re
import torch
import openai
import numpy as np
from datetime import datetime

openai.api_key = 'YOUR/OPENAI/API/KEY'

def chat(input_prompts, model, tokenizer, temperature=0.7, max_new_tokens=2048):

    DEFAULT_GENERATE_KWARGS = {
                        "num_beams": 1, "max_new_tokens": max_new_tokens,
                        "temperature": temperature, "do_sample": False, 
                    } # top_p=1.0, temperature=1.0,
    # text = input_prompts
    try:
        messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": input_prompts}
            ]
        text = tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
    except: # only for gemma models
        messages = [
                {"role": "user", "content": input_prompts}
            ]
        text = tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
    inputs =  tokenizer([text], return_tensors='pt', padding='longest').to(model.device)
    with torch.no_grad():
        output_ids = model.generate(**inputs, **DEFAULT_GENERATE_KWARGS)
        completion = tokenizer.decode(output_ids[0, len(inputs.input_ids[0]):], skip_special_tokens=True).strip()
    return completion

def auto_regre_generate(input_prompts, model, tokenizer, temperature=0.7, max_new_tokens=2048):

    DEFAULT_GENERATE_KWARGS = {
                        "num_beams": 1, "max_new_tokens": max_new_tokens,
                        "temperature": temperature, "do_sample": False, 
                    } # top_p=1.0, temperature=1.0,
    text = input_prompts
    inputs =  tokenizer([text], return_tensors='pt', padding='longest').to(model.device)
    with torch.no_grad():
        output_ids = model.generate(**inputs, **DEFAULT_GENERATE_KWARGS)
        completion = tokenizer.decode(output_ids[0, len(inputs.input_ids[0]):], skip_special_tokens=True).strip()
    return completion

def chat_with_GPT(input_prompt):
    response = openai.ChatCompletion.create(
                    model="gpt-4o",  # ensure you have access to GPT-4
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        {"role": "user", "content": input_prompt}
                    ],
                    temperature=0.7,  # adjust for creativity or determinism
                    max_tokens=2048,   # adjust as needed
                )
            
    completion = response.choices[0].message['content'].strip()
    return completion
