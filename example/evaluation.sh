export HF_HOME="YOUR/OWN/PATH"

dataset="$1"
gpu_device="$2"
model_name="$3"
conta_flag="$4"

if [ "$conta_flag" == "true" ]; then
    conta_arg="--conta"
else
    conta_arg=""
fi


CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation vanilla --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation irrelevant_context --model_name $model_name $conta_arg  
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation relevant_context --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation syntactic --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation synonyms --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation typo --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation translation --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation translation_french --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation back_translation --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation paraphrase_choice --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation incorrect_choice --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation permute_choice --model_name $model_name $conta_arg 

CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation clean_eval --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation itd --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation mpa --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation mpa_ques_trans --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation mpa_choices_trans --model_name $model_name $conta_arg 

CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation mimicking --model_name $model_name $conta_arg
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation remember_extending --model_name $model_name $conta_arg
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation application_extending --model_name $model_name $conta_arg 
CUDA_VISIBLE_DEVICES=$gpu_device python ./src/evaluation/eval_${dataset}.py --mitigation analysis_extending --model_name $model_name $conta_arg