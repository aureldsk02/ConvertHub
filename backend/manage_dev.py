#!/usr/bin/env python
"""
Script de gestion pour le développement de ConvertHub
"""
import os
import sys
import subprocess
from pathlib import Path

# Ajouter le répertoire courant au PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'converthub.settings')

def run_command(command, description):
    """Exécuter une commande avec description"""
    print(f"\n🔄 {description}...")
    print(f"Commande: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} terminé avec succès")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de {description}")
        print(f"Erreur: {e.stderr}")
        return False

def setup_database():
    """Configurer la base de données"""
    commands = [
        ("python manage.py makemigrations", "Création des migrations"),
        ("python manage.py migrate", "Application des migrations"),
        ("python manage.py createsuperuser --noinput --username admin --email admin@converthub.com", "Création du superuser"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def load_fixtures():
    """Charger les données de test"""
    print("\n🔄 Chargement des données de test...")
    
    # Créer des catégories de base
    from django.core.management import execute_from_command_line
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Catégories de base
        categories_data = [
            ('Unités', 'unites', 'Conversions d\'unités de mesure', '📏'),
            ('Devises', 'devises', 'Conversions de devises', '💰'),
            ('Formats', 'formats', 'Conversions de formats de fichiers', '📁'),
            ('Bases numériques', 'bases-numeriques', 'Conversions entre bases numériques', '🔢'),
            ('Langues', 'langues', 'Traductions et conversions linguistiques', '🌐'),
        ]
        
        for name, slug, description, icon in categories_data:
            cursor.execute("""
                INSERT INTO conversions_conversioncategory (name, slug, description, icon, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                ON CONFLICT (slug) DO NOTHING
            """, (name, slug, description, icon, True))
        
        # Types de conversion de base
        types_data = [
            ('Température Celsius vers Fahrenheit', 'celsius-fahrenheit', 1, '°C', '°F', 'F = C × 9/5 + 32'),
            ('Longueur mètres vers pieds', 'metres-pieds', 1, 'm', 'ft', 'ft = m × 3.28084'),
            ('Poids kilogrammes vers livres', 'kg-livres', 1, 'kg', 'lb', 'lb = kg × 2.20462'),
            ('Devise EUR vers USD', 'eur-usd', 2, 'EUR', 'USD', 'Taux de change en temps réel'),
        ]
        
        for name, slug, category_id, input_unit, output_unit, formula in types_data:
            cursor.execute("""
                INSERT INTO conversions_conversiontype (category_id, name, slug, input_unit, output_unit, formula, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                ON CONFLICT (slug) DO NOTHING
            """, (category_id, name, slug, input_unit, output_unit, formula, True))
    
    print("✅ Données de test chargées avec succès")
    return True

def main():
    """Fonction principale"""
    print("🚀 Script de gestion ConvertHub")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("Usage: python manage_dev.py [setup|run|test|shell]")
        print("\nCommandes disponibles:")
        print("  setup  - Configurer la base de données et charger les données de test")
        print("  run    - Démarrer le serveur de développement")
        print("  test   - Exécuter les tests")
        print("  shell  - Ouvrir le shell Django")
        return
    
    command = sys.argv[1]
    
    if command == "setup":
        print("\n🔧 Configuration de l'environnement de développement...")
        if setup_database():
            load_fixtures()
            print("\n🎉 Configuration terminée avec succès !")
            print("Vous pouvez maintenant démarrer le serveur avec: python manage_dev.py run")
        else:
            print("\n❌ Erreur lors de la configuration")
    
    elif command == "run":
        print("\n🚀 Démarrage du serveur de développement...")
        os.system("python manage.py runserver 0.0.0.0:8000")
    
    elif command == "test":
        print("\n🧪 Exécution des tests...")
        os.system("python manage.py test")
    
    elif command == "shell":
        print("\n🐍 Ouverture du shell Django...")
        os.system("python manage.py shell")
    
    else:
        print(f"❌ Commande inconnue: {command}")

if __name__ == "__main__":
    main()
