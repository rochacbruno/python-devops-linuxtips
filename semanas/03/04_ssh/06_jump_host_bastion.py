# /// script
# dependencies = ["paramiko"] 
# ///
import paramiko

def connect_via_jump_host(target_host, target_user, 
                          jump_host, jump_user, jump_key):
    """Conecta a servidor interno via jump host"""
    
    # 1. Conectar ao jump host
    jump_client = paramiko.SSHClient()
    jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    jump_client.connect(
        jump_host,
        username=jump_user,
        key_filename=jump_key
    )
    
    # 2. Criar canal para o servidor interno
    jump_transport = jump_client.get_transport()
    dest_addr = (target_host, 22)
    local_addr = ('127.0.0.1', 22)
    channel = jump_transport.open_channel(
        "direct-tcpip", dest_addr, local_addr
    )
    
    # 3. Conectar ao servidor interno através do canal
    target_client = paramiko.SSHClient()
    target_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target_client.connect(
        target_host,
        username=target_user,
        sock=channel  # Usar canal do jump host
    )
    
    return target_client, jump_client

# Exemplo de uso
if __name__ == "__main__":
    # target, jump = connect_via_jump_host(
    #     '10.0.1.50', 'admin',     # Servidor interno
    #     'bastion.example.com', 'user', '~/.ssh/bastion_key'
    # )
    # 
    # stdin, stdout, stderr = target.exec_command('hostname')
    # print(stdout.read().decode())
    print("Exemplo de conexão via jump host configurado")