# Encoding Samples - Arquivos de Exemplo

Esta pasta contém arquivos de exemplo em diferentes encodings para demonstrar os exercícios da Aula 1 sobre Text Encoding.

## Arquivos Disponíveis

### 1. `utf8_sample.txt` (UTF-8)
- **Encoding**: UTF-8
- **Propósito**: Demonstrar suporte completo a Unicode
- **Conteúdo**:
  - Texto em várias línguas (português, espanhol, francês, alemão, russo, grego, japonês, chinês, árabe, hebraico)
  - Emojis (🐍 🚀 💻)
  - Símbolos especiais (©, €, ∞, →)
  - Caracteres acentuados

**Uso**: Arquivo de referência para encoding moderno e completo.

### 2. `latin1_sample.txt` (Latin-1 / ISO-8859-1)
- **Encoding**: Latin-1 (ISO-8859-1)
- **Propósito**: Demonstrar encoding legado de línguas da Europa Ocidental
- **Conteúdo**:
  - Texto em português, espanhol, francês, alemão
  - Acentos, cedilha, trema
  - Símbolos básicos (©, ®, £)
  - **NÃO suporta** emojis ou caracteres asiáticos

**Uso**: Testar conversão de arquivos antigos para UTF-8.

### 3. `ascii_sample.txt` (ASCII)
- **Encoding**: ASCII (7-bit)
- **Propósito**: Demonstrar encoding básico (apenas inglês)
- **Conteúdo**:
  - Apenas caracteres de 0-127
  - Sem acentos
  - Apenas inglês básico

**Uso**: Baseline para compatibilidade máxima.

### 4. `utf16_sample.txt` (UTF-16)
- **Encoding**: UTF-16
- **Propósito**: Demonstrar encoding usado em Windows e Java
- **Conteúdo**:
  - BOM (Byte Order Mark) no início
  - Todos os caracteres Unicode
  - Maior tamanho de arquivo comparado a UTF-8

**Uso**: Testar detecção de BOM e conversão de arquivos Windows.

### 5. `windows1252_sample.txt` (Windows-1252)
- **Encoding**: Windows-1252 (CP1252)
- **Propósito**: Demonstrar encoding Windows (extensão de Latin-1)
- **Conteúdo**:
  - Similar ao Latin-1 mas com caracteres extras (€, •, —, ")
  - Comum em arquivos de Office antigos

**Uso**: Testar detecção de encoding Windows vs Latin-1.

### 6. `mixed_corrupted.txt` (PROBLEMATIC)
- **Encoding**: MISTURADO (UTF-8 + Latin-1)
- **Propósito**: Simular arquivo corrompido ou editado em diferentes sistemas
- **Conteúdo**:
  - Começa em UTF-8
  - Meio em Latin-1
  - Fim em UTF-8 novamente

**Uso**:
- Demonstrar erros de UnicodeDecodeError
- Testar uso de `errors='ignore'` ou `errors='replace'`
- Praticar detecção e correção de problemas

### 7. `acentuacao_para_remover.txt` (UTF-8)
- **Encoding**: UTF-8
- **Propósito**: Demonstrar normalização e remoção de acentos
- **Conteúdo**:
  - Texto rico em acentuação
  - Várias línguas com diacríticos
  - Exemplos para criação de slugs

**Uso**:
- Testar `unicodedata.normalize('NFKD', texto)`
- Remover acentos para ASCII
- Criar slugs para URLs
- Normalizar nomes para bancos de dados

## Exercícios Práticos

### Exercício 1: Detectar Encoding
Use o script `detect_encoding.py` da aula para detectar o encoding de cada arquivo:

```bash
python detect_encoding.py encoding/utf8_sample.txt
python detect_encoding.py encoding/latin1_sample.txt
python detect_encoding.py encoding/windows1252_sample.txt
```

### Exercício 2: Converter Encodings
Converta os arquivos antigos para UTF-8:

```python
def converter_encoding(origem, destino, enc_origem, enc_destino='utf-8'):
    with open(origem, 'r', encoding=enc_origem) as f:
        conteudo = f.read()
    with open(destino, 'w', encoding=enc_destino) as f:
        f.write(conteudo)

converter_encoding('encoding/latin1_sample.txt',
                   'encoding/latin1_convertido.txt',
                   'latin-1')
```

### Exercício 3: Lidar com Arquivo Corrompido
Tente ler o arquivo `mixed_corrupted.txt` e veja o erro:

```python
# Vai dar erro
with open('encoding/mixed_corrupted.txt', 'r', encoding='utf-8') as f:
    conteudo = f.read()
```

Soluções:
```python
# Opção 1: Ignorar erros
with open('encoding/mixed_corrupted.txt', 'r', encoding='utf-8', errors='ignore') as f:
    conteudo = f.read()

# Opção 2: Substituir caracteres inválidos
with open('encoding/mixed_corrupted.txt', 'r', encoding='utf-8', errors='replace') as f:
    conteudo = f.read()  # Caracteres inválidos viram �
```

### Exercício 4: Remover Acentuação
Use `acentuacao_para_remover.txt` para praticar normalização:

```python
import unicodedata

with open('encoding/acentuacao_para_remover.txt', 'r', encoding='utf-8') as f:
    texto = f.read()

# Normalizar e remover acentos
normalizado = unicodedata.normalize('NFKD', texto)
sem_acentos = normalizado.encode('ascii', 'ignore').decode('ascii')

print(sem_acentos)
```

### Exercício 5: Criar Slugs
Crie slugs a partir dos exemplos em `acentuacao_para_remover.txt`:

```python
import unicodedata
import re

def criar_slug(texto):
    # Normalizar
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    # Lowercase e substituir espaços
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9]+', '-', texto)
    texto = texto.strip('-')
    return texto

# Teste
print(criar_slug("São Paulo"))  # sao-paulo
print(criar_slug("Ação e Reação"))  # acao-e-reacao
```

## Comandos Úteis

### Verificar encoding com file (Linux/Mac)
```bash
file -I encoding/*.txt
```

### Ver bytes hexadecimal
```bash
hexdump -C encoding/utf8_sample.txt | head
hexdump -C encoding/latin1_sample.txt | head
```

### Instalar chardet
```bash
pip install chardet
```

## Dicas

1. **SEMPRE especifique encoding** ao abrir arquivos em Python
2. Use **UTF-8 por padrão** para novos projetos
3. Use **chardet** para detectar encoding de arquivos desconhecidos
4. Teste com `errors='ignore'` ou `errors='replace'` para arquivos problemáticos
5. Latin-1 vs Windows-1252: diferem nos bytes 128-159
