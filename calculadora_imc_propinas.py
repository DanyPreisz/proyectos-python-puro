#!/usr/bin/env python3
"""
Calculadora de IMC y de propinas.
Python puro.

Uso en Colab:
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/calculadora_imc_propinas.py
!python calculadora_imc_propinas.py
"""

import argparse
import sys


def calcular_imc(peso: float, altura: float) -> dict:
    """Calcula el IMC y su clasificación."""
    if peso <= 0 or altura <= 0:
        raise ValueError("Peso y altura deben ser mayores a 0.")

    imc = peso / (altura ** 2)

    if imc < 18.5:
        clasificacion = "Bajo peso"
    elif imc < 25:
        clasificacion = "Peso normal"
    elif imc < 30:
        clasificacion = "Sobrepeso"
    else:
        clasificacion = "Obesidad"

    return {"imc": round(imc, 2), "clasificacion": clasificacion}


def calcular_propina(total: float, porcentaje: float, personas: int = 1) -> dict:
    """Calcula propina y total por persona."""
    if total < 0 or porcentaje < 0 or personas < 1:
        raise ValueError("Valores inválidos.")

    propina = total * (porcentaje / 100)
    total_con_propina = total + propina
    por_persona = total_con_propina / personas

    return {
        "propina": round(propina, 2),
        "total": round(total_con_propina, 2),
        "por_persona": round(por_persona, 2),
    }


def modo_interactivo():
    print("=== Calculadora de IMC y Propinas ===\n")
    print("1. Calcular IMC")
    print("2. Calcular propina")
    print("Escribe 'salir' para terminar.\n")

    while True:
        opcion = input("Opción (1/2/salir): ").strip().lower()
        if opcion in ("salir", "exit", "q"):
            print("Hasta luego!")
            break

        try:
            if opcion == "1":
                peso = float(input("Peso (kg): "))
                altura = float(input("Altura (m): "))
                resultado = calcular_imc(peso, altura)
                print(f"\nIMC: {resultado['imc']}")
                print(f"Clasificación: {resultado['clasificacion']}\n")

            elif opcion == "2":
                total = float(input("Total de la cuenta: "))
                porcentaje = float(input("Porcentaje de propina (ej: 10): ") or 10)
                personas = int(input("Número de personas (defecto 1): ") or 1)
                resultado = calcular_propina(total, porcentaje, personas)
                print(f"\nPropina: {resultado['propina']}")
                print(f"Total con propina: {resultado['total']}")
                print(f"Por persona: {resultado['por_persona']}\n")

            else:
                print("Opción no válida.\n")

        except ValueError as e:
            print(f"Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(description="Calculadora de IMC y propinas")
    subparsers = parser.add_subparsers(dest="comando")

    p_imc = subparsers.add_parser("imc", help="Calcular IMC")
    p_imc.add_argument("peso", type=float, help="Peso en kg")
    p_imc.add_argument("altura", type=float, help="Altura en metros")

    p_prop = subparsers.add_parser("propina", help="Calcular propina")
    p_prop.add_argument("total", type=float, help="Total de la cuenta")
    p_prop.add_argument("-p", "--porcentaje", type=float, default=10, help="Porcentaje")
    p_prop.add_argument("-n", "--personas", type=int, default=1, help="Número de personas")

    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive or args.comando is None:
        modo_interactivo()
        return

    try:
        if args.comando == "imc":
            r = calcular_imc(args.peso, args.altura)
            print(f"IMC: {r['imc']} ({r['clasificacion']})")
        elif args.comando == "propina":
            r = calcular_propina(args.total, args.porcentaje, args.personas)
            print(f"Propina: {r['propina']}")
            print(f"Total: {r['total']}")
            print(f"Por persona: {r['por_persona']}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
