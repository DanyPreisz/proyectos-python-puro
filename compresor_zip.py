#!/usr/bin/env python3
"""
Compresor y descompresor simple usando zipfile (biblioteca estándar).

Uso en Colab:
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/compresor_zip.py
!python compresor_zip.py
"""

import argparse
import sys
import zipfile
from pathlib import Path


def comprimir(archivos: list, salida: str):
    """Comprime uno o varios archivos/carpetas en un ZIP."""
    salida_path = Path(salida)
    if not salida_path.suffix:
        salida_path = salida_path.with_suffix(".zip")

    with zipfile.ZipFile(salida_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in archivos:
            path = Path(item)
            if not path.exists():
                print(f"Aviso: no existe {item}")
                continue

            if path.is_file():
                zf.write(path, path.name)
                print(f"  + {path.name}")
            elif path.is_dir():
                for archivo in path.rglob("*"):
                    if archivo.is_file():
                        arcname = archivo.relative_to(path.parent)
                        zf.write(archivo, arcname)
                        print(f"  + {arcname}")

    print(f"\nCreado: {salida_path}")
    return str(salida_path)


def descomprimir(archivo_zip: str, destino: str = "."):
    """Descomprime un archivo ZIP."""
    zip_path = Path(archivo_zip)
    if not zip_path.exists():
        raise FileNotFoundError(f"No se encontró: {archivo_zip}")

    destino_path = Path(destino)
    destino_path.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(destino_path)
        print(f"Extraído en: {destino_path}")
        print("Archivos:")
        for nombre in zf.namelist():
            print(f"  - {nombre}")

    return str(destino_path)


def listar_contenido(archivo_zip: str):
    """Lista el contenido de un ZIP sin extraerlo."""
    zip_path = Path(archivo_zip)
    if not zip_path.exists():
        raise FileNotFoundError(f"No se encontró: {archivo_zip}")

    with zipfile.ZipFile(zip_path, "r") as zf:
        print(f"Contenido de {zip_path.name}:\n")
        for info in zf.infolist():
            print(f"  {info.filename}  ({info.file_size} bytes)")


def modo_interactivo():
    print("=== Compresor / Descompresor ZIP ===\n")
    print("1. Comprimir archivos")
    print("2. Descomprimir ZIP")
    print("3. Listar contenido de un ZIP")
    print("Escribe 'salir' para terminar.\n")

    while True:
        opcion = input("Opción (1/2/3/salir): ").strip().lower()
        if opcion in ("salir", "exit", "q"):
            print("Hasta luego!")
            break

        try:
            if opcion == "1":
                archivos = input("Archivos o carpetas (separados por espacio): ").split()
                salida = input("Nombre del ZIP de salida: ").strip() or "archivo.zip"
                comprimir(archivos, salida)

            elif opcion == "2":
                archivo = input("Archivo ZIP: ").strip()
                destino = input("Carpeta destino (Enter = actual): ").strip() or "."
                descomprimir(archivo, destino)

            elif opcion == "3":
                archivo = input("Archivo ZIP: ").strip()
                listar_contenido(archivo)

            else:
                print("Opción no válida.\n")

            print()

        except Exception as e:
            print(f"Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(description="Compresor y descompresor ZIP")
    subparsers = parser.add_subparsers(dest="comando")

    p_comp = subparsers.add_parser("comprimir", help="Comprimir archivos")
    p_comp.add_argument("archivos", nargs="+", help="Archivos o carpetas")
    p_comp.add_argument("-o", "--salida", default="archivo.zip", help="Nombre del ZIP")

    p_desc = subparsers.add_parser("descomprimir", help="Descomprimir ZIP")
    p_desc.add_argument("archivo", help="Archivo ZIP")
    p_desc.add_argument("-d", "--destino", default=".", help="Carpeta destino")

    p_list = subparsers.add_parser("listar", help="Listar contenido de un ZIP")
    p_list.add_argument("archivo", help="Archivo ZIP")

    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive or args.comando is None:
        modo_interactivo()
        return

    try:
        if args.comando == "comprimir":
            comprimir(args.archivos, args.salida)
        elif args.comando == "descomprimir":
            descomprimir(args.archivo, args.destino)
        elif args.comando == "listar":
            listar_contenido(args.archivo)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
