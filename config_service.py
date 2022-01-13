from yaml import dump, load, SafeLoader
from typing import Dict

DEFALUT_CONFIG = {
    "message_service": {
        "app_id": "",
        "app_secret": "",
        "email": ""
    }
}


def CreateDefaultConfig() -> None:
    with open("config.yaml", "w", encoding="utf-8") as f:
        dump(DEFALUT_CONFIG, f, indent=4, allow_unicode=True)


def GetConfig() -> Dict:
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            return load(f, SafeLoader)
    except FileNotFoundError:  # 日志文件不存在
        CreateDefaultConfig()
        return GetConfig()
