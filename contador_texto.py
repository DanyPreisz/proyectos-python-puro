#!/usr/bin/env python3
"""
Contador de palabras, líneas y caracteres en archivos de texto.
Python puro (solo biblioteca estándar).

Uso en Colab:
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/contador_texto.py
!python contador_texto.py archivo.txt
"""

import argparse
import sys
from pathlib import Path


def analizar_texto(contenido: str) -> dict:
    """Analiza un texto y devuelve estadísticas."""
    lineas = contenido.splitlines()
    palabras = contenido.split()

    return {
        "lineas": len(lineas),
        "lineas_no_vacias": sum(1 for l in lineas if l.strip()),
        "palabras": len(palabras),
        "caracteres": len(contenido),
        "caracteres_sin_espacios": len(contenido.replace(" ", "").replace("\n", "").replace("\t", "")),
        "parrafos": len([p for p in contenido.split("\n\n") if p.strip()]),
    }


def analizar_archivo(ruta: str) -> dict:
    """Lee un archivo y lo analiza."""
    path = Path(ruta)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    if not path.is_file():
        raise ValueError(f"No es un archivo: {ruta}")

    contenido = path.read_text(encoding="utf-8", errors="replace")
    stats = analizar_texto(contenido)
    stats["archivo"] = str(path)
    return stats


def mostrar_estadisticas(stats: dict):
    """Muestra las estadísticas de forma clara."""
    print(f"\nArchivo: {stats.get('archivo', '(texto directo)')}")
    print("-" * 40)
    print(f"Líneas totales:          {stats['lineas']}")
    print(f"Líneas no vacías:        {stats['lineas_no_vacias']}")
    print(f"Palabras:                {stats['palabras']}")
    print(f"Caracteres:              {stats['caracteres']}")
    print(f"Caracteres (sin espacios): {stats['caracteres_sin_espacios']}")
    print(f"Párrafos:                {stats['parrafos']}")
    print("-" * 40)


def modo_interactivo():
    print("=== Contador de Texto ===\n")
    print("1. Analizar archivo")
    print("2. Analizar texto pegado")
    print("Escribe 'salir' para terminar.\n")

    while True:
        opcion = input("Opción (1/2/salir): ").strip().lower()
        if opcion in ("salir", "exit", "q"):
            print("Hasta luego!")
            break

        if opcion == "1":
            ruta = input("Ruta del archivo: ").strip()
            try:
                stats = analizar_archivo(ruta)
                mostrar_estadisticas(stats)
            except Exception as e:
                print(f"Error: {e}\n")

        elif opcion == "2":
            print("Pega el texto (termina con una línea vacía):")
            lineas = []
            while True:
                linea = input()
                if linea == "":
                    break
                lineas.append(linea)
            texto = "\n".join(lineas)
            if texto.strip():
                stats = analizar_texto(texto)
                mostrar_estadisticas(stats)
            else:
                print("No se ingresó texto.\n")
        else:
            print("Opción no válida.\n")


def main():
    parser = argparse.ArgumentParser(description="Contador de palabras, líneas y caracteres")
    parser.add_argument("archivo", nargs="?", help="Archivo de texto a analizar")
    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive or args.archivo is None:
        modo_interactivo()
        return

    try:
        stats = analizar_archivo(args.archivo)
        mostrar_estadisticas(stats)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
