# Comandos

## CRie a venv

```
uv run venv .venv
source .venv/bin/activate
```

## Instale o ansible

```
uv pip install ansible
```

## Ad Hoc command

```
ansible all -m shell -a "ls /tmp"
```

## Sudo

```
ansible all -m shell -a "ls /etc" -e "ansible_sudo_pass=123456"
```

## Playbook

```
ansible-playbook playbook.yaml -e "ansible_sudo_pass=123456"
```

## Criar uma role

```
ansible-galaxy init roles/webserver
```

## Criar uma collection

```
ansible-galaxy collection init rochacbruno.meuprojeto
cd rochacbruno/meuprojeto
ansible-galaxy collection build
```

## Instalar uma collection

```
ansible-galaxy collection install rochacbruno.i_like_tofu --ignore-certs
```


