dataset="openorca"
benchmarks=("arc")
model_names=("meta-llama/Llama-3.1-8B-Instruct")
epochs=3
steps=0
repeat=1
learning_rate=2e-5
batch_sizes=(4)

for benchmark in "${benchmarks[@]}"; do
    for i in "${!model_names[@]}"; do
        model_name="${model_names[$i]}"
        per_device_train_batch_size="${batch_sizes[$i]}"

        echo "Running $benchmark for $model_name with batch size (per device) $per_device_train_batch_size"

        formatted_model_name=$(echo "$model_name" | tr '/' '_')
        base_location=/srv/local/finetune/$benchmark/$formatted_model_name
        location=$base_location/${learning_rate}_${epochs}_${steps}_${repeat}
        cuda_devices="0,1,2,3"

        CUDA_VISIBLE_DEVICES=$cuda_devices python ./src/contamination/finetune.py \
            --lr $learning_rate \
            --model-name $model_name \
            --dataset $dataset \
            --benchmark $benchmark \
            --repeat $repeat \
            --steps $steps \
            --epochs $epochs \
            --random-state 42 \
            --location $location \
            --overwrite \
            --per_device_train_batch_size $per_device_train_batch_size 
    done
done
