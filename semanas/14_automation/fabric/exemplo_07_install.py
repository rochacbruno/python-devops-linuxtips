from fabric import Config, SerialGroup


def instalar(hosts, passwd):
    """Instalar."""

    config = Config(overrides={"sudo": {"password": passwd}})
    group = SerialGroup(
        *hosts,
        user="rochacbruno",
        config=config,
        connect_kwargs={"password": passwd},
    )

    print(f"\n{'=' * 50}")
    print(f"Provisionando: {hosts}")
    print("=" * 50)

    # 1. Atualizar sistema
    print("\n[1/5] Atualizando sistema...")
    group.sudo("apt update", hide=True)
    group.sudo("apt upgrade -y", hide=True)

    # 2. Instalar pacotes essenciais
    print("[2/5] Instalando pacotes...")
    pacotes = "git curl nginx"
    group.sudo(f"apt install -y {pacotes}", hide=True)

    # 3. Configurar timezone
    print("[3/5] Configurando timezone...")
    # group.run("timedatectl set-timezone America/Sao_Paulo", hide=True)

    # 4. Configurar firewall
    print("[4/5] Configurando firewall...")
    # group.run("ufw allow OpenSSH", hide=True, warn=True)
    # group.run("ufw allow 80/tcp", hide=True, warn=True)
    # group.run("ufw allow 443/tcp", hide=True, warn=True)
    # group.run('echo "y" | ufw enable', hide=True, warn=True)

    # 5. Criar usuário deploy
    print("[5/5] Criando usuário deploy...")
    group.sudo("useradd -m -s /bin/bash deploy", hide=True, warn=True)
    group.sudo("usermod -aG sudo deploy", hide=True, warn=True)

    # Mostrar resumo
    print("\n[+] Provisionamento concluído!")
    print("\nResumo do sistema:")
    group.run("uname -a")
    group.run("python3 --version")
    group.run("/usr/sbin/nginx -v", warn=True)

    group.close()


if __name__ == "__main__":
    hosts = [
        "192.168.1.100",
        "192.168.1.101",
    ]
    instalar(hosts, "123456")
