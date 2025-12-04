"""Script d'installation cross-platform des dépendances"""

import sys
import subprocess
from pathlib import Path


def main():
    """Installe les dépendances Python de manière cross-platform"""
    print("📦 Installation des dépendances NIRD Chatbot...")

    requirements_file = Path(__file__).parent / "requirements.txt"

    if not requirements_file.exists():
        print("❌ Erreur: requirements.txt introuvable!")
        sys.exit(1)

    try:
        # Mettre à jour pip
        print("\n1️⃣ Mise à jour de pip...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
        )

        # Installer les dépendances
        print("\n2️⃣ Installation des dépendances...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True,
        )

        print("\n✅ Installation terminée avec succès!")
        print("\nPour lancer l'API:")
        print("  python run.py")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de l'installation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
