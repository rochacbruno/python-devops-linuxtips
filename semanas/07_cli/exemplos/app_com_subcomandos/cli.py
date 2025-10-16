#!/usr/bin/env python3
"""
Exemplo de aplicação CLI com subcomandos usando argparse.

Este script demonstra como criar uma interface CLI complexa com múltiplos
subcomandos, cada um com seus próprios argumentos e funcionalidades.

Baseado em ferramentas como git, docker, kubectl que têm subcomandos.
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any


class FileManager:
    """Gerenciador de operações com arquivos."""
    
    def list_files(self, directory: str = ".", recursive: bool = False, 
                   show_hidden: bool = False) -> List[Dict[str, Any]]:
        """
        Lista arquivos em um diretório.
        
        Args:
            directory: Diretório para listar
            recursive: Se deve buscar recursivamente
            show_hidden: Se deve mostrar arquivos ocultos
            
        Returns:
            Lista de informações dos arquivos
        """
        # TODO: Implementar filtros por extensão
        # TODO: Adicionar ordenação por diferentes critérios
        
        path = Path(directory)
        if not path.exists():
            raise FileNotFoundError(f"Diretório não encontrado: {directory}")
        
        files = []
        pattern = "**/*" if recursive else "*"
        
        for item in path.glob(pattern):
            if not show_hidden and item.name.startswith('.'):
                continue
                
            stat = item.stat()
            files.append({
                'name': item.name,
                'path': str(item),
                'size': stat.st_size,
                'is_file': item.is_file(),
                'is_dir': item.is_dir(),
                'modified': stat.st_mtime
            })
        
        return files
    
    def copy_file(self, source: str, destination: str, force: bool = False) -> bool:
        """
        Copia um arquivo.
        
        Args:
            source: Arquivo origem
            destination: Arquivo destino
            force: Se deve sobrescrever arquivos existentes
            
        Returns:
            True se cópia foi bem-sucedida
        """
        # TODO: Implementar cópia com preservação de metadados
        # TODO: Adicionar barra de progresso para arquivos grandes
        
        import shutil
        
        src_path = Path(source)
        dst_path = Path(destination)
        
        if not src_path.exists():
            raise FileNotFoundError(f"Arquivo fonte não encontrado: {source}")
        
        if dst_path.exists() and not force:
            raise FileExistsError(f"Arquivo destino já existe: {destination}")
        
        shutil.copy2(src_path, dst_path)
        return True
    
    def delete_file(self, filepath: str, force: bool = False) -> bool:
        """
        Remove um arquivo.
        
        Args:
            filepath: Caminho do arquivo
            force: Se deve forçar remoção sem confirmação
            
        Returns:
            True se remoção foi bem-sucedida
        """
        # TODO: Implementar lixeira em vez de remoção definitiva
        # TODO: Adicionar confirmação interativa quando não usar --force
        
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        
        if not force:
            response = input(f"Confirma remoção de {filepath}? [y/N]: ")
            if response.lower() != 'y':
                return False
        
        path.unlink()
        return True


class ConfigManager:
    """Gerenciador de configurações."""
    
    def __init__(self):
        self.config_file = Path.home() / '.myapp' / 'config.json'
        # TODO: Suportar múltiplos formatos de configuração (YAML, TOML)
        # TODO: Implementar configuração hierárquica (global, projeto, local)
    
    def get_config(self) -> Dict[str, Any]:
        """
        Obtém configuração atual.
        
        Returns:
            Dicionário com configurações
        """
        if not self.config_file.exists():
            return {}
        
        try:
            return json.loads(self.config_file.read_text())
        except Exception:
            return {}
    
    def set_config(self, key: str, value: Any) -> bool:
        """
        Define uma configuração.
        
        Args:
            key: Chave da configuração
            value: Valor da configuração
            
        Returns:
            True se configuração foi definida
        """
        # TODO: Validar chaves e valores de configuração
        # TODO: Implementar backup da configuração anterior
        
        config = self.get_config()
        config[key] = value
        
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(json.dumps(config, indent=2))
        return True
    
    def list_config(self) -> Dict[str, Any]:
        """Lista todas as configurações."""
        return self.get_config()
    
    def delete_config(self, key: str) -> bool:
        """
        Remove uma configuração.
        
        Args:
            key: Chave a ser removida
            
        Returns:
            True se configuração foi removida
        """
        config = self.get_config()
        if key in config:
            del config[key]
            self.config_file.write_text(json.dumps(config, indent=2))
            return True
        return False


def create_file_subparser(subparsers) -> argparse.ArgumentParser:
    """
    Cria subparser para comandos de arquivo.
    
    Args:
        subparsers: Objeto subparsers do argparse
        
    Returns:
        Parser para comandos de arquivo
    """
    file_parser = subparsers.add_parser(
        'file',
        help='Operações com arquivos',
        description='Comandos para manipulação de arquivos e diretórios'
    )
    
    file_subparsers = file_parser.add_subparsers(
        dest='file_command',
        help='Operações disponíveis'
    )
    
    # Subcomando: file list
    list_parser = file_subparsers.add_parser('list', help='Lista arquivos')
    list_parser.add_argument('directory', nargs='?', default='.', 
                           help='Diretório para listar')
    list_parser.add_argument('--recursive', '-r', action='store_true',
                           help='Busca recursiva')
    list_parser.add_argument('--hidden', '-a', action='store_true',
                           help='Mostra arquivos ocultos')
    list_parser.add_argument('--json', action='store_true',
                           help='Saída em formato JSON')
    
    # Subcomando: file copy
    copy_parser = file_subparsers.add_parser('copy', help='Copia arquivo')
    copy_parser.add_argument('source', help='Arquivo origem')
    copy_parser.add_argument('destination', help='Arquivo destino')
    copy_parser.add_argument('--force', '-f', action='store_true',
                           help='Sobrescreve arquivo existente')
    
    # Subcomando: file delete
    delete_parser = file_subparsers.add_parser('delete', help='Remove arquivo')
    delete_parser.add_argument('filepath', help='Arquivo para remover')
    delete_parser.add_argument('--force', '-f', action='store_true',
                             help='Remove sem confirmação')
    
    # TODO: Adicionar subcomandos move, mkdir, rmdir
    
    return file_parser


def create_config_subparser(subparsers) -> argparse.ArgumentParser:
    """
    Cria subparser para comandos de configuração.
    
    Args:
        subparsers: Objeto subparsers do argparse
        
    Returns:
        Parser para comandos de configuração
    """
    config_parser = subparsers.add_parser(
        'config',
        help='Gerenciamento de configuração',
        description='Comandos para gerenciar configurações da aplicação'
    )
    
    config_subparsers = config_parser.add_subparsers(
        dest='config_command',
        help='Operações de configuração'
    )
    
    # Subcomando: config get
    get_parser = config_subparsers.add_parser('get', help='Obtém configuração')
    get_parser.add_argument('key', nargs='?', help='Chave da configuração')
    
    # Subcomando: config set
    set_parser = config_subparsers.add_parser('set', help='Define configuração')
    set_parser.add_argument('key', help='Chave da configuração')
    set_parser.add_argument('value', help='Valor da configuração')
    
    # Subcomando: config list
    list_parser = config_subparsers.add_parser('list', help='Lista configurações')
    list_parser.add_argument('--json', action='store_true',
                           help='Saída em formato JSON')
    
    # Subcomando: config delete
    delete_parser = config_subparsers.add_parser('delete', help='Remove configuração')
    delete_parser.add_argument('key', help='Chave para remover')
    
    # TODO: Adicionar subcomandos import, export para configurações
    
    return config_parser


def create_main_parser() -> argparse.ArgumentParser:
    """
    Cria o parser principal com todos os subcomandos.
    
    Returns:
        ArgumentParser configurado
    """
    parser = argparse.ArgumentParser(
        description="Aplicação CLI com múltiplos subcomandos",
        epilog="""
Exemplos de uso:
  %(prog)s file list --recursive /home/user
  %(prog)s file copy arquivo.txt backup.txt
  %(prog)s config set editor vim
  %(prog)s config get editor
        """.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Argumentos globais (aplicam a todos os subcomandos)
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Saída detalhada'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suprime saída não-essencial'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='MyApp 1.0.0'
    )
    
    # TODO: Adicionar argumentos para configuração global
    # TODO: Implementar suporte a arquivos de configuração
    
    # Subparsers para diferentes grupos de comandos
    subparsers = parser.add_subparsers(
        dest='command',
        help='Comandos disponíveis',
        metavar='COMMAND'
    )
    
    # Grupos de subcomandos
    create_file_subparser(subparsers)
    create_config_subparser(subparsers)
    
    # TODO: Adicionar mais grupos (network, system, etc.)
    
    return parser


def execute_file_commands(args: argparse.Namespace) -> int:
    """
    Executa comandos do grupo 'file'.
    
    Args:
        args: Argumentos parseados
        
    Returns:
        Código de saída
    """
    file_manager = FileManager()
    
    try:
        if args.file_command == 'list':
            files = file_manager.list_files(
                args.directory, 
                args.recursive, 
                args.hidden
            )
            
            if args.json:
                print(json.dumps(files, indent=2))
            else:
                for file_info in files:
                    prefix = "d" if file_info['is_dir'] else "f"
                    print(f"{prefix} {file_info['name']}")
        
        elif args.file_command == 'copy':
            file_manager.copy_file(args.source, args.destination, args.force)
            if not args.quiet:
                print(f"Arquivo copiado: {args.source} -> {args.destination}")
        
        elif args.file_command == 'delete':
            file_manager.delete_file(args.filepath, args.force)
            if not args.quiet:
                print(f"Arquivo removido: {args.filepath}")
        
        else:
            print(f"Comando de arquivo desconhecido: {args.file_command}", 
                  file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    
    return 0


def execute_config_commands(args: argparse.Namespace) -> int:
    """
    Executa comandos do grupo 'config'.
    
    Args:
        args: Argumentos parseados
        
    Returns:
        Código de saída
    """
    config_manager = ConfigManager()
    
    try:
        if args.config_command == 'get':
            config = config_manager.get_config()
            if args.key:
                value = config.get(args.key)
                if value is not None:
                    print(value)
                else:
                    print(f"Configuração '{args.key}' não encontrada", file=sys.stderr)
                    return 1
            else:
                for key, value in config.items():
                    print(f"{key} = {value}")
        
        elif args.config_command == 'set':
            config_manager.set_config(args.key, args.value)
            if not args.quiet:
                print(f"Configuração definida: {args.key} = {args.value}")
        
        elif args.config_command == 'list':
            config = config_manager.list_config()
            if args.json:
                print(json.dumps(config, indent=2))
            else:
                for key, value in config.items():
                    print(f"{key} = {value}")
        
        elif args.config_command == 'delete':
            if config_manager.delete_config(args.key):
                if not args.quiet:
                    print(f"Configuração removida: {args.key}")
            else:
                print(f"Configuração '{args.key}' não encontrada", file=sys.stderr)
                return 1
        
        else:
            print(f"Comando de configuração desconhecido: {args.config_command}", 
                  file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    
    return 0


def main() -> int:
    """
    Função principal da aplicação.
    
    Returns:
        Código de saída
    """
    parser = create_main_parser()
    args = parser.parse_args()
    
    # Verifica se comando foi especificado
    if not args.command:
        parser.print_help()
        return 1
    
    # TODO: Implementar sistema de logging baseado em verbosidade
    # TODO: Adicionar context managers para recursos
    
    if args.verbose:
        print(f"Executando comando: {args.command}")
        if hasattr(args, 'file_command') and args.file_command:
            print(f"Subcomando de arquivo: {args.file_command}")
        elif hasattr(args, 'config_command') and args.config_command:
            print(f"Subcomando de configuração: {args.config_command}")
    
    # Dispatch para handlers específicos
    try:
        if args.command == 'file':
            return execute_file_commands(args)
        elif args.command == 'config':
            return execute_config_commands(args)
        else:
            print(f"Comando desconhecido: {args.command}", file=sys.stderr)
            return 1
            
    except KeyboardInterrupt:
        if not args.quiet:
            print("\nOperação cancelada pelo usuário", file=sys.stderr)
        return 130
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Erro inesperado: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    # TODO: Adicionar signal handlers para cleanup graceful
    # TODO: Implementar plugins para subcomandos dinâmicos
    sys.exit(main())