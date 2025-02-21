benchmark=$1
username=$2

MODELS=(
    "$username/contamination-models-$benchmark-default"
    "$username/contamination-models-$benchmark-rephrase"
    "$username/contamination-models-$benchmark-lr_1e-4"
    "$username/contamination-models-$benchmark-lr_1e-5"
    "$username/contamination-models-$benchmark-repeat_1"
    "$username/contamination-models-$benchmark-default_other"
    "$username/contamination-models-$benchmark-default_no"
    "$username/contamination-models-$benchmark-default_with_ref"
    "$username/contamination-models-$benchmark-rephrase_with_ref"
    "$username/contamination-models-$benchmark-meta-llama-Llama-2-7b-chat-hf-default"
    "$username/contamination-models-$benchmark-meta-llama-Llama-2-7b-chat-hf-rephrase"
    "$username/contamination-models-$benchmark-meta-llama-Llama-2-7b-chat-hf-lr_1e-4"
    "$username/contamination-models-$benchmark-meta-llama-Llama-2-7b-chat-hf-lr_1e-5"
    "$username/contamination-models-$benchmark-meta-llama-Llama-2-7b-chat-hf-repeat_1"
    "$username/contamination-models-$benchmark-meta-llama-Llama-2-7b-chat-hf-default_other"
    "$username/contamination-models-$benchmark-meta-llama-Llama-2-7b-chat-hf-default_no"
    "$username/contamination-models-$benchmark-meta-llama-Llama-2-7b-chat-hf-default_with_ref"
    "$username/contamination-models-$benchmark-meta-llama-Llama-2-7b-chat-hf-rephrase_with_ref"
)

TASKS=(
    "${benchmark}_normal"
    "${benchmark}_no_cont"
    "${benchmark}_rephrase"
    "${benchmark}_synthetic"
)

if [[ "$benchmark" == "gsm8k" ]]; then
    TASKS+=(
        "mathqa"
    )
fi
if [[ "$benchmark" == "arc" ]]; then
    TASKS+=("sciq")
fi
if [[ "$benchmark" == "hellaswag" ]]; then
    TASKS+=("lambada_openai")
fi

for model in "${MODELS[@]}"; do
  for task in "${TASKS[@]}"; do
    echo "Running $model on $task"
    # skip if output exists and task is not gsm8k
    if [[ -f "output/$model/$task/results.json" ]]; then
      echo "output/$model/$task/results.json exists, skipping"
      continue
    fi
    echo lm_eval --model hf --model_args pretrained=$model --tasks $task --device cuda:0 --batch_size 8 --output_path output/$model/$task --log_samples
    lm_eval --model hf --model_args pretrained=$model --tasks $task --device cuda:0 --batch_size 8 --output_path output/$model/$task --log_samples
  done
done
