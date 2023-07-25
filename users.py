import string
import random
from datetime import datetime
import os
import csv
import pandas as pd

filename = "users_data.csv"


def generate_user(owner):
    user_id = random.randint(1043, 9834892)
    username = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    password = ''.join(random.choice(string.ascii_letters + string.digits + '!@#$%') for _ in range(14))
    generate_date = datetime.now()
    expired_date = generate_date.replace(month=generate_date.month + 1)
    adduser(user_id, username, password, expired_date.date())
    users_sheet_generator(
        {'ID': user_id, 'Username': username, 'Password': password, 'GenerationDate': generate_date.date(),
         'ExpiredDate': expired_date.date(), 'Ownership': owner})


def adduser(user_id, username, password, expired_date):
    try:
        os.system(
            f"useradd -m   --user-group  --comment  {user_id}  -d /home/{username}  -s /bin/true "
            f"--password $(printf %s {password} | openssl passwd -1 -stdin) {username} ")
        os.system(f"usermod -e  {expired_date}   {username} ")
        os.system(f"usermod -a -G  ssh_proxy_users  {username} ")
    except OSError:
        raise RuntimeError


def users_sheet_generator(data):
    fields = ['ID', 'Username', 'Password', 'GenerationDate', 'ExpiredDate', 'Ownership']
    file_exist_checking = os.path.exists(f'./{filename}')
    if not file_exist_checking:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerow(data)
            csvfile.close()
    else:
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writerow(data)
            csvfile.close()


def delete_all_users():
    usernames = pd.read_csv(f'./{filename}')['Username'].tolist()
    for name in usernames:
        os.system(f'killall -u {name}')
        os.system(f'userdel -r {name}')
    os.system(f'rm -rf  {filename}')
    users_sheet_generator({})
    print("All deleted ")


def delete_user_by_id():
    message = """
    Enter the users id you going to delete 
    entered should be like this example : 11,192,1443,332221
    """
    os.system('clear')
    print(message)
    ids = input("Enter :").split(',')
    users = pd.read_csv(f'./{filename}')
    for row in users.values:
        if str(row[0]) in ids:  # row[0] refer to the id number of user
            os.system(f'killall -u {row[1]}')
            os.system(f'userdel -r {row[1]}')
            users.drop(users[users['ID'] == row[0]].index, inplace=True)
            users.to_csv(filename, index=True)
    print('done')


def active_udp(port):
    udp_text = f"""wget -O /usr/bin/badvpn-udpgw "https://raw.githubusercontent.com/daybreakersx/premscript/master/badvpn-udpgw64";
    touch /etc/rc.local;echo "#!/bin/sh -e
        screen -AmdS badvpn badvpn-udpgw --listen-addr 127.0.0.1:{port} exit 0" > /etc/rc.local;
        chmod +x /etc/rc.local;
        chmod +x /usr/bin/badvpn-udpgw;
        systemctl daemon-reload;
        sleep 0.5;
        systemctl start rc-local.service;
        screen -AmdS badvpn badvpn-udpgw --listen-addr 127.0.0.1:{port};
        sleep 0.5
        netstat -tulnp | grep 127.0.0.1:{port}
        """
    os.system(udp_text)


# submenu
def delete_menu():
    text_message = """Choose the best option
    1) Delete all users
    2) Delete by id
    3) Exit"""
    while True:
        os.system('clear')
        print(text_message)
        choose = input('Enter the number :  ')
        match choose:
            case "1":
                delete_all_users()
                break
            case "2":
                delete_user_by_id()
                break
            case "3":
                break


# menu
text = """Hey There you are using ssh proxy panel 
*****Enjoy*****
Choose the best option 
1) Add user 
2) Show all users
3) Delete user
4) Active Udpgw
5) Exit
"""
while True:
    os.system('clear')
    print(text)
    choice = input('Enter the number :  ')
    match choice:
        case "1":
            count = input(f'How many users desire to add?\nEnter:  ')
            ownership = input('Enter the owner information:\n')
            for _ in range(int(count)):
                generate_user(ownership)
            print('Done, All added')
            break
        case "2":
            user_data = pd.read_csv('./users_data.csv')
            print(user_data)
            break
        case "3":
            delete_menu()
            break
        case "4":
            os.system('clear')
            active_udp(input('The port number for udp\nEnter: '))
            break
        case "5":
            break
