#!/usr/bin/env python3
"""
Generador de nombres de usuario y de proyectos aleatorios.
Python puro (random + listas).

Uso en Colab:
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/generador_nombres.py
!python generador_nombres.py
"""

import argparse
import random
import string
import sys

# Listas de palabras para combinar
ADJETIVOS = [
    "rapido", "brillante", "silencioso", "poderoso", "creativo",
    "oscuro", "luminoso", "agil", "sabio", "valiente",
    "misterioso", "feliz", "audaz", "sereno", "feroz",
]

SUSTANTIVOS = [
    "lobo", "aguila", "dragon", "tigre", "leon",
    "codigo", "nube", "estrella", "rio", "montana",
    "fuego", "viento", "oceano", "rayo", "sombra",
]

PROYECTOS_PREFIJOS = [
    "proyecto", "app", "sistema", "herramienta", "plataforma",
    "servicio", "modulo", "libreria", "bot", "api",
]


def generar_usuario(cantidad: int = 1, con_numero: bool = True, longitud_numero: int = 2) -> list:
    """Genera nombres de usuario del tipo adjetivo_sustantivo123."""
    resultados = []
    for _ in range(cantidad):
        adj = random.choice(ADJETIVOS)
        sust = random.choice(SUSTANTIVOS)
        nombre = f"{adj}_{sust}"
        if con_numero:
            numero = "".join(random.choices(string.digits, k=longitud_numero))
            nombre += numero
        resultados.append(nombre)
    return resultados


def generar_proyecto(cantidad: int = 1, con_numero: bool = False) -> list:
    """Genera nombres de proyectos."""
    resultados = []
    for _ in range(cantidad):
        prefijo = random.choice(PROYECTOS_PREFIJOS)
        adj = random.choice(ADJETIVOS)
        sust = random.choice(SUSTANTIVOS)
        nombre = f"{prefijo}-{adj}-{sust}"
        if con_numero:
            nombre += f"-{random.randint(1, 99)}"
        resultados.append(nombre)
    return resultados


def generar_aleatorio(cantidad: int = 1, longitud: int = 8) -> list:
    """Genera nombres completamente aleatorios."""
    caracteres = string.ascii_lowercase + string.digits
    return [
        "".join(random.choices(caracteres, k=longitud))
        for _ in range(cantidad)
    ]


def modo_interactivo():
    print("=== Generador de Nombres ===\n")
    print("1. Nombres de usuario")
    print("2. Nombres de proyectos")
    print("3. Nombres aleatorios")
    print("Escribe 'salir' para terminar.\n")

    while True:
        opcion = input("Opción (1/2/3/salir): ").strip().lower()
        if opcion in ("salir", "exit", "q"):
            print("Hasta luego!")
            break

        try:
            cantidad = int(input("¿Cuántos generar? (defecto 5): ") or 5)

            if opcion == "1":
                con_num = input("Incluir números? (s/n, defecto s): ").lower() != "n"
                nombres = generar_usuario(cantidad, con_num)
            elif opcion == "2":
                con_num = input("Incluir número al final? (s/n): ").lower() == "s"
                nombres = generar_proyecto(cantidad, con_num)
            elif opcion == "3":
                longitud = int(input("Longitud (defecto 8): ") or 8)
                nombres = generar_aleatorio(cantidad, longitud)
            else:
                print("Opción no válida.\n")
                continue

            print("\n--- Nombres generados ---\n")
            for i, nombre in enumerate(nombres, 1):
                print(f"{i}. {nombre}")
            print()

        except ValueError as e:
            print(f"Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(description="Generador de nombres")
    parser.add_argument("tipo", nargs="?", choices=["usuario", "proyecto", "aleatorio"],
                        help="Tipo de nombre")
    parser.add_argument("-n", "--cantidad", type=int, default=5, help="Cantidad")
    parser.add_argument("--sin-numero", action="store_true", help="Sin números")
    parser.add_argument("-l", "--longitud", type=int, default=8, help="Longitud (aleatorio)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive or args.tipo is None:
        modo_interactivo()
        return

    if args.tipo == "usuario":
        nombres = generar_usuario(args.cantidad, not args.sin_numero)
    elif args.tipo == "proyecto":
        nombres = generar_proyecto(args.cantidad, not args.sin_numero)
    else:
        nombres = generar_aleatorio(args.cantidad, args.longitud)

    for nombre in nombres:
        print(nombre)


if __name__ == "__main__":
    main()
