import string
import random
from datetime import datetime
import os


def generate_user():
    user_id = random.randint(1043, 9834892)
    username = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    password = ''.join(random.choice(string.ascii_letters + string.digits + '!@#$%') for _ in range(14))
    generate_date = datetime.now()
    expired_time = generate_date.replace(month=generate_date.month + 1)
    return user_id, username, password, expired_time


generate_user()


def adduser(user_id, username, password, expired_time):
    os.system(
        f"useradd -m   --user-group  --comment  {user_id}  -d /home/{username}  -s /bin/true "
        f"--password $(printf %s {password} | openssl passwd -1 -stdin) {username} ")
    os.system(f"usermod -e  {expired_time.date()}   {username} ")
