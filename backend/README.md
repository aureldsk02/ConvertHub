# 🔧 Backend ConvertHub - Django

## Vue d'ensemble

Le backend de ConvertHub est construit avec Django et Django REST Framework, offrant une API robuste pour toutes les conversions possibles.

## 🏗️ Architecture

### Applications Django

- **`conversions`** : Gestion des conversions (unités, devises, fichiers)
- **`users`** : Gestion des utilisateurs et profils
- **`core`** : Fonctionnalités de base et utilitaires

### Modèles de données

- **`ConversionCategory`** : Catégories de conversion (unités, devises, etc.)
- **`ConversionType`** : Types spécifiques de conversion
- **`Conversion`** : Historique des conversions effectuées
- **`FileConversion`** : Conversions de fichiers

## 🚀 Installation et configuration

### 1. Environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copier le fichier d'environnement
cp env.example .env

# Éditer .env avec vos paramètres
nano .env
```

### 4. Base de données

```bash
# Configuration automatique
python manage_dev.py setup

# Ou manuellement
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Démarrage

```bash
# Avec le script de gestion
python manage_dev.py run

# Ou directement
python manage.py runserver
```

## 📡 API Endpoints

### Conversions

- `GET /api/categories/` - Liste des catégories
- `GET /api/types/` - Liste des types de conversion
- `POST /api/conversions/convert/` - Effectuer une conversion
- `GET /api/conversions/` - Historique des conversions

### Utilisateurs

- `GET /api/users/profile/` - Profil utilisateur
- `GET /api/users/stats/` - Statistiques utilisateur

### Core

- `GET /api/core/health/` - Vérification de l'état
- `GET /api/core/stats/` - Statistiques globales

## 🧪 Tests

```bash
# Tous les tests
python manage_dev.py test

# Tests spécifiques
python manage.py test apps.conversions
python manage.py test apps.users
```

## 🔧 Scripts de gestion

Le fichier `manage_dev.py` fournit des commandes utiles :

- `python manage_dev.py setup` - Configuration complète
- `python manage_dev.py run` - Démarrer le serveur
- `python manage_dev.py test` - Exécuter les tests
- `python manage_dev.py shell` - Shell Django

## 📊 Administration

Accédez à l'interface d'administration Django à `/admin/` avec le superuser créé.

## 🔒 Sécurité

- Authentification requise pour certaines opérations
- Validation des données d'entrée
- Protection CSRF
- Gestion des permissions par utilisateur

## 🚀 Prochaines étapes

1. ✅ Configuration Django de base
2. ✅ Modèles de données
3. ✅ API REST
4. 🔄 Logique de conversion réelle
5. 🔄 Tests automatisés
6. 🔄 Documentation API complète
