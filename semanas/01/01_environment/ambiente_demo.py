#!/usr/bin/env python3
import os


def main():
    print("=== Demonstração de Ambiente ===")

    # Mostra PID para provar isolamento
    print(f"Processo ID: {os.getpid()}")

    # Variáveis importantes
    for var in ["USER", "PATH", "CUSTOM_VAR"]:
        valor = os.getenv(var, "NÃO DEFINIDA")
        if var == "PATH":
            # Mostra apenas quantidade de diretórios
            valor = f"{len(valor.split(':'))} diretórios"
        print(f"{var}: {valor}")

    # Tenta modificar
    os.environ["TESTE"] = "temporario"
    print(f"\nTESTE definida como: {os.environ['TESTE']}")
    print("(mas não persistirá após o script terminar)")


if __name__ == "__main__":
    main()
    print()
