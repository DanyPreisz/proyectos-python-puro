#!/usr/bin/env python3
"""
Buscador de archivos por nombre, extensión o contenido.
Python puro (pathlib + re).

Uso en Colab:
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/buscador_archivos.py
!python buscador_archivos.py
"""

import argparse
import re
import sys
from pathlib import Path


def buscar_archivos(
    carpeta: str,
    nombre: str = None,
    extension: str = None,
    contenido: str = None,
    ignorar_mayus: bool = True,
    recursivo: bool = True,
) -> list:
    """Busca archivos que coincidan con los criterios."""
    carpeta_path = Path(carpeta)
    if not carpeta_path.exists() or not carpeta_path.is_dir():
        raise ValueError(f"Carpeta no válida: {carpeta}")

    flags = re.IGNORECASE if ignorar_mayus else 0
    patron_nombre = re.compile(nombre, flags) if nombre else None
    patron_contenido = re.compile(contenido, flags) if contenido else None

    if extension and not extension.startswith("."):
        extension = "." + extension

    resultados = []
    patron_busqueda = "**/*" if recursivo else "*"

    for archivo in carpeta_path.glob(patron_busqueda):
        if not archivo.is_file():
            continue

        # Filtro por extensión
        if extension and archivo.suffix.lower() != extension.lower():
            continue

        # Filtro por nombre
        if patron_nombre and not patron_nombre.search(archivo.name):
            continue

        # Filtro por contenido
        if patron_contenido:
            try:
                texto = archivo.read_text(encoding="utf-8", errors="ignore")
                if not patron_contenido.search(texto):
                    continue
            except Exception:
                continue

        resultados.append(archivo)

    return resultados


def mostrar_resultados(resultados: list):
    if not resultados:
        print("No se encontraron archivos.")
        return

    print(f"\nSe encontraron {len(resultados)} archivo(s):\n")
    for i, archivo in enumerate(resultados, 1):
        print(f"{i:3}. {archivo}")


def modo_interactivo():
    print("=== Buscador de Archivos ===\n")

    while True:
        try:
            carpeta = input("Carpeta a buscar (o 'salir'): ").strip()
            if carpeta.lower() in ("salir", "exit", "q"):
                print("Hasta luego!")
                break
            if not carpeta:
                carpeta = "."

            nombre = input("Patrón de nombre (regex, opcional): ").strip() or None
            extension = input("Extensión (ej: .py, opcional): ").strip() or None
            contenido = input("Texto en contenido (regex, opcional): ").strip() or None
            recursivo = input("Buscar en subcarpetas? (s/n, defecto s): ").lower() != "n"

            resultados = buscar_archivos(
                carpeta, nombre, extension, contenido, True, recursivo
            )
            mostrar_resultados(resultados)
            print()

        except Exception as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nHasta luego!")
            break


def main():
    parser = argparse.ArgumentParser(description="Buscador de archivos (Python puro)")
    parser.add_argument("carpeta", nargs="?", default=".", help="Carpeta donde buscar")
    parser.add_argument("-n", "--nombre", help="Patrón de nombre (regex)")
    parser.add_argument("-e", "--extension", help="Extensión (ej: .py)")
    parser.add_argument("-c", "--contenido", help="Texto a buscar en el contenido (regex)")
    parser.add_argument("--no-recursivo", action="store_true", help="No buscar en subcarpetas")
    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive or (len(sys.argv) == 1):
        modo_interactivo()
        return

    try:
        resultados = buscar_archivos(
            args.carpeta,
            args.nombre,
            args.extension,
            args.contenido,
            True,
            not args.no_recursivo,
        )
        mostrar_resultados(resultados)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
