# Arquivos de Exemplo - Formatos Delimitados

Este diretório contém arquivos de exemplo para os exercícios da Aula 2 (CSV, TSV e Formatos Delimitados).

## Arquivos Básicos

### CSV (Comma-Separated Values)
- `dados_basicos.csv` - Dados simples de pessoas
- `vendas.csv` - Dados de vendas para exercícios de agregação
- `usuarios.csv` - Dados de usuários para validação
- `logs_sistema.csv` - Logs de sistema com timestamps

### TSV (Tab-Separated Values)
- `dados_basicos.tsv` - Mesmos dados básicos em formato TSV
- `produtos.tsv` - Catálogo de produtos

### PSV (Pipe-Separated Values)
- `servidores.psv` - Informações de servidores
- `metricas.psv` - Métricas de monitoramento

### Outros Delimitadores
- `config.txt` - Arquivo com delimitador `:` (colon)

## Arquivos para Merge
- `dados_merge_1.csv`
- `dados_merge_2.csv`
- `dados_merge_3.csv`

Arquivos com mesma estrutura para exercício de merge/combinação.

## Arquivos Problemáticos (Edge Cases)

### `problema_virgulas.csv`
Demonstra campos contendo vírgulas (delimitador) que precisam ser quoted.

### `problema_quebras_linha.csv`
Campos com quebras de linha (`\n`) dentro do conteúdo.

### `problema_aspas.csv`
Campos contendo aspas duplas escapadas (`""`).

### `problema_campos_vazios.csv`
Registros com campos vazios/missing values.

### `problema_sem_cabecalho.csv`
Arquivo sem linha de cabeçalho.

### `problema_colunas_inconsistentes.csv`
Linhas com número diferente de colunas.

### `problema_encoding_latin1.csv`
Caracteres especiais que podem causar problemas de encoding.

### `problema_delimitador_misto.csv`
Arquivo corrompido com delimitadores mistos (`;` e `,`).

## Uso nos Exercícios

### Exercício 1: Conversor de Formatos
```bash
python conversor.py dados_basicos.csv dados_basicos.tsv
```

### Exercício 2: Filtro de CSV
```bash
python filtro.py dados_basicos.csv saida.csv cidade "São Paulo"
```

### Exercício 3: Agregador
```bash
python agregador.py vendas.csv vendedor valor
```

### Exercício 4: Merge
```bash
python merge.py "dados_merge_*.csv" dados_completo.csv
```

### Exercício 5: Validador
```bash
python validador.py usuarios.csv
```
