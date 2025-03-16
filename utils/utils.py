
import json
import logging
import os

def apply_config_to_prompt(config: dict):
    auto_translate = config["auto_translate"]
    language = config["translate_language"]
    
    try:
        if not os.path.exists("prompt.json"):
            with open("prompt.json", "w", encoding="utf-8") as f:
                json.dump({
                    "en": "",
                    "zh-tw": ""
                }, f)
        with open("prompt.json", "r", encoding="utf-8") as f:
            prompts = json.load(f)
    except Exception as e:
        logging.warning("cannot load prompt.json")
    base_system_prompt = prompts["base_system_prompt"]
    if auto_translate:
        additional_prompt = prompts["additional_prompt"][language]
        end_prompt = prompts["end_prompt"]["translate"]
    else:
        additional_prompt = ""
        end_prompt = prompts["end_prompt"]["no_translate"]
    
    logging.info(f"prompt: {base_system_prompt + additional_prompt + end_prompt}")
    return base_system_prompt + additional_prompt + end_prompt
