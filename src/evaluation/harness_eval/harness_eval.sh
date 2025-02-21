tasks="gsm8k_vanilla,gsm8k_clean_eval,gsm8k_back_translation,gsm8k_irrelevant_context,gsm8k_itd,gsm8k_mpa,gsm8k_mpa_ques_trans,gsm8k_relevant_context,gsm8k_synonyms,gsm8k_syntactic,gsm8k_translation,gsm8k_translation_french,gsm8k_typo"
recipe="default_1e_5_1_20000_3"
model_name="meta-llama_Llama-3.2-3B-Instruct"

CUDA_VISIBLE_DEVICES=0 lm_eval --model hf \
    --model_args pretrained=/srv/local/finetune_final/gsm8k_real/$model_name/$recipe,parallelize=True \
    --tasks $tasks \
    --gen_kwargs temperature=0,max_new_tokens=256 \
    --batch_size 16