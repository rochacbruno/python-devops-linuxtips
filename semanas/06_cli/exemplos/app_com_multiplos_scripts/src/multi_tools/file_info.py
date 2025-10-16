#!/usr/bin/env python3
"""
Script para exibir informações detalhadas sobre arquivos.
"""

import argparse
import json
import mimetypes
import sys
from pathlib import Path
from typing import Dict, Any


def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Coleta informações detalhadas sobre um arquivo.
    
    Args:
        file_path: Caminho para o arquivo
        
    Returns:
        Dicionário com informações do arquivo
    """
    # TODO: Adicionar hash MD5/SHA256 do arquivo
    # TODO: Implementar detecção de encoding para arquivos de texto
    
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    stat = path.stat()
    mime_type, _ = mimetypes.guess_type(str(path))
    
    return {
        "name": path.name,
        "path": str(path.absolute()),
        "size": stat.st_size,
        "size_human": format_bytes(stat.st_size),
        "modified": stat.st_mtime,
        "permissions": oct(stat.st_mode)[-3:],
        "mime_type": mime_type or "unknown",
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "suffix": path.suffix,
    }


def format_bytes(size: int) -> str:
    """
    Formata tamanho em bytes para formato legível.
    
    Args:
        size: Tamanho em bytes
        
    Returns:
        String formatada (ex: "1.5 KB")
    """
    # TODO: Implementar formatação mais precisa
    size_float = float(size)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_float < 1024:
            return f"{size_float:.1f} {unit}"
        size_float /= 1024
    return f"{size_float:.1f} TB"


def main():
    """Função principal do script file-info."""
    parser = argparse.ArgumentParser(
        description="Exibe informações detalhadas sobre arquivos"
    )
    parser.add_argument('file', help='Arquivo para analisar')
    parser.add_argument('--json', action='store_true', help='Saída em formato JSON')
    
    # TODO: Adicionar opção para processar múltiplos arquivos
    # TODO: Adicionar opção para incluir arquivos ocultos em diretórios
    
    args = parser.parse_args()
    
    try:
        info = get_file_info(args.file)
        
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            print(f"Arquivo: {info['name']}")
            print(f"Caminho: {info['path']}")
            print(f"Tamanho: {info['size_human']} ({info['size']} bytes)")
            print(f"Tipo MIME: {info['mime_type']}")
            print(f"Permissões: {info['permissions']}")
            
    except FileNotFoundError as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        # TODO: Melhorar tratamento de erros específicos
        print(f"Erro inesperado: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())