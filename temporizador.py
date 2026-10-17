#!/usr/bin/env python3
"""
Temporizador y cronómetro en Python puro.
Usa time y threading.

Uso en Colab:
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/temporizador.py
!python temporizador.py
"""

import argparse
import sys
import time
import threading


def formato_tiempo(segundos: float) -> str:
    """Convierte segundos a HH:MM:SS."""
    segundos = int(segundos)
    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def cronometro():
    """Cronómetro que cuenta hacia arriba. Presiona Enter para detener."""
    print("Cronómetro iniciado. Presiona Enter para detener.\n")
    inicio = time.time()
    detenido = threading.Event()

    def esperar_enter():
        input()
        detenido.set()

    hilo = threading.Thread(target=esperar_enter, daemon=True)
    hilo.start()

    try:
        while not detenido.is_set():
            transcurrido = time.time() - inicio
            print(f"\rTiempo: {formato_tiempo(transcurrido)}", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    print(f"\n\nTiempo final: {formato_tiempo(time.time() - inicio)}")


def temporizador(segundos: int):
    """Temporizador que cuenta hacia atrás."""
    print(f"Temporizador de {formato_tiempo(segundos)} iniciado.\n")
    inicio = time.time()
    fin = inicio + segundos

    try:
        while time.time() < fin:
            restante = fin - time.time()
            print(f"\rRestante: {formato_tiempo(restante)}", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nTemporizador cancelado.")
        return

    print("\n\n¡Tiempo terminado!")
    # Intentar hacer un beep (funciona en algunos entornos)
    print("\a", end="", flush=True)


def modo_interactivo():
    print("=== Temporizador / Cronómetro ===\n")
    print("1. Cronómetro (cuenta hacia arriba)")
    print("2. Temporizador (cuenta hacia atrás)")
    print("Escribe 'salir' para terminar.\n")

    while True:
        opcion = input("Opción (1/2/salir): ").strip().lower()
        if opcion in ("salir", "exit", "q"):
            print("Hasta luego!")
            break

        if opcion == "1":
            cronometro()
            print()
        elif opcion == "2":
            try:
                minutos = input("Minutos (defecto 0): ").strip() or "0"
                segundos = input("Segundos (defecto 10): ").strip() or "10"
                total = int(minutos) * 60 + int(segundos)
                if total <= 0:
                    print("El tiempo debe ser mayor a 0.\n")
                    continue
                temporizador(total)
                print()
            except ValueError:
                print("Número inválido.\n")
        else:
            print("Opción no válida.\n")


def main():
    parser = argparse.ArgumentParser(description="Temporizador y cronómetro")
    parser.add_argument("-c", "--cronometro", action="store_true", help="Iniciar cronómetro")
    parser.add_argument("-t", "--temporizador", type=int, help="Temporizador en segundos")
    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")

    args = parser.parse_args()

    if args.interactive or (not args.cronometro and args.temporizador is None):
        modo_interactivo()
        return

    if args.cronometro:
        cronometro()
    elif args.temporizador:
        temporizador(args.temporizador)


if __name__ == "__main__":
    main()
