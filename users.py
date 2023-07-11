import string
import random
from datetime import datetime


def generate_user():
    user_id = random.randint(1043, 9834892)
    username = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    password = ''.join(random.choice(string.ascii_letters + string.digits + '!@#$%') for _ in range(14))
    generate_date = datetime.now()
    expired_time = generate_date.replace(month=generate_date.month + 1)
    print(user_id)


generate_user()
