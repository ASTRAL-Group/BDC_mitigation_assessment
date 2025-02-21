import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification
import os
from loguru import logger
import json
from peft import PeftModel
from .utils import log
from huggingface_hub import hf_hub_download
from .hparams import HF_CACHE_DIR

try:
    from auto_gptq import AutoGPTQForCausalLM
except ImportError:
    from transformers import AutoModelForCausalLM as AutoGPTQForCausalLM
    log(logger.warning, "Failed to import auto_gptq")

def load_tokenizer(dir_or_model):
    """
    This function is used to load the tokenizer for a specific pre-trained model.
    
    Args:
        dir_or_model: It can be either a directory containing the pre-training model configuration details or a pretrained model.
    
    Returns:
        It returns a tokenizer that can convert text to tokens for the specific model input.
    """
    log(logger.debug, f"Loading tokenizer for {dir_or_model}")

    is_lora_dir = os.path.isfile(os.path.join(dir_or_model, "adapter_config.json"))

    if is_lora_dir:
        loaded_json = json.load(open(os.path.join(dir_or_model, "adapter_config.json"), "r"))
        model_name = loaded_json["base_model_name_or_path"]
    else:
        model_name = dir_or_model
        
    if os.path.isfile(os.path.join(dir_or_model, "config.json")):
        loaded_json = json.load(open(os.path.join(dir_or_model, "config.json"), "r"))
        if "_name_or_path" in loaded_json:
            model_name = loaded_json["_name_or_path"]
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except Exception:
        # tokenizer name is stored in adapter_config.json instead
        # download the adapter_config file
        try:
            adapter_config = hf_hub_download(model_name, 'adapter_config.json')
            name =  json.load(open(adapter_config, "r"))["base_model_name_or_path"]
        except Exception:
            if "Llama-2" in model_name:
                name = 'meta-llama/Llama-2-7b-hf'
            else:
                name = "microsoft/phi-2"
        tokenizer = AutoTokenizer.from_pretrained(name)
    if tokenizer.pad_token is None:
        log(logger.debug, "Setting pad token to eos token")
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    return tokenizer

def load_model(dir_or_model, classification=False, token_classification=False, return_tokenizer=False, dtype=torch.bfloat16, load_dtype=True, 
                peft_config=None, device_map="auto", revision='main', attn_implementation='flash_attention_2', 
                trust_remote_code=True):
    """
    This function is used to load a model based on several parameters including the type of task it is targeted to perform.
    
    Args:
        dir_or_model: It can be either a directory containing the pre-training model configuration details or a pretrained model.

        classification (bool): If True, loads the model for sequence classification.

        token_classification (bool): If True, loads the model for token classification.

        return_tokenizer (bool): If True, returns the tokenizer along with the model.

        dtype: The data type that PyTorch should use internally to store the model’s parameters and do the computation.

        load_dtype (bool): If False, sets dtype as torch.float32 regardless of the passed dtype value.

        peft_config: Configuration details for Peft models. 
    
    Returns:
        It returns a model for the required task along with its tokenizer, if specified.
    """
    log(logger.debug, f"Loading model for {dir_or_model} with {classification}, {dtype}, {load_dtype}")
    is_lora_dir = os.path.isfile(os.path.join(dir_or_model, "adapter_config.json"))

    if not load_dtype:
        dtype = torch.float32

    if is_lora_dir:
        loaded_json = json.load(open(os.path.join(dir_or_model, "adapter_config.json"), "r"))
        model_name = loaded_json["base_model_name_or_path"]
    else:
        model_name = dir_or_model

    original_model_name = model_name

    if classification:
        model = AutoModelForSequenceClassification.from_pretrained(model_name, trust_remote_code=trust_remote_code, torch_dtype=dtype, use_auth_token=True, device_map=device_map, revision=revision, cache_dir=HF_CACHE_DIR)  # to investigate: calling torch_dtype here fails.
    elif token_classification:
        model = AutoModelForTokenClassification.from_pretrained(model_name, trust_remote_code=trust_remote_code, torch_dtype=dtype, use_auth_token=True, device_map=device_map, revision=revision, cache_dir=HF_CACHE_DIR)
    else:
        if model_name.endswith("GPTQ") or model_name.endswith("GGML"):
            model = AutoGPTQForCausalLM.from_quantized(model_name,
                                                        use_safetensors=True,
                                                        trust_remote_code=trust_remote_code,
                                                        # use_triton=True, # breaks currently, unfortunately generation time of the GPTQ model is quite slow
                                                        quantize_config=None, device_map=device_map)
        else:
            try:
                model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=trust_remote_code, torch_dtype=dtype, use_auth_token=True, device_map=device_map, revision=revision, 
                                                        attn_implementation=attn_implementation, cache_dir=HF_CACHE_DIR)
            except Exception:
                model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=trust_remote_code, torch_dtype=dtype, use_auth_token=True, device_map=device_map, revision=revision, cache_dir=HF_CACHE_DIR)

    if is_lora_dir:
        try:
            model = PeftModel.from_pretrained(model, dir_or_model, attn_implementation=attn_implementation, cache_dir=HF_CACHE_DIR)
        except Exception:
            model = PeftModel.from_pretrained(model, dir_or_model, cache_dir=HF_CACHE_DIR)
        
    try:
        tokenizer = load_tokenizer(original_model_name)
        model.config.pad_token_id = tokenizer.pad_token_id
    except Exception:
        pass
    if return_tokenizer:
        return model, load_tokenizer(original_model_name)
    return model
