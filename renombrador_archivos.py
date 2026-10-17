#!/usr/bin/env python3
"""
Renombrador masivo de archivos (patrones, numeración, fechas).
Python puro (pathlib).

Uso en Colab:
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/renombrador_archivos.py
!python renombrador_archivos.py
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path


def renombrar_archivos(
    carpeta: str,
    patron: str = "archivo_{n}",
    extension: str = None,
    inicio: int = 1,
    incluir_fecha: bool = False,
    prefijo: str = "",
    sufijo: str = "",
    simulacion: bool = True,
) -> list:
    """
    Renombra archivos en una carpeta.
    Devuelve lista de (original, nuevo).
    """
    carpeta_path = Path(carpeta)
    if not carpeta_path.exists() or not carpeta_path.is_dir():
        raise ValueError(f"Carpeta no válida: {carpeta}")

    archivos = [
        f for f in carpeta_path.iterdir()
        if f.is_file() and (not extension or f.suffix.lower() == extension.lower())
    ]
    archivos.sort()

    cambios = []
    fecha = datetime.now().strftime("%Y%m%d") if incluir_fecha else ""

    for i, archivo in enumerate(archivos, start=inicio):
        nuevo_nombre = patron.format(n=i, fecha=fecha)
        if prefijo:
            nuevo_nombre = prefijo + nuevo_nombre
        if sufijo:
            nuevo_nombre = nuevo_nombre + sufijo

        # Mantener extensión original si no se especifica otra
        if not extension:
            nuevo_nombre += archivo.suffix

        nuevo_path = archivo.parent / nuevo_nombre
        cambios.append((archivo, nuevo_path))

    if not simulacion:
        for original, nuevo in cambios:
            if original != nuevo:
                original.rename(nuevo)

    return cambios


def mostrar_cambios(cambios: list, simulacion: bool = True):
    if not cambios:
        print("No hay archivos para renombrar.")
        return

    modo = "SIMULACIÓN" if simulacion else "EJECUTADO"
    print(f"\n[{modo}] {len(cambios)} archivo(s):\n")
    for original, nuevo in cambios:
        print(f"  {original.name}  →  {nuevo.name}")
    print()


def modo_interactivo():
    print("=== Renombrador Masivo de Archivos ===\n")

    while True:
        try:
            carpeta = input("Carpeta (o 'salir'): ").strip()
            if carpeta.lower() in ("salir", "exit", "q"):
                print("Hasta luego!")
                break
            if not carpeta:
                carpeta = "."

            patron = input("Patrón (usa {n} y {fecha}, defecto 'archivo_{n}'): ").strip() or "archivo_{n}"
            extension = input("Filtrar por extensión (ej: .jpg, opcional): ").strip() or None
            inicio = int(input("Número inicial (defecto 1): ") or 1)
            incluir_fecha = input("Incluir fecha en el nombre? (s/n): ").lower() == "s"
            prefijo = input("Prefijo (opcional): ").strip()
            sufijo = input("Sufijo (opcional): ").strip()

            # Primero simulación
            cambios = renombrar_archivos(
                carpeta, patron, extension, inicio, incluir_fecha, prefijo, sufijo, simulacion=True
            )
            mostrar_cambios(cambios, simulacion=True)

            if cambios:
                confirmar = input("¿Aplicar cambios? (s/n): ").lower()
                if confirmar == "s":
                    renombrar_archivos(
                        carpeta, patron, extension, inicio, incluir_fecha, prefijo, sufijo, simulacion=False
                    )
                    print("Cambios aplicados.\n")
                else:
                    print("Cancelado.\n")

        except Exception as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nHasta luego!")
            break


def main():
    parser = argparse.ArgumentParser(description="Renombrador masivo de archivos")
    parser.add_argument("carpeta", nargs="?", default=".", help="Carpeta")
    parser.add_argument("-p", "--patron", default="archivo_{n}", help="Patrón (usa {n} y {fecha})")
    parser.add_argument("-e", "--extension", help="Filtrar por extensión")
    parser.add_argument("--inicio", type=int, default=1, help="Número inicial")
    parser.add_argument("--fecha", action="store_true", help="Incluir fecha")
    parser.add_argument("--prefijo", default="", help="Prefijo")
    parser.add_argument("--sufijo", default="", help="Sufijo")
    parser.add_argument("--aplicar", action="store_true", help="Aplicar cambios (por defecto solo simula)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive or len(sys.argv) == 1:
        modo_interactivo()
        return

    try:
        cambios = renombrar_archivos(
            args.carpeta,
            args.patron,
            args.extension,
            args.inicio,
            args.fecha,
            args.prefijo,
            args.sufijo,
            simulacion=not args.aplicar,
        )
        mostrar_cambios(cambios, simulacion=not args.aplicar)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
