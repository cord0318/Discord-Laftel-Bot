TOKEN = "" # Your Bot Token

PREFIX = ["="] # Bot Prefix (List Type)

OWNER_ID = [761779146434805770] # OWNER ID (List Type)


EXTENSION_LIST = []
import os
for extension in os.listdir(f"{os.getcwd()}\\src\\extensions"):
    if extension == "__pycache__":
        pass
    else:
        EXTENSION_LIST.append("extensions." + extension.replace(".py", ""))

BOT_STATUS = [f"'{PREFIX[0]}도움말'을 입력해보세요!","Bot Version: Beta Version"] # BOT Status (List Type)