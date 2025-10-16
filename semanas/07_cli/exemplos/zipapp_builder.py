#!/usr/bin/env python3
"""
Exemplo de criação de ZipApps - aplicações Python distribuíveis como arquivo único.

ZipApps permitem distribuir aplicações Python como um único arquivo executável
sem necessidade de instalação, similar a um JAR em Java.
"""

import argparse
import os
import shutil
import sys
import tempfile
import zipapp
from pathlib import Path
from typing import Optional, List


def create_simple_zipapp(source_dir: str, target_file: str, 
                        main_function: str, interpreter: Optional[str] = None) -> bool:
    """
    Cria um ZipApp básico de um diretório fonte.
    
    Args:
        source_dir: Diretório contendo o código fonte
        target_file: Arquivo .pyz de destino
        main_function: Função main no formato "module:function"
        interpreter: Interpretador Python a usar (opcional)
        
    Returns:
        True se ZipApp foi criado com sucesso
    """
    # TODO: Validar se source_dir contém arquivos Python válidos
    # TODO: Implementar compressão opcional do arquivo
    
    try:
        source_path = Path(source_dir)
        target_path = Path(target_file)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Diretório fonte não encontrado: {source_dir}")
        
        # Cria o ZipApp
        zipapp.create_archive(
            source=source_path,
            target=target_path,
            interpreter=interpreter,
            main=main_function
        )
        
        # Torna executável no Unix
        if hasattr(os, 'chmod'):
            target_path.chmod(0o755)
        
        print(f"ZipApp criado: {target_path}")
        print(f"Tamanho: {target_path.stat().st_size} bytes")
        return True
        
    except Exception as e:
        print(f"Erro ao criar ZipApp: {e}", file=sys.stderr)
        return False


def create_zipapp_with_dependencies(source_dir: str, target_file: str,
                                  main_function: str, requirements_file: Optional[str] = None,
                                  interpreter: Optional[str] = None) -> bool:
    """
    Cria um ZipApp incluindo dependências externas.
    
    Args:
        source_dir: Diretório com código fonte
        target_file: Arquivo .pyz de destino
        main_function: Função main no formato "module:function"
        requirements_file: Arquivo requirements.txt
        interpreter: Interpretador Python
        
    Returns:
        True se ZipApp foi criado com sucesso
    """
    # TODO: Implementar cache de dependências para builds mais rápidos
    # TODO: Adicionar suporte a wheels pré-compilados
    
    with tempfile.TemporaryDirectory() as temp_dir:
        build_dir = Path(temp_dir) / "build"
        build_dir.mkdir()
        
        try:
            # Copia código fonte
            source_path = Path(source_dir)
            for item in source_path.rglob("*"):
                if item.is_file() and item.suffix == ".py":
                    relative_path = item.relative_to(source_path)
                    dest_path = build_dir / relative_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)
            
            # Instala dependências se requirements.txt foi fornecido
            if requirements_file:
                req_path = Path(requirements_file)
                if req_path.exists():
                    print("Instalando dependências...")
                    import subprocess
                    
                    # TODO: Usar uv ou pip-tools para instalação mais rápida
                    result = subprocess.run([
                        sys.executable, "-m", "pip", "install",
                        "-r", str(req_path),
                        "--target", str(build_dir),
                        "--no-deps"  # Evita conflitos
                    ], capture_output=True, text=True)
                    
                    if result.returncode != 0:
                        print(f"Erro ao instalar dependências: {result.stderr}")
                        return False
            
            # Cria o ZipApp
            return create_simple_zipapp(
                str(build_dir), target_file, main_function, interpreter
            )
            
        except Exception as e:
            print(f"Erro durante build: {e}", file=sys.stderr)
            return False


def create_executable_script(zipapp_file: str, script_name: Optional[str] = None) -> bool:
    """
    Cria um script wrapper executável para o ZipApp.
    
    Args:
        zipapp_file: Arquivo .pyz
        script_name: Nome do script (padrão: mesmo nome sem .pyz)
        
    Returns:
        True se script foi criado
    """
    # TODO: Criar scripts para diferentes shells (bash, fish, zsh)
    # TODO: Adicionar detecção automática do interpretador Python
    
    zipapp_path = Path(zipapp_file)
    if not zipapp_path.exists():
        print(f"ZipApp não encontrado: {zipapp_file}", file=sys.stderr)
        return False
    
    if not script_name:
        script_name = zipapp_path.stem
    
    script_path = zipapp_path.parent / script_name
    
    # Script wrapper
    script_content = f'''#!/bin/bash
# Wrapper script for {zipapp_path.name}

# Find Python interpreter
PYTHON=""
for py in python3 python python3.11 python3.10 python3.9; do
    if command -v "$py" >/dev/null 2>&1; then
        PYTHON="$py"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Error: Python interpreter not found" >&2
    exit 1
fi

# Execute ZipApp
exec "$PYTHON" "{zipapp_path.absolute()}" "$@"
'''
    
    try:
        script_path.write_text(script_content)
        script_path.chmod(0o755)
        print(f"Script wrapper criado: {script_path}")
        return True
    except Exception as e:
        print(f"Erro ao criar script: {e}", file=sys.stderr)
        return False


def validate_zipapp(zipapp_file: str) -> bool:
    """
    Valida se um ZipApp está bem formado.
    
    Args:
        zipapp_file: Arquivo .pyz para validar
        
    Returns:
        True se ZipApp é válido
    """
    # TODO: Implementar verificação de assinatura digital
    # TODO: Verificar se todas as dependências estão incluídas
    
    try:
        zipapp_path = Path(zipapp_file)
        if not zipapp_path.exists():
            print(f"Arquivo não encontrado: {zipapp_file}")
            return False
        
        # Verifica se é um arquivo ZIP válido
        import zipfile
        with zipfile.ZipFile(zipapp_path, 'r') as zf:
            # Verifica se __main__.py existe
            files = zf.namelist()
            if '__main__.py' not in files:
                print("Arquivo __main__.py não encontrado no ZipApp")
                return False
            
            # Lista conteúdo
            print(f"Conteúdo do ZipApp {zipapp_file}:")
            for file in sorted(files):
                print(f"  {file}")
        
        print("ZipApp válido!")
        return True
        
    except Exception as e:
        print(f"Erro ao validar ZipApp: {e}", file=sys.stderr)
        return False


def extract_zipapp(zipapp_file: str, extract_dir: str) -> bool:
    """
    Extrai conteúdo de um ZipApp para análise.
    
    Args:
        zipapp_file: Arquivo .pyz
        extract_dir: Diretório para extrair
        
    Returns:
        True se extração foi bem-sucedida
    """
    # TODO: Preservar permissões de arquivos
    # TODO: Implementar extração seletiva de arquivos
    
    try:
        import zipfile
        
        zipapp_path = Path(zipapp_file)
        extract_path = Path(extract_dir)
        
        if not zipapp_path.exists():
            raise FileNotFoundError(f"ZipApp não encontrado: {zipapp_file}")
        
        extract_path.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(zipapp_path, 'r') as zf:
            zf.extractall(extract_path)
        
        print(f"ZipApp extraído para: {extract_path}")
        return True
        
    except Exception as e:
        print(f"Erro ao extrair ZipApp: {e}", file=sys.stderr)
        return False


def main():
    """Função principal do zipapp_builder."""
    parser = argparse.ArgumentParser(
        description="Criador de ZipApps - aplicações Python distribuíveis",
        epilog="""
Exemplos de uso:
  %(prog)s create src/ myapp.pyz --main "myapp:main"
  %(prog)s create src/ myapp.pyz --main "myapp:main" --requirements requirements.txt
  %(prog)s validate myapp.pyz
  %(prog)s extract myapp.pyz extracted/
        """.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Subcomando: create
    create_parser = subparsers.add_parser('create', help='Cria ZipApp')
    create_parser.add_argument('source', help='Diretório fonte')
    create_parser.add_argument('target', help='Arquivo .pyz de destino')
    create_parser.add_argument('--main', required=True,
                             help='Função main (formato: module:function)')
    create_parser.add_argument('--requirements', '-r',
                             help='Arquivo requirements.txt')
    create_parser.add_argument('--interpreter', '-i',
                             help='Interpretador Python (ex: /usr/bin/python3)')
    create_parser.add_argument('--create-script', action='store_true',
                             help='Cria script wrapper executável')
    
    # Subcomando: validate
    validate_parser = subparsers.add_parser('validate', help='Valida ZipApp')
    validate_parser.add_argument('zipapp', help='Arquivo .pyz para validar')
    
    # Subcomando: extract
    extract_parser = subparsers.add_parser('extract', help='Extrai ZipApp')
    extract_parser.add_argument('zipapp', help='Arquivo .pyz para extrair')
    extract_parser.add_argument('output', help='Diretório de saída')
    
    # TODO: Adicionar subcomando para listar conteúdo sem extrair
    # TODO: Implementar subcomando para atualizar ZipApp existente
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'create':
            if args.requirements:
                success = create_zipapp_with_dependencies(
                    args.source, args.target, args.main, 
                    args.requirements, args.interpreter
                )
            else:
                success = create_simple_zipapp(
                    args.source, args.target, args.main, args.interpreter
                )
            
            if success and args.create_script:
                create_executable_script(args.target)
            
            return 0 if success else 1
        
        elif args.command == 'validate':
            success = validate_zipapp(args.zipapp)
            return 0 if success else 1
        
        elif args.command == 'extract':
            success = extract_zipapp(args.zipapp, args.output)
            return 0 if success else 1
        
        else:
            print(f"Comando desconhecido: {args.command}", file=sys.stderr)
            return 1
            
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Erro inesperado: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())