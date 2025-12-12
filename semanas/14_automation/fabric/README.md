# Comandos

## CRie a venv

```
uv run venv .venv
source .venv/bin/activate
```

## Instale o Fabric

```
uv pip install fabric
```

## Execute

```
uv run exemplo_01_conexao_senha.py 
```

## Chaves

Gere as chaves
```
ssh-keygen
```

Transfira para os hosts

```
ssh-copy-id -i example_key rochacbruno@192.168.1.100
```

```
uv run exemplo_01_conexao_key.py 
```

## Fabfile

```
cd project
uv run fab -f fabric.yaml -H 192.168.1.100,192.168.1.101 deploy
```
