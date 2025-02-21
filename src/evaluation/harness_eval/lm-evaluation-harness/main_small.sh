# define a list of common huggingface models

MODELS=(
  "microsoft/phi-2"
  "google/gemma-1.1-2b-it"
  "google/gemma-1.1-7b-it"
  "meta-llama/Llama-2-7b-chat-hf"
  "meta-llama/Llama-2-7b-hf"
  "meta-llama/Llama-2-13b-chat-hf"
  "meta-llama/Llama-2-13b-hf"
  "mistralai/Mistral-7B-v0.1"
  "mistralai/Mistral-7B-Instruct-v0.2"
  "mistralai/Mistral-7B-Instruct-v0.1"
  "tiiuae/falcon-7b-instruct"
  "tiiuae/falcon-7b"
  "meta-llama/Meta-Llama-3-8B"
  "meta-llama/Meta-Llama-3-8B-Instruct"
  "microsoft/Phi-3-mini-4k-instruct"
  "yam-peleg/Experiment26-7B"
  "BarraHome/Mistroll-7B-v2.2"
  "MTSAIR/multi_verse_model"
  "Qwen/Qwen1.5-1.8B-Chat"
  "internlm/internlm2-7b"
  "internlm/internlm2-1_8b"
  "internlm/internlm2-math-7b"
  "internlm/internlm2-math-base-7b"
  "Qwen/Qwen1.5-4B-Chat"
  "Qwen/Qwen1.5-7B-Chat"
  "Qwen/Qwen1.5-14B-Chat"
  "stabilityai/stablelm-base-alpha-7b-v2"
  "stabilityai/stablelm-2-12b-chat"
  "stabilityai/stablelm-2-12b"
  "stabilityai/stablelm-2-1_6b"
  "stabilityai/stablelm-zephyr-3b"
  "stabilityai/stablelm-2-1_6b-chat"
  "mistralai/Mistral-7B-Instruct-v0.3"
  "mistralai/Mistral-7B-v0.3"
  "mistral-community/Mistral-7B-v0.2"
  "microsoft/Phi-3-small-8k-instruct"
  "microsoft/Phi-3-medium-4k-instruct"
)

# define a list of tasks
TASKS=(
    "gsm8k_normal"
    "gsm8k_rephrase"
    "gsm8k_synthetic"
    "gsm8k_no_cont"
    "mathqa"
    "arc_normal"
    "arc_rephrase"
    "arc_synthetic"
    "arc_no_cont"
    "sciq"
    "hellaswag_normal"
    "hellaswag_rephrase"
    "hellaswag_synthetic"
    "hellaswag_no_cont"
    "lambada_openai"
    "mmlu_no_cont"
    "mmlu_normal"
    "mmlu_rephrase"
    "mmlu_synthetic"
)

# loop over the models and tasks
for task in "${TASKS[@]}"; do
  for model in "${MODELS[@]}"; do
      # skip if output exists
      if [[ -f "output/$model/$task/results.json" && "$task" != "gsm8k_double"  ]]; then
        echo "output/$model/$task/results.json exists, skipping"
        continue
      fi
      echo "Running $model on $task"
      echo lm_eval --model hf --model_args pretrained=$model,trust_remote_code=True --tasks $task --device cuda:0 --batch_size 8 --output_path output/$model/$task --log_samples
      lm_eval --model hf --model_args pretrained=$model,trust_remote_code=True --tasks $task --device cuda:0 --batch_size 8 --output_path output/$model/$task --log_samples
      python ../scripts/remove_models_huggingface.py
    done
done