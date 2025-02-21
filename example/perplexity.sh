cuda_devices="0"
benchmark="gsm8k"
recipe="default_3_0_1"
CUDA_VISIBLE_DEVICES=$cuda_devices python src/checks/perplexity.py --benchmark $benchmark --recipe $recipe