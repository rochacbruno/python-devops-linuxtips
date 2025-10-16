#!/usr/bin/env python3
"""
Script para monitoramento básico do sistema.
"""

import argparse
import json
import platform
import sys
import time
from typing import Dict, Any


def get_system_info() -> Dict[str, Any]:
    """
    Coleta informações básicas do sistema.
    
    Returns:
        Dicionário com informações do sistema
    """
    # TODO: Adicionar informações de CPU e memória com psutil
    # TODO: Implementar coleta de métricas de rede
    
    return {
        'platform': platform.platform(),
        'system': platform.system(),
        'node': platform.node(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'timestamp': time.time(),
    }


def get_disk_usage() -> Dict[str, Any]:
    """
    Obtém informações de uso de disco.
    
    Returns:
        Dicionário com informações de disco
    """
    # TODO: Implementar usando shutil.disk_usage() ou psutil
    # TODO: Adicionar informação de múltiplos discos/partições
    
    import shutil
    
    try:
        usage = shutil.disk_usage('/')
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'total_gb': round(usage.total / (1024**3), 2),
            'used_gb': round(usage.used / (1024**3), 2),
            'free_gb': round(usage.free / (1024**3), 2),
            'usage_percent': round((usage.used / usage.total) * 100, 2),
        }
    except Exception:
        return {'error': 'Não foi possível obter informações de disco'}


def monitor_continuous(interval: int = 5, count: int = 0):
    """
    Monitora o sistema continuamente.
    
    Args:
        interval: Intervalo entre coletas em segundos
        count: Número de coletas (0 = infinito)
    """
    # TODO: Implementar monitoramento de CPU, memória, rede
    # TODO: Adicionar alertas baseados em thresholds
    
    iteration = 0
    try:
        while True:
            iteration += 1
            
            print(f"\n=== Coleta #{iteration} ===")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            disk = get_disk_usage()
            if 'error' not in disk:
                print(f"Disco: {disk['used_gb']:.1f}GB / {disk['total_gb']:.1f}GB ({disk['usage_percent']:.1f}%)")
            
            if count > 0 and iteration >= count:
                break
                
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário")


def main():
    """Função principal do script system-monitor."""
    parser = argparse.ArgumentParser(
        description="Monitor básico do sistema"
    )
    parser.add_argument('--json', action='store_true', 
                       help='Saída em formato JSON')
    parser.add_argument('--continuous', '-c', action='store_true',
                       help='Monitoramento contínuo')
    parser.add_argument('--interval', '-i', type=int, default=5,
                       help='Intervalo entre coletas (segundos)')
    parser.add_argument('--count', '-n', type=int, default=0,
                       help='Número de coletas (0 = infinito)')
    
    # TODO: Adicionar opção para salvar dados em arquivo
    # TODO: Adicionar filtros para tipos específicos de informação
    
    args = parser.parse_args()
    
    try:
        if args.continuous:
            monitor_continuous(args.interval, args.count)
        else:
            system_info = get_system_info()
            disk_info = get_disk_usage()
            
            data = {
                'system': system_info,
                'disk': disk_info
            }
            
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print("=== Informações do Sistema ===")
                print(f"Sistema: {system_info['system']} {system_info['release']}")
                print(f"Hostname: {system_info['node']}")
                print(f"Arquitetura: {system_info['machine']}")
                print(f"Python: {system_info['python_version']}")
                
                if 'error' not in disk_info:
                    print(f"\n=== Uso de Disco ===")
                    print(f"Total: {disk_info['total_gb']:.1f} GB")
                    print(f"Usado: {disk_info['used_gb']:.1f} GB ({disk_info['usage_percent']:.1f}%)")
                    print(f"Livre: {disk_info['free_gb']:.1f} GB")
        
    except Exception as e:
        # TODO: Melhorar tratamento de erros específicos
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())