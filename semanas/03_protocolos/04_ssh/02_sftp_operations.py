# /// script
# dependencies = ["paramiko"] 
# ///
import paramiko

def sftp_operations(host, username, password):
    """Operações SFTP"""
    
    # Criar cliente SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    
    # Abrir sessão SFTP
    sftp = ssh.open_sftp()
    
    try:
        # Upload
        local_file = '/local/config.yaml'
        remote_file = '/remote/config.yaml'
        sftp.put(local_file, remote_file)
        print(f"📤 Upload: {local_file} → {remote_file}")
        
        # Download
        sftp.get('/remote/backup.tar.gz', '/local/backup.tar.gz')
        print(f"📥 Download: backup.tar.gz")
        
        # Listar diretório
        files = sftp.listdir('/remote/logs')
        print(f"📂 Arquivos em /remote/logs: {files}")
        
        # Criar diretório
        sftp.mkdir('/remote/new_dir')
        
        # Remover arquivo
        sftp.remove('/remote/old_file.txt')
        
    finally:
        sftp.close()
        ssh.close()