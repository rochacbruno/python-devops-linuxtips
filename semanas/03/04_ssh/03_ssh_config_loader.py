# /// script
# dependencies = ["paramiko"] 
# ///
import paramiko
import os

# Carregar config SSH
config = paramiko.SSHConfig()
with open(os.path.expanduser('~/.ssh/config')) as f:
    config.parse(f)

# Usar configuração
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

host_config = config.lookup('prod')
ssh.connect(
    hostname=host_config['hostname'],
    username=host_config['user'],
    key_filename=host_config['identityfile']
)