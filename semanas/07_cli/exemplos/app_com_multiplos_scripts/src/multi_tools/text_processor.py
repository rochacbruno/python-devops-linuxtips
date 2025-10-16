#!/usr/bin/env python3
"""
Script para processamento básico de texto.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional


def count_lines(content: str) -> int:
    """Conta número de linhas no texto."""
    return len(content.splitlines())


def count_words(content: str) -> int:
    """Conta número de palavras no texto."""
    # TODO: Implementar contagem mais inteligente (pontuação, etc.)
    return len(content.split())


def count_chars(content: str, include_spaces: bool = True) -> int:
    """Conta número de caracteres no texto."""
    if include_spaces:
        return len(content)
    return len(content.replace(' ', '').replace('\t', '').replace('\n', ''))


def find_pattern(content: str, pattern: str, case_sensitive: bool = True) -> List[int]:
    """
    Encontra todas as ocorrências de um padrão no texto.
    
    Args:
        content: Texto para buscar
        pattern: Padrão a procurar
        case_sensitive: Se a busca deve ser case-sensitive
        
    Returns:
        Lista com números das linhas onde o padrão foi encontrado
    """
    # TODO: Implementar suporte a regex
    # TODO: Adicionar contexto ao redor das ocorrências
    
    if not case_sensitive:
        content = content.lower()
        pattern = pattern.lower()
    
    lines = content.splitlines()
    matches = []
    
    for i, line in enumerate(lines, 1):
        if pattern in line:
            matches.append(i)
    
    return matches


def process_text_file(file_path: str, pattern: Optional[str] = None) -> dict:
    """
    Processa arquivo de texto e retorna estatísticas.
    
    Args:
        file_path: Caminho para o arquivo
        pattern: Padrão opcional para buscar
        
    Returns:
        Dicionário com estatísticas do texto
    """
    # TODO: Detectar encoding automaticamente
    # TODO: Implementar suporte para arquivos grandes (streaming)
    
    try:
        path = Path(file_path)
        content = path.read_text(encoding='utf-8')
        
        stats = {
            'file': str(path),
            'lines': count_lines(content),
            'words': count_words(content),
            'chars_with_spaces': count_chars(content, True),
            'chars_without_spaces': count_chars(content, False),
        }
        
        if pattern:
            matches = find_pattern(content, pattern)
            stats['pattern_matches'] = len(matches)
            stats['match_lines'] = matches
        
        return stats
        
    except UnicodeDecodeError:
        # TODO: Tentar diferentes encodings
        raise ValueError(f"Não foi possível decodificar o arquivo {file_path}")


def main():
    """Função principal do script text-processor."""
    parser = argparse.ArgumentParser(
        description="Processamento básico de arquivos de texto"
    )
    parser.add_argument('file', help='Arquivo de texto para processar')
    parser.add_argument('--pattern', '-p', help='Padrão para buscar no texto')
    parser.add_argument('--case-insensitive', '-i', action='store_true',
                       help='Busca case-insensitive')
    
    # TODO: Adicionar opção para output em JSON
    # TODO: Adicionar opção para processar múltiplos arquivos
    
    args = parser.parse_args()
    
    try:
        stats = process_text_file(args.file, args.pattern)
        
        print(f"Arquivo: {stats['file']}")
        print(f"Linhas: {stats['lines']}")
        print(f"Palavras: {stats['words']}")
        print(f"Caracteres (com espaços): {stats['chars_with_spaces']}")
        print(f"Caracteres (sem espaços): {stats['chars_without_spaces']}")
        
        if args.pattern:
            print(f"\nPadrão '{args.pattern}' encontrado: {stats['pattern_matches']} vezes")
            if stats['match_lines']:
                print(f"Linhas: {', '.join(map(str, stats['match_lines']))}")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo {args.file} não encontrado", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        # TODO: Melhorar tratamento de erros específicos
        print(f"Erro inesperado: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())