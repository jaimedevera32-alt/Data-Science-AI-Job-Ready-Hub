#!/usr/bin/env python3
"""
Daily Training Platform Runner - 1h/day
Ejecuta y evalúa los retos diarios de preparación técnica.
"""
import sys
import subprocess
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TRACKS_DIR = BASE_DIR / "tracks"

TRACKS = {
    "1": ("Python & Algoritmia para Data", "01_python_algos"),
    "2": ("SQL & Analytics Engineering (DuckDB)", "02_sql_mastery"),
    "3": ("Data Engineering & PySpark", "03_spark_data_eng"),
    "4": ("Machine Learning & MLOps", "04_ml_engineering"),
    "5": ("AI Agents & Skills (ReAct, Tools, MCP)", "05_ai_agents_skills"),
}

def print_banner():
    print("=" * 70)
    print("  🚀 DATA SCIENCE & AI JOB-READY HUB - DAILY TRAINING (1h/DAY)")
    print("=" * 70)
    print(" Rutina diaria:")
    print("  • 15 min: Flash Conceptual (Teoría / Arquitectura)")
    print("  • 35 min: Coding Kata (Solución de código + pytest)")
    print("  • 10 min: Simulación de Entrevista Técnica con Agente")
    print("=" * 70)

def list_tracks():
    print("\nSelecciona el track que quieres entrenar hoy:\n")
    for key, (name, _) in TRACKS.items():
        print(f"  [{key}] {name}")
    print("  [0] Salir\n")

def run_tests_for_challenge(challenge_dir: Path):
    test_files = list(challenge_dir.glob("test_*.py"))
    if not test_files:
        print(f"⚠️ No se encontraron archivos de test en: {challenge_dir}")
        return
    
    print(f"\n🧪 Ejecutando tests automáticos en: {challenge_dir.name}...")
    
    # Intento con pytest primero
    cmd = [sys.executable, "-m", "pytest", str(challenge_dir), "-v"]
    res = subprocess.run(cmd)
    
    if res.returncode != 0:
        # Fallback a ejecución directa si pytest no está instalado
        for tf in test_files:
            print(f"-> Ejecutando directamente {tf.name}...")
            res_direct = subprocess.run([sys.executable, str(tf)], cwd=str(challenge_dir))
            if res_direct.returncode != 0:
                print(f"\n❌ Error al ejecutar {tf.name}.")
                return
        print("\n🎉 ¡Tests ejecutados con éxito!")
    else:
        print("\n🎉 ¡ENHORABUENA! Todos los tests han pasado exitosamente.")
        print("💡 Próximo paso: Revisa las preguntas de entrevista en el README del reto.")

def select_challenge_in_track(folder_name: str):
    target_track = TRACKS_DIR / folder_name
    if not target_track.exists():
        print(f"Directorio de track no encontrado: {target_track}")
        return
    
    challenges = sorted([d for d in target_track.iterdir() if d.is_dir()])
    if not challenges:
        print(f"No hay retos disponibles aún en este track.")
        return
    
    print(f"\nRetos disponibles en {folder_name}:")
    for i, ch in enumerate(challenges, 1):
        print(f"  [{i}] {ch.name}")
    print("  [0] Volver")
    
    choice = input("\nElige un reto: ").strip()
    if choice == "0" or not choice.isdigit():
        return
    idx = int(choice) - 1
    if 0 <= idx < len(challenges):
        selected = challenges[idx]
        readme = selected / "README.md"
        if readme.exists():
            print("\n" + "-" * 70)
            print(readme.read_text(encoding="utf-8"))
            print("-" * 70)
        
        input("\nPulsa ENTER cuando estés listo para ejecutar los tests de tu solución...")
        run_tests_for_challenge(selected)

def main():
    while True:
        print_banner()
        list_tracks()
        choice = input("Opción: ").strip()
        if choice == "0":
            print("\n¡Hasta mañana! Mantén la racha diaria de 1h.")
            break
        elif choice in TRACKS:
            _, folder = TRACKS[choice]
            select_challenge_in_track(folder)
            input("\nPulsa ENTER para volver al menú principal...")
        else:
            print("Opción inválida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()

