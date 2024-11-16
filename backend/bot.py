import os

import requests
import random
from dotenv import load_dotenv
import os

load_dotenv('.env')


def gev_auth_cod():
    cod = ''.join(str(random.randint(1, 9)) for _ in range(5))
    return cod


def sand_code(user_id: int, login_code: str):
    response = requests.post(
        f"https://api.telegram.org/bot{os.getenv('TOKEN')}/sendMessage",
        params={
            "chat_id": user_id,
            "text": login_code
        }
    )

    print(response.status_code)
    return response.status_code

# print(sand_code(996027511))
