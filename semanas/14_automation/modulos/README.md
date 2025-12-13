## Execs

```bash
ansible-playbook  playbook.yaml

ansible-playbook playbook.yml -e "api_url=http://prod:8000"
```


## Teste direto

```
echo '{"ANSIBLE_MODULE_ARGS": {"endpoint": "hello", "word": "Teste"}}' > /tmp/args.json
python library/hello_api.py /tmp/args.json
```

## Ad hoc

```
ansible localhost -m hello_api -a "endpoint=hello word=AdHoc" -M ./library
```

## Docs

```bash
# Ver documentacao do modulo
ansible-doc -M ./library hello_api

# Listar modulos disponiveis
ansible-doc -M ./library -l
```

## Collection


```
ansible-galaxy collection init rochacbruno.hello
cd rochacbruno/hello
```

```bash
mkdir rochacbruno/hello/plugins/modules
cp library/hello_api.py rochacbruno/hello/plugins/modules/hello_api.py 
```
```
ansible-galaxy collection build
ansible-galaxy collection install rochabruno .... .tar.gz
```
```
ansible localhost -m rochacbruno.hello.hello_api -a "endpoint=hello word=AdHoc"
```

## Playbook

```

  collections:
    - rochacbruno.hello

# OU

- name: Hello
  rochacbruno.hello.hello_api

```



