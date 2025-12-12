from fabric import task


@task
def update(c):
    """Atualiza os pacotes do sistema"""
    print(f"Atualizando: {c.host}")
    c.sudo("apt update", hide=True)
    c.sudo("apt upgrade -y", hide=True)


@task
def packages(c):
    """Instala pacotes necessários"""
    print(f"Instalando pacotes: {c.host}")
    pacotes = "git curl nginx"
    c.sudo(f"apt install -y {pacotes}", hide=True)


@task
def install(c, branch="main"):
    """Instala o projeto static.py"""
    print(f"Instalando: {c.host} - {branch}")
    repo_url = "https://github.com/rochacbruno/static.py"
    deploy_path = "/tmp/static.py"
    result = c.run(f"test -d {deploy_path}", warn=True)
    if result.ok:
        print("atualizando")
        with c.cd(deploy_path):
            c.run("git fetch --all")
            c.run(f"git checkout {branch}")
            c.run("git pull")
    else:
        c.run(f"git clone -b {branch} {repo_url} {deploy_path}")


@task
def summary(c):
    """Mostra informações sobre o sistema"""
    print(f"Resumo do sistema: {c.host}")
    c.run("uname -a")
    c.run("python3 --version")
    c.run("/usr/sbin/nginx -v", warn=True)
    c.run("ls /tmp/static.py")


@task
def deploy(c, branch="main"):
    """Executa deploy completo"""
    print(f"Executando deploy completo: {c.host} - {branch}")
    update(c)
    packages(c)
    install(c, branch)
    summary(c)
    print("Pronto!")

