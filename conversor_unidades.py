#!/usr/bin/env python3
"""
Conversor de unidades en Python puro (solo biblioteca estándar).
Soporta temperatura, longitud y peso.

Uso en Colab:
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/conversor_unidades.py
!python conversor_unidades.py
"""

import argparse
import sys

# Factores de conversión a unidad base
LONGITUD = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "mi": 1609.344,
}

PESO = {
    "mg": 0.001,
    "g": 1.0,
    "kg": 1000.0,
    "oz": 28.349523125,
    "lb": 453.59237,
}

TEMPERATURA = ["c", "f", "k"]


def convertir_longitud(valor: float, de: str, a: str) -> float:
    de, a = de.lower(), a.lower()
    if de not in LONGITUD or a not in LONGITUD:
        raise ValueError(f"Unidades válidas de longitud: {list(LONGITUD.keys())}")
    metros = valor * LONGITUD[de]
    return metros / LONGITUD[a]


def convertir_peso(valor: float, de: str, a: str) -> float:
    de, a = de.lower(), a.lower()
    if de not in PESO or a not in PESO:
        raise ValueError(f"Unidades válidas de peso: {list(PESO.keys())}")
    gramos = valor * PESO[de]
    return gramos / PESO[a]


def convertir_temperatura(valor: float, de: str, a: str) -> float:
    de, a = de.lower(), a.lower()
    if de not in TEMPERATURA or a not in TEMPERATURA:
        raise ValueError("Unidades válidas de temperatura: c, f, k")

    # Convertir a Celsius
    if de == "f":
        celsius = (valor - 32) * 5 / 9
    elif de == "k":
        celsius = valor - 273.15
    else:
        celsius = valor

    # De Celsius a destino
    if a == "f":
        return celsius * 9 / 5 + 32
    elif a == "k":
        return celsius + 273.15
    return celsius


def convertir(valor: float, tipo: str, de: str, a: str) -> float:
    tipo = tipo.lower()
    if tipo in ("longitud", "l", "len"):
        return convertir_longitud(valor, de, a)
    elif tipo in ("peso", "p", "weight"):
        return convertir_peso(valor, de, a)
    elif tipo in ("temperatura", "t", "temp"):
        return convertir_temperatura(valor, de, a)
    else:
        raise ValueError("Tipo válido: longitud, peso o temperatura")


def modo_interactivo():
    print("=== Conversor de Unidades ===\n")
    print("Tipos: longitud, peso, temperatura")
    print("Longitud: mm, cm, m, km, in, ft, mi")
    print("Peso: mg, g, kg, oz, lb")
    print("Temperatura: c, f, k\n")

    while True:
        try:
            tipo = input("Tipo (o 'salir'): ").strip().lower()
            if tipo in ("salir", "exit", "q"):
                print("Hasta luego!")
                break
            if not tipo:
                continue

            valor = float(input("Valor: "))
            de = input("De unidad: ").strip()
            a = input("A unidad: ").strip()

            resultado = convertir(valor, tipo, de, a)
            print(f"\n{valor} {de} = {resultado:.6g} {a}\n")

        except ValueError as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nHasta luego!")
            break


def main():
    parser = argparse.ArgumentParser(description="Conversor de unidades (Python puro)")
    parser.add_argument("valor", type=float, nargs="?", help="Valor a convertir")
    parser.add_argument("tipo", nargs="?", help="longitud | peso | temperatura")
    parser.add_argument("de", nargs="?", help="Unidad origen")
    parser.add_argument("a", nargs="?", help="Unidad destino")
    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive or args.valor is None:
        modo_interactivo()
        return

    try:
        resultado = convertir(args.valor, args.tipo, args.de, args.a)
        print(f"{args.valor} {args.de} = {resultado:.6g} {args.a}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
