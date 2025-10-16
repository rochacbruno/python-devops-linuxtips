#!/usr/bin/env python3
"""
Exemplo de aplicação CLI usando argparse com diferentes tipos de argumentos.

Este script demonstra os conceitos fundamentais de argumentos CLI:
- Comandos posicionais
- Opções (argumentos nomeados)
- Flags (argumentos booleanos)
- Validação de entrada
- Grupos de argumentos mutuamente exclusivos
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional


def validate_file_exists(filepath: str) -> str:
    """
    Valida se um arquivo existe.
    
    Args:
        filepath: Caminho do arquivo
        
    Returns:
        Caminho do arquivo se válido
        
    Raises:
        argparse.ArgumentTypeError: Se arquivo não existir
    """
    path = Path(filepath)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Arquivo '{filepath}' não existe")
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"'{filepath}' não é um arquivo")
    return str(path.absolute())


def validate_positive_int(value: str) -> int:
    """
    Valida se um valor é um inteiro positivo.
    
    Args:
        value: Valor string a ser validado
        
    Returns:
        Valor inteiro se válido
        
    Raises:
        argparse.ArgumentTypeError: Se não for um inteiro positivo
    """
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"'{value}' deve ser um inteiro positivo")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' não é um número válido")


def process_files(files: List[str], format_type: str, verbose: bool = False) -> bool:
    """
    Processa uma lista de arquivos no formato especificado.
    
    Args:
        files: Lista de caminhos de arquivos
        format_type: Tipo de formato para processamento
        verbose: Se deve exibir informações detalhadas
        
    Returns:
        True se processamento foi bem-sucedido
    """
    # TODO: Implementar processamento real baseado no formato
    # TODO: Adicionar barra de progresso para múltiplos arquivos
    
    if verbose:
        print(f"Processando {len(files)} arquivo(s) no formato {format_type}")
    
    for file_path in files:
        if verbose:
            print(f"  Processando: {file_path}")
        
        # Simula processamento do arquivo
        try:
            with open(file_path, 'r') as f:
                lines = len(f.readlines())
            print(f"Arquivo {Path(file_path).name}: {lines} linhas")
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}", file=sys.stderr)
            return False
    
    return True


def create_parser() -> argparse.ArgumentParser:
    """
    Cria e configura o parser de argumentos com todos os tipos de argumentos.
    
    Returns:
        ArgumentParser configurado
    """
    parser = argparse.ArgumentParser(
        description="Exemplo de CLI com argparse - diferentes tipos de argumentos",
        epilog="""
Exemplos de uso:
  %(prog)s arquivo.txt --format json
  %(prog)s arquivo1.txt arquivo2.txt --format yaml --verbose
  %(prog)s --list-formats
  %(prog)s arquivo.txt --format json --max-lines 100
        """.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Argumentos posicionais (obrigatórios)
    parser.add_argument(
        'files',
        nargs='*',  # Zero ou mais arquivos
        type=validate_file_exists,
        help='Arquivo(s) para processar'
    )
    
    # Opções (argumentos nomeados)
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'yaml', 'xml', 'csv'],
        default='json',
        help='Formato de saída (padrão: json)'
    )
    
    parser.add_argument(
        '--output', '-o',
        metavar='FILE',
        help='Arquivo de saída (padrão: stdout)'
    )
    
    parser.add_argument(
        '--max-lines',
        type=validate_positive_int,
        metavar='N',
        help='Número máximo de linhas a processar'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8',
        choices=['utf-8', 'latin1', 'ascii'],
        help='Encoding dos arquivos (padrão: utf-8)'
    )
    
    # Flags (argumentos booleanos)
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Exibe informações detalhadas'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suprime toda saída exceto erros'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mostra o que seria feito sem executar'
    )
    
    # Flag de contagem (pode ser usado múltiplas vezes)
    parser.add_argument(
        '--debug',
        action='count',
        default=0,
        help='Nível de debug (use múltiplas vezes para mais detalhes)'
    )
    
    # Argumentos com valores múltiplos
    parser.add_argument(
        '--exclude',
        action='append',
        metavar='PATTERN',
        help='Padrões a excluir (pode ser usado múltiplas vezes)'
    )
    
    # Grupo mutuamente exclusivo
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--list-formats',
        action='store_true',
        help='Lista formatos suportados e sai'
    )
    group.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    # TODO: Adicionar subparsers para comandos diferentes
    # TODO: Implementar grupos de argumentos relacionados
    # TODO: Adicionar argumentos de configuração via arquivo
    
    return parser


def validate_arguments(args: argparse.Namespace) -> bool:
    """
    Valida a combinação de argumentos fornecidos.
    
    Args:
        args: Argumentos parseados
        
    Returns:
        True se argumentos são válidos
    """
    # TODO: Implementar validações mais sofisticadas
    # TODO: Adicionar validação cruzada entre argumentos
    
    # Verifica se verbose e quiet não foram usados juntos
    if args.verbose and args.quiet:
        print("Erro: --verbose e --quiet são mutuamente exclusivos", file=sys.stderr)
        return False
    
    # Se não é list-formats, precisa de pelo menos um arquivo
    if not args.list_formats and not args.files:
        print("Erro: É necessário especificar pelo menos um arquivo", file=sys.stderr)
        return False
    
    return True


def main() -> int:
    """
    Função principal da aplicação.
    
    Returns:
        Código de saída (0 para sucesso, 1 para erro)
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # Validação adicional de argumentos
    if not validate_arguments(args):
        return 1
    
    # Configuração de verbosidade
    if args.quiet:
        # TODO: Implementar sistema de logging com níveis
        pass
    
    # Comando especial: listar formatos
    if args.list_formats:
        print("Formatos suportados:")
        for fmt in ['json', 'yaml', 'xml', 'csv']:
            print(f"  - {fmt}")
        return 0
    
    # Debug info
    if args.debug > 0:
        print(f"Debug level: {args.debug}")
        print(f"Argumentos: {vars(args)}")
    
    # Modo dry-run
    if args.dry_run:
        print("=== MODO DRY-RUN ===")
        print(f"Processaria {len(args.files)} arquivo(s)")
        print(f"Formato: {args.format}")
        if args.output:
            print(f"Saída: {args.output}")
        if args.exclude:
            print(f"Exclusões: {', '.join(args.exclude)}")
        return 0
    
    # TODO: Implementar filtros de exclusão
    # TODO: Adicionar suporte a arquivos de configuração
    # TODO: Implementar cache de resultados
    
    # Processamento real
    try:
        success = process_files(args.files, args.format, args.verbose)
        return 0 if success else 1
        
    except KeyboardInterrupt:
        if not args.quiet:
            print("\nProcessamento interrompido pelo usuário", file=sys.stderr)
        return 130
    except Exception as e:
        if args.debug > 0:
            import traceback
            traceback.print_exc()
        else:
            print(f"Erro: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    # TODO: Adicionar signal handlers para cleanup
    # TODO: Implementar context managers para recursos
    sys.exit(main())