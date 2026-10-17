#!/usr/bin/env python3
"""
Organizador de carpetas: mueve archivos por extensión a subcarpetas.
Python puro (pathlib).

Uso en Colab:
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/organizador_carpetas.py
!python organizador_carpetas.py
"""

import argparse
import sys
from pathlib import Path


def organizar_por_extension(
    carpeta: str,
    simulacion: bool = True,
    crear_carpetas: bool = True,
) -> list:
    """
    Mueve archivos a subcarpetas según su extensión.
    Devuelve lista de (original, destino).
    """
    carpeta_path = Path(carpeta)
    if not carpeta_path.exists() or not carpeta_path.is_dir():
        raise ValueError(f"Carpeta no válida: {carpeta}")

    cambios = []

    for archivo in carpeta_path.iterdir():
        if not archivo.is_file():
            continue

        extension = archivo.suffix.lower().lstrip(".") or "sin_extension"
        destino_carpeta = carpeta_path / extension

        if crear_carpetas and not simulacion:
            destino_carpeta.mkdir(exist_ok=True)

        destino = destino_carpeta / archivo.name
        cambios.append((archivo, destino))

    if not simulacion:
        for original, destino in cambios:
            if original != destino:
                # Crear carpeta si no existe
                destino.parent.mkdir(exist_ok=True)
                original.rename(destino)

    return cambios


def mostrar_cambios(cambios: list, simulacion: bool = True):
    if not cambios:
        print("No hay archivos para organizar.")
        return

    modo = "SIMULACIÓN" if simulacion else "EJECUTADO"
    print(f"\n[{modo}] {len(cambios)} archivo(s):\n")
    for original, destino in cambios:
        print(f"  {original.name}  →  {destino.parent.name}/{destino.name}")
    print()


def modo_interactivo():
    print("=== Organizador de Carpetas por Extensión ===\n")

    while True:
        try:
            carpeta = input("Carpeta a organizar (o 'salir'): ").strip()
            if carpeta.lower() in ("salir", "exit", "q"):
                print("Hasta luego!")
                break
            if not carpeta:
                carpeta = "."

            # Simulación primero
            cambios = organizar_por_extension(carpeta, simulacion=True)
            mostrar_cambios(cambios, simulacion=True)

            if cambios:
                confirmar = input("¿Aplicar cambios? (s/n): ").lower()
                if confirmar == "s":
                    organizar_por_extension(carpeta, simulacion=False)
                    print("Archivos organizados.\n")
                else:
                    print("Cancelado.\n")

        except Exception as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nHasta luego!")
            break


def main():
    parser = argparse.ArgumentParser(description="Organizador de carpetas por extensión")
    parser.add_argument("carpeta", nargs="?", default=".", help="Carpeta a organizar")
    parser.add_argument("--aplicar", action="store_true", help="Aplicar cambios (por defecto solo simula)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive or len(sys.argv) == 1:
        modo_interactivo()
        return

    try:
        cambios = organizar_por_extension(args.carpeta, simulacion=not args.aplicar)
        mostrar_cambios(cambios, simulacion=not args.aplicar)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
