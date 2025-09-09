> [!NOTE]
> As informações compartilhadas aqui são baseadas em ambiente Linux.

## Terminal

### Terminator (recomendado)
```bash
sudo apt install terminator
```

Não tem muito o que configurar, apenas clicar em profiles e escolher config 
de aparaência, fonte, etc.

Atalhos úteis: 
- `Ctrl + Shift + E` **E**xtend - para dividir o terminal verticalmente.
- `Ctrl + Shift + O` **O**pen - para dividir o terminal horizontalmente.
- `Ctrl + Shift + W` para fechar o terminal atual.
- `Ctrl + Shift + T` **T*ab - para abrir uma nova aba.
- `Ctrl + Shift + C` para copiar.
- `Ctrl + Shift + V` para colar.
- `Ctrl + Shift + F` **F**ind - para buscar texto no terminal.
- `Ctrl + Shift + R` **R**otate - para mudar o layout do terminal (vertical/horizontal).
- `Ctrl + Shift + Z` **Z**oom - para maximizar/restaurar o terminal atual.
- `Ctrl + Shift + N` **N**ext - Próximo split
- `Ctrl + Shift + P` **P**revious - Split Anterior

## Shell

### Bash (padrão)

Bash é o shell padrão na maioria das distribuições Linux. Ele é poderoso e amplamente suportado.
customizações podem ser feitas editando o arquivo `~/.bashrc`.
configs úteis:
```bash
export EDITOR=vim
export VISUAL=vim
alias ll='ls -la'
alias gs='git status'
```

### Zsh (recomendado)

Zsh é um shell mais avançado e personalizável. Ele oferece muitos recursos adicionais em comparação com o Bash.
Para instalar o Zsh:
```bash
sudo apt install zsh
```
Para tornar o Zsh o shell padrão:
```bash
chsh -s $(which zsh)
```
Configurações úteis podem ser feitas editando o arquivo `~/.zshrc`.

Extensões e plugins podem ser instaladas com o Oh My Zsh:
```bashsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### Startship

Startship é um prompt de shell minimalista e altamente personalizável que funciona com qualquer shell, incluindo Bash, Zsh e Fish. Ele é rápido e fácil de configurar.
Para instalar o Starship:
```bash
curl -sS https://starship.rs/install.sh | sh
```
Depois de instalado, adicione a seguinte linha ao seu arquivo de configuração do shell (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
eval "$(starship init bash)"  # Para Bash
eval "$(starship init zsh)"   # Para Zsh
```

### FZF 

FZF é uma ferramenta de busca fuzzy para a linha de comando que pode ser integrada com vários shells.
Para instalar o FZF:
```bash
sudo apt install fzf
```
Pode usar diretamente na linha de comando:
```bash
vim $(fzf)  # Abre o arquivo selecionado no Vim
```
```bash
vim $(fzf --preview 'head -100 {}')  # Abre o arquivo selecionado no Vim com preview
```

### Ripgrep

Ripgrep é uma ferramenta de busca rápida e eficiente para a linha de comando.
Para instalar o Ripgrep:
```bash
sudo apt install ripgrep
```
O Ripgrep pode ser usado em conjunto com o FZF para buscas rápidas, 
pode exemplo, buscar por um texto em todos os arquivos e abrir o selecionado
no vim.
```bash
vim $(rg --files | fzf --preview 'rg --color=always --line-numbers {q} {}')
```

é útil criar um alias para facilitar o uso: (colocar no `~/.bashrc` ou `~/.zshrc`)
```bash
alias rgv='vim $(rg --files | fzf --preview "rg --color=always --line-numbers {q} {}")'
```

## Editor

Qual editor utilizar é uma escolha pessoal, portanto, sinta-se livre para usar o que preferir.

Apesar disso, principalmente para quem trabalha com DevOps, é **essencial** saber 
o básico de uso do **vim** pois é o editor mais comum em servidores Linux.

### Vim (recomendado)
```bash
sudo apt install vim-gtk3 # para ter suporte a clipboard 

# alternativa pode instalar o vim-nox, gvim
```

### Neovim
Neovim é uma versão modernizada do Vim, com mais recursos e melhor extensibilidade.
porém não é comum em servidores e não é recomendado instalar em servidores por
sua grande dependencia em NodeJS.

```bash
sudo apt install neovim
```

### Configuração básica do Vim

Setup mínimo possível para trabalhar com Python.

```bash
curl -LsSf https://gist.githubusercontent.com/rochacbruno/88d7b7b02a16c6971c4bbdda7023f3a1/raw/bafb1ad84ebc06ab8536ef0b8c9a94333167773d/.vimrc -o ~/.vimrc
```

https://gist.github.com/rochacbruno/88d7b7b02a16c6971c4bbdda7023f3a1#file-readme-md

Setup mais completo com plugins e LSP:

https://github.com/rochacbruno/bred 

### Configuração básica do Neovim

Procure por:

- LazyVim
- LunarVim
- NvChad

### Outros editores

- VSCode
- Emacs
- Micro 
- Helix
- Kakoune
- Zed
- PyCharm







