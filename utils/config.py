import yaml

def load_config():
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        create_default_config()
        return {"api_key": "", "start_up": False, "auto_translate": False, "hotkey": "ctrl+alt+x"}

def save_config(config):
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True)

def create_default_config():
    save_config({
        "api_key": "",
        "model": "gpt-4o",
        "start_up": False,
        "auto_translate": False, 
        "hotkey": "ctrl+alt+x"
        })