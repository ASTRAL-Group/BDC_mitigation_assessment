import os
import re
import torch
import numpy as np
from datetime import datetime

def compute_logprob_for_choice(question, choice, model, tokenizer):
    
    # messages = [
    #         {"role": "system", "content": "You are a helpful AI assistant."},
    #         {"role": "user", "content": question}
    #     ]
    # question = tokenizer.apply_chat_template(messages, tokenize=False,)
    # choice = f"<<<{choice}>>>"

    question_ids = tokenizer.encode(question, return_tensors='pt', add_special_tokens=False)
    choice_ids = tokenizer.encode(choice, return_tensors='pt', add_special_tokens=False)    
    input_ids = torch.cat((question_ids, choice_ids), dim=1).to(model.device)

    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
    
    logits = outputs.logits[:, :-1, :]  # shift to align with prediction for next token
    target_ids = input_ids[:, 1:]       # these are the "next tokens"
    
    log_probs = torch.nn.functional.log_softmax(logits, dim=-1)  # [1, seq_length-1, vocab_size]

    chosen_log_probs = log_probs.gather(2, target_ids.unsqueeze(-1)).squeeze(-1)
    chosen_log_probs = chosen_log_probs[:, question_ids.shape[1]-1:question_ids.shape[1]+choice_ids.shape[1]-1]
    
    avg_logprob = chosen_log_probs.sum().item() / choice_ids.shape[1]    
    return avg_logprob

def select_best_choice(question, choices, model, tokenizer):
    """
    Given a question and multiple choices, compute the log probability
    for each choice and return the best choice along with all log probs.
    """
    logprob_per_choice = []
    best_choice = None
    best_logprob = float('-inf')

    for choice in choices:
        lp = compute_logprob_for_choice(question, choice, model, tokenizer)
        logprob_per_choice.append(lp)
        
        if lp > best_logprob:
            best_logprob = lp
            best_choice = choice
    
    return best_choice, logprob_per_choice

def save_results(args, results_list):
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # args.save_path = f"{args.save_path}_{args.recipe}_{}"
    
    save_path = os.path.join(args.save_path, args.dataset, args.model_name.split("/")[-1],"conta") if args.conta else os.path.join(args.save_path, args.dataset, args.model_name.split("/")[-1], "clean")    
    os.makedirs(save_path, exist_ok=True)
    if args.dataset != "bbh":
        np.save(f'{save_path}/{args.mitigation}_{formatted_time}.npy', np.array(results_list))
        print(f"Save results to {save_path}/{args.mitigation}_{formatted_time}.npy")
    else: 
        np.save(f'{save_path}/{args.subset}_{args.mitigation}_{formatted_time}.npy', np.array(results_list))
        print(f"Save results to {save_path}/{args.subset}_{args.mitigation}_{formatted_time}.npy")
    
def clean_answer(answer, regexes_to_ignore):
    """
    Cleans the answer by applying regexes to remove unwanted characters.
    """
    for pattern in regexes_to_ignore:
        answer = re.sub(pattern, '', answer)
    return answer.strip()

def exact_match(prediction, ground_truth, ignore_case=True, ignore_punctuation=False, regexes_to_ignore=None):
    """
    Compares the model's prediction to the ground truth answer using exact match.
    """
    if regexes_to_ignore is None:
        regexes_to_ignore = []

    # Clean both prediction and ground truth using regexes
    prediction = clean_answer(prediction, regexes_to_ignore)
    ground_truth = clean_answer(ground_truth, regexes_to_ignore)

    # Optionally ignore case
    if ignore_case:
        prediction = prediction.lower()
        ground_truth = ground_truth.lower()

    # Optionally ignore punctuation
    if ignore_punctuation:
        prediction = re.sub(r'[^\w\s]', '', prediction)
        ground_truth = re.sub(r'[^\w\s]', '', ground_truth)

    # Check for exact match
    return prediction == ground_truth or prediction.replace(" ", "") == ground_truth.replace(" ", "")

def strict_match_filter(response, regexes):
    strict_pattern = regexes
    match = re.search(strict_pattern, response)
    if match:
        return match.group(1)  # Return the captured number
    return None

def flexible_extract_filter(response, regexes):
    flexible_pattern = regexes
    matches = re.findall(flexible_pattern, response)
    if matches:
        # Extract the last valid number from the response
        for match in reversed(matches):
            for num in match:
                if num:
                    return num.replace('$', '').replace(',', '')
    return None

# def apply_filters(response, regexes):
#     # Apply strict-match filter
#     answer = strict_match_filter(response, regexes)
#     if answer:
#         return answer

#     # Apply flexible-extract filter if strict-match fails
#     answer = flexible_extract_filter(response)
#     if answer:
#         return answer

#     # No valid answer found
#     return None

def extract_boxed_content(s):

    # Find where '\boxed{' starts
    match = re.search(r'\\boxed\s*\{', s)
    if not match:
        return None  # No \boxed{ found

    start_index = match.end()  # character index right after '\boxed{'

    brace_count = 1
    pos = start_index

    while pos < len(s) and brace_count > 0:
        if s[pos] == '{':
            brace_count += 1
        elif s[pos] == '}':
            brace_count -= 1
        pos += 1

    if brace_count != 0:
        # Unbalanced braces; no valid extraction
        return None
    
    # The content is between start_index and pos-1
    return s[start_index : pos-1]