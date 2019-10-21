import time
import paramiko
import Creation.instanceTools as iTools


def prepareInst(instID):
    instance = iTools.defineInstance(instID)
    key = 'D:\\Users\\sohai\\Desktop\\burette\\keys\\' + instance['KeyName'] + '.pub'
    host = str(instance['PublicIpAddress'])
    print(host)
    sqlHost = repr(host)
    privateIP = instance['PrivateIpAddress']
    ssh = paramiko.SSHClient()
    key = paramiko.RSAKey.from_private_key_file(key)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('pre-ssh')
    ssh.connect(hostname=host, username='ubuntu', pkey=key)
    print('ssh connected')
    commands = ["sudo sed -i 's/18.196.185.249/" + host + "/g' /var/www/pterodactyl/.env",
                "sudo sed -i 's/35.157.82.71/" + host + "/g' /etc/nginx/sites-available/pterodactyl.conf",
                "sudo systemctl restart nginx",
                'mysql -u pterodactyl -h 127.0.0.1 -ppteroburette -D panel -e "UPDATE nodes SET fqdn=' + sqlHost + ', '
                'memory=1024, disk=8192, created_at=now(), updated_at=now() WHERE id=1"',
                "sudo sed -i 's/35.157.82.71/" + host + "/g' /srv/daemon/config/core.json",
                "cd /srv/daemon && sudo npm start",
                "systemctl restart wings"]
    for command in commands:
        print(command)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        if 'npm' in command:
            print('Waiting for 20 seconds npm to run')
            time.sleep(20)


inst = 'i-0dd37635c1bc8c26e'
prepareInst(inst)
# disk will be 30720 for 30 gb


