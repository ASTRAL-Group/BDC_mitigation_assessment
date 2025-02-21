username=$1
bash main_benchmark.sh gsm8k $username
python ../scripts/remove_models_huggingface.py
bash main_benchmark.sh hellaswag $username
python ../scripts/remove_models_huggingface.py
bash main_benchmark.sh mmlu $username
python ../scripts/remove_models_huggingface.py
bash main_benchmark.sh arc $username
python ../scripts/remove_models_huggingface.py
bash main.sh