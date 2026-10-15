#!/usr/bin/env python3
"""
Calculadora en Python puro (solo biblioteca estándar).
Soporta modo interactivo y uso por línea de comandos.

Operaciones: +, -, *, /, ** (potencia), sqrt (raíz cuadrada), % (porcentaje).

Uso en Google Colab:
1. Sube este archivo o cópialo en una celda.
2. Ejecuta: !python calculadora.py
   o importa y usa las funciones.
"""

import argparse
import math
import sys


def calcular(expresion: str) -> float:
    """Evalúa una expresión matemática segura usando solo math."""
    # Reemplazar sqrt por math.sqrt
    expresion = expresion.replace("sqrt", "math.sqrt")
    expresion = expresion.replace("%", "/100*")  # simple porcentaje

    # Entorno seguro
    allowed = {
        "math": math,
        "__builtins__": {},
    }

    try:
        resultado = eval(expresion, allowed)
        return float(resultado)
    except Exception as e:
        raise ValueError(f"Error en la expresión: {e}")


def modo_interactivo():
    print("=== Calculadora Python Puro ===")
    print("Operaciones: + - * / ** sqrt() %")
    print("Ejemplos: 5 + 3, sqrt(16), 20%, 2 ** 8")
    print("Escribe 'salir' para terminar.\n")

    while True:
        try:
            entrada = input(">>> ").strip()
            if entrada.lower() in ("salir", "exit", "q"):
                print("Hasta luego!")
                break
            if not entrada:
                continue

            resultado = calcular(entrada)
            print(f"= {resultado}\n")
        except KeyboardInterrupt:
            print("\nHasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Calculadora en Python puro (biblioteca estándar)"
    )
    parser.add_argument(
        "expresion",
        nargs="*",
        help="Expresión a evaluar (ej: '5 + 3' o 'sqrt(16)')"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Forzar modo interactivo"
    )

    args = parser.parse_args()

    if args.interactive or not args.expresion:
        modo_interactivo()
    else:
        expresion = " ".join(args.expresion)
        try:
            resultado = calcular(expresion)
            print(resultado)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
