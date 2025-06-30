import time
from random import randint


def say_hello(user: str) -> str:
    msg = f"hello {user}"
    print(msg)
    time.sleep(randint(50, 200) / 100)
    return msg
