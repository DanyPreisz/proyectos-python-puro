#!/usr/bin/env python3
"""
Generador de contraseñas seguras en Python puro (solo biblioteca estándar).
Usa el módulo secrets para generación criptográficamente segura.

Uso en Google Colab:
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/generador_contrasenas.py
!python generador_contrasenas.py
"""

import argparse
import secrets
import string
import sys


def generar_contrasena(
    longitud: int = 16,
    incluir_mayusculas: bool = True,
    incluir_minusculas: bool = True,
    incluir_numeros: bool = True,
    incluir_simbolos: bool = True,
) -> str:
    """Genera una contraseña segura con los criterios indicados."""
    if longitud < 4:
        raise ValueError("La longitud mínima recomendada es 4.")

    caracteres = ""
    obligatorios = []

    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
        obligatorios.append(secrets.choice(string.ascii_uppercase))
    if incluir_minusculas:
        caracteres += string.ascii_lowercase
        obligatorios.append(secrets.choice(string.ascii_lowercase))
    if incluir_numeros:
        caracteres += string.digits
        obligatorios.append(secrets.choice(string.digits))
    if incluir_simbolos:
        simbolos = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        caracteres += simbolos
        obligatorios.append(secrets.choice(simbolos))

    if not caracteres:
        raise ValueError("Debes incluir al menos un tipo de caracter.")

    # Completar el resto de la contraseña
    resto = [secrets.choice(caracteres) for _ in range(longitud - len(obligatorios))]
    contrasena_lista = obligatorios + resto

    # Mezclar para que no queden siempre al principio los obligatorios
    secrets.SystemRandom().shuffle(contrasena_lista)

    return "".join(contrasena_lista)


def modo_interactivo():
    print("=== Generador de Contraseñas Seguras ===\n")

    try:
        longitud = int(input("Longitud (por defecto 16): ") or 16)
        mayus = input("Incluir mayúsculas? (s/n, defecto s): ").lower() != "n"
        minus = input("Incluir minúsculas? (s/n, defecto s): ").lower() != "n"
        nums = input("Incluir números? (s/n, defecto s): ").lower() != "n"
        sims = input("Incluir símbolos? (s/n, defecto s): ").lower() != "n"
        cantidad = int(input("¿Cuántas contraseñas generar? (defecto 1): ") or 1)

        print("\n--- Contraseñas generadas ---\n")
        for i in range(cantidad):
            pwd = generar_contrasena(longitud, mayus, minus, nums, sims)
            print(f"{i+1}. {pwd}")

    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nCancelado.")


def main():
    parser = argparse.ArgumentParser(
        description="Generador de contraseñas seguras (Python puro)"
    )
    parser.add_argument("-l", "--longitud", type=int, default=16, help="Longitud de la contraseña")
    parser.add_argument("-n", "--cantidad", type=int, default=1, help="Cantidad de contraseñas")
    parser.add_argument("--sin-mayus", action="store_true", help="Excluir mayúsculas")
    parser.add_argument("--sin-minus", action="store_true", help="Excluir minúsculas")
    parser.add_argument("--sin-numeros", action="store_true", help="Excluir números")
    parser.add_argument("--sin-simbolos", action="store_true", help="Excluir símbolos")
    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive or len(sys.argv) == 1:
        modo_interactivo()
        return

    try:
        for i in range(args.cantidad):
            pwd = generar_contrasena(
                longitud=args.longitud,
                incluir_mayusculas=not args.sin_mayus,
                incluir_minusculas=not args.sin_minus,
                incluir_numeros=not args.sin_numeros,
                incluir_simbolos=not args.sin_simbolos,
            )
            print(pwd)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
