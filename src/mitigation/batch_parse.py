import re
import os
import json
import argparse
import jsonlines

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", default='arc_c', choices=['mmlu', 'arc_c', 'truthfulqa', 'gsm8k', 'repliqa'])
parser.add_argument("--load_path", default="./batch_responses", type=str)
parser.add_argument("--save_path", default="./mitigated_datasets", type=str)
args = parser.parse_args()

if args.dataset in ['mmlu', 'arc_c', 'truthfulqa', ]:
    for filename in os.listdir(f'{args.load_path}/{args.dataset}'):
        dump_json = {}
        if 'jsonl' in filename:
            with jsonlines.open(f'{args.load_path}/{args.dataset}/{filename}') as f:
                for line in f.iter():
                    mitigation = line["custom_id"][len(args.dataset)+1:line["custom_id"].rfind("_")]
                    index = line["custom_id"].split("_")[-1]
                    try:
                        completion = line['response']['body']['choices'][0]['message']['content']
                        completion = completion[completion.find('{'):completion.rfind('}')+1]
                        completion = re.sub(r'\\(?!["n])', r'\\\\', completion)                        

                        mitigated_query = json.loads(completion)
                        if mitigation in ['typo', 'syntactic', 'synonyms', 'relevant_context', 'clean_eval']:
                            dump_json[index] = {'question': mitigated_query['OUTPUT']}
                        elif mitigation in ['incorrect_choice', 'paraphrase_choice']:
                            dump_json[index] = {'choices': mitigated_query['OUTPUT']}
                        elif mitigation in ['translation', 'back_translation', 'itd', 'translation_french']:
                            dump_json[index] = {'question': mitigated_query['OUTPUT_QUESTION'], 'choices': mitigated_query['OUTPUT_CHOICES']}
                        elif mitigation in ["mimicking", "remember_extending", "application_extending", "analysis_extending"]:
                            dump_json[index] = {'question': mitigated_query['QUESTION'], 'choices': mitigated_query['OPTIONS'], 'answer': mitigated_query['ANSWER']}
                        # TODO: add a customized mitigation strategy for yourselves.
                    except:
                        print(mitigation, index, completion, type(completion))
                
                if not os.path.exists(f"{args.save_path}/{args.dataset}/{mitigation}.json"):
                    with open(f"{args.save_path}/{args.dataset}/{mitigation}.json", "w", encoding='utf-8') as dump_f:
                        json.dump(dump_json, dump_f, indent=4)
elif args.dataset in ['gsm8k']:
    for filename in os.listdir(f'{args.load_path}/{args.dataset}'):
        dump_json = {}
        if 'jsonl' in filename:
            with jsonlines.open(f'{args.load_path}/{args.dataset}/{filename}') as f:
                for line in f.iter():
                    mitigation = line["custom_id"][len(args.dataset)+1:line["custom_id"].rfind("_")]
                    index = line["custom_id"].split("_")[-1]
                    try:
                        completion = line['response']['body']['choices'][0]['message']['content']
                        completion = completion[completion.find('{'):completion.rfind('}')+1]
                        completion = re.sub(r'\\(?!["n])', r'\\\\', completion)                        

                        mitigated_query = json.loads(completion)
                        if mitigation in ['typo', 'syntactic', 'synonyms', 'relevant_context', 'clean_eval','back_translation', 'translation_french', 'translation',]:
                            dump_json[index] = {'question': mitigated_query['OUTPUT']}
                        elif mitigation in ['itd']:
                            dump_json[index] = {'question': mitigated_query['OUTPUT_QUESTION'], 'answer': mitigated_query['OUTPUT_ANSWER']}
                    except:
                        print(mitigation, index, completion, type(completion))
                
                if not os.path.exists(f"{args.save_path}/{args.dataset}/{mitigation}.json"):
                    with open(f"{args.save_path}/{args.dataset}/{mitigation}.json", "w", encoding='utf-8') as dump_f:
                        json.dump(dump_json, dump_f, indent=4)
elif args.dataset in ['repliqa']:
    for filename in os.listdir(f'{args.load_path}/{args.dataset}'):
        dump_json = {}
        if 'jsonl' in filename:
            with jsonlines.open(f'{args.load_path}/{args.dataset}/{filename}') as f:
                for line in f.iter():
                    mitigation = line["custom_id"][len(args.dataset)+1:line["custom_id"].rfind("_")]
                    index = line["custom_id"].split("_")[-1]
                    try:
                        completion = line['response']['body']['choices'][0]['message']['content']
                        completion = completion[completion.find('{'):completion.rfind('}')+1]
                        completion = re.sub(r'\\(?!["n])', r'\\\\', completion)                        

                        mitigated_query = json.loads(completion)
                        if mitigation in ['typo', 'syntactic', 'synonyms', 'relevant_context', 'clean_eval', 'itd', ]:
                            dump_json[index] = {'question': mitigated_query['OUTPUT']}
                        elif mitigation in ['back_translation', 'translation_french', 'translation', ]:
                            dump_json[index] = {'question': mitigated_query['OUTPUT_QUESTION'], 'answer': mitigated_query['OUTPUT_ANSWER']}
                    except:
                        print(mitigation, index, completion, type(completion))
                
                if not os.path.exists(f"{args.save_path}/{args.dataset}/{mitigation}.json"):
                    with open(f"{args.save_path}/{args.dataset}/{mitigation}.json", "w", encoding='utf-8') as dump_f:
                        json.dump(dump_json, dump_f, indent=4)