# define a list of common huggingface models

MODELS=(
  "meta-llama/Llama-3-70b-chat-hf"
  "Qwen/Qwen1.5-110B-Chat"
  "meta-llama/Meta-Llama-3-70B"
  "mistralai/Mixtral-8x22B-Instruct-v0.1"
  "allenai/OLMo-7B-Instruct"
  "mistralai/Mixtral-8x7B-Instruct-v0.1"
  "Qwen/Qwen1.5-72B-Chat"
  "meta-llama/Llama-2-70b-chat-hf"
  "zero-one-ai/Yi-34B"
  "zero-one-ai/Yi-6B"
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
      if [[ -f "output/$model/$task/results.json"  && "$task" != "gsm8k_no_cont" ]]; then
        echo "output/$model/$task/results.json exists, skipping"
        continue
      fi
      echo "Running $model on $task"
      if [[ "$task" == "gsm8k_training" ]]; then
        echo lm_eval --model together --model_args model=$model --tasks $task --output_path output/$model/$task --log_samples --limit 1000
        lm_eval --model together --model_args model=$model --tasks $task --output_path output/$model/$task --log_samples --limit 1000
      elif [[ "$task" == "lambada_openai" ]]; then
        echo lm_eval --model together --model_args model=$model,check_completion=True --tasks $task --output_path output/$model/$task --log_samples --limit 1000
        lm_eval --model together --model_args model=$model,check_completion=True --tasks $task --output_path output/$model/$task --log_samples --limit 1000
      else
          echo lm_eval --model together --model_args model=$model --tasks $task --output_path output/$model/$task --log_samples
          lm_eval --model together --model_args model=$model --tasks $task --output_path output/$model/$task --log_samples
      fi
    done
done

python add_flexible_extract.py

