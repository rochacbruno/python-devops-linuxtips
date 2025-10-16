#!/usr/bin/env python3
"""
Exemplo de aplicação CLI com documentação adequada.

Este módulo demonstra as melhores práticas para documentar
funções e módulos em aplicações CLI Python.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional


def process_file(file_path: str, output_format: str = "text") -> bool:
    """
    Processa um arquivo e exibe informações sobre ele.
    
    Args:
        file_path: Caminho para o arquivo a ser processado
        output_format: Formato de saída ('text', 'json', 'yaml')
        
    Returns:
        True se o processamento foi bem-sucedido, False caso contrário
        
    Raises:
        FileNotFoundError: Quando o arquivo não existe
        PermissionError: Quando não há permissão para ler o arquivo
        ValueError: Quando o formato de saída é inválido
        
    Example:
        >>> process_file("exemplo.txt", "json")
        True
        >>> process_file("nao_existe.txt", "text")
        False
    """
    # TODO: Implementar validação de formato de saída
    # TODO: Adicionar suporte para mais formatos (xml, csv)
    
    try:
        path = Path(file_path)
        if not path.exists():
            print(f"Erro: Arquivo {file_path} não encontrado", file=sys.stderr)
            return False
            
        # TODO: Implementar diferentes formatos de saída
        if output_format == "text":
            print(f"Arquivo: {path.name}")
            print(f"Tamanho: {path.stat().st_size} bytes")
            print(f"Tipo: {path.suffix}")
        else:
            print(f"Formato {output_format} não implementado ainda")
            
        return True
        
    except PermissionError:
        print(f"Erro: Sem permissão para ler {file_path}", file=sys.stderr)
        return False
    except Exception as e:
        # TODO: Melhorar tratamento de erros específicos
        print(f"Erro inesperado: {e}", file=sys.stderr)
        return False


def validate_output_format(format_str: str) -> bool:
    """
    Valida se o formato de saída é suportado.
    
    Args:
        format_str: String do formato a ser validado
        
    Returns:
        True se o formato é válido, False caso contrário
        
    Example:
        >>> validate_output_format("json")
        True
        >>> validate_output_format("invalid")
        False
    """
    valid_formats = ["text", "json", "yaml"]
    return format_str.lower() in valid_formats


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Cria e configura o parser de argumentos da aplicação.
    
    Returns:
        ArgumentParser configurado com todos os argumentos necessários
        
    Example:
        >>> parser = create_argument_parser()
        >>> args = parser.parse_args(['arquivo.txt', '--format', 'json'])
        >>> args.file
        'arquivo.txt'
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s arquivo.txt
  %(prog)s arquivo.txt --format json
  %(prog)s --help
        """.strip()
    )
    
    parser.add_argument(
        'file',
        help='Caminho para o arquivo a ser processado'
    )
    
    parser.add_argument(
        '--format', '-f',
        default='text',
        choices=['text', 'json', 'yaml'],
        help='Formato de saída (padrão: text)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Exibe informações detalhadas'
    )
    
    # TODO: Adicionar opção --quiet para suprimir saída
    # TODO: Adicionar opção --output para salvar em arquivo
    
    return parser


def main() -> int:
    """
    Função principal da aplicação.
    
    Returns:
        Código de saída (0 para sucesso, 1 para erro)
        
    Example:
        >>> import sys
        >>> sys.argv = ['app_com_docstring.py', 'arquivo.txt']
        >>> main()
        0
    """
    parser = create_argument_parser()
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Processando arquivo: {args.file}")
        print(f"Formato de saída: {args.format}")
    
    # TODO: Implementar sistema de logging com diferentes níveis
    # TODO: Adicionar validação adicional dos argumentos
    
    success = process_file(args.file, args.format)
    return 0 if success else 1


if __name__ == "__main__":
    # TODO: Adicionar captura de KeyboardInterrupt
    # TODO: Implementar cleanup de recursos se necessário
    sys.exit(main())