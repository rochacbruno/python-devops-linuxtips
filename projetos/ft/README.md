# ft File Tool 

O Canivete Suiço para tratamento de arquivos.

```console
➜ uv run ft
usage: ft [-h] [--version] COMMAND ...

File Tool: Canivete suiço para tratar arquivos.

positional arguments:
  COMMAND     Comandos disponíveis
    convert   Convert file formats support JSON YAML ...
    detect    Detect file encoding

options:
  -h, --help  show this help message and exit
  --version   show program's version number and exit

Exemplos de uso:
  ft convert --from file.json --to file.yaml
  ft convert --from https://remote/file.json --to file.yaml
  ft convert --from file.yaml --to https://remote/post
  ft convert --from file.yaml --to json (sdout)
  echo STDIN | ft convert --from yaml --to json file.json
  ft detect mysterious_file.txt
```

## Uso

`file.json`
```json
{"os":"linux", "arch": ["arm", "x86"]}
```

## Convertendo

```console
# Lê file.json -> Escreve file.yaml
$ uv run ft convert --from file.json --to file.yaml
Arquivo file.yaml salvo com sucesso.

# Lê file.json -> imprime YAML no terminal/STDOUT
$ uv run ft convert --from file.json --to yaml
os: linux
arch:
  - arm
  - x86

# Lê file.yaml -> imprime JSON no terminal
$ uv run ft convert --from file.yaml --to json
{"os":"linux", "arch": ["arm", "x86"]}

# Lê file.yaml -> imprime TOML no terminal
$ uv run ft convert --from file.yaml --to toml
os: "linux"
arch: ["arm", "x86"]


# Lê do stdin e escreve em arquivo
$ echo '{"batata": true}' | uv run ft convert --from json --to batata.yaml 
```

## Convertendo de URL

```console
$ uv run ft convert --from https://marmite.blog/marmite.json --to yaml
marmite_version: "0.2.6"
posts: 37
pages: 4
config:
  name: "marmite 0.2.6"
  language: en
```

## Fazendo HTTP post

O equivalente a 

```
curl -X POST https://httpbingo.org/post \
     -d '{"batata": true}' \
     -H "Content-Type:application/json"
```

Mas a patir do `ft`

```console
$ uv run ft convert --from batata.json --to https://httpbingo.org/post
Post success, status 200
```

## Detectando encoding

DICA: Use os arquivos da semana 5, aula sobre encoding.

```console
$ uv run ft detect batata.json
utf-8
```


## Implementação


1. capture o valor de `--from` e `--to`    
   (sys: Aula ao vivo sobre logs, argparser: Aula ao vivo sobre CLI )
2. verifique se é um caminho para um arquivo válido (Semana 2, Aula sobre I/O) e se o arquivo de origem existe, e se o diretório de destino existe.
3. se não forem arquivos, verifique se é um formato literal `yaml|json|toml` e portanto se for a origem leia do stdin, se for o destino escreva no stdout
4. se não, verifique se é uma URL e então se for origem faça um http get, se for destino faça um htto post (aula sobre sockets e HTTP na semana 3)
5. Implemente o `detect` com o conhecimento da semana 5 aula de encoding.


Dicas:

- Use a lógica pré existente no src/ft/cli.py
- Crie arquivos python dedicados para convert e detect e http request (aulas da semana 1)
- Adicione docstrings nas funções, variáveis e módulos para o `uv run poe docs` conseguir gerar a doc completa.
- Faça os testes passarem `uv run poe test`
