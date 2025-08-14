# 📁 Structure du Projet ConvertHub

## Vue d'ensemble

ConvertHub est une plateforme web open-source pour toutes sortes de conversions, construite avec Django (backend) et Next.js (frontend).

## 🏗️ Architecture

```
ConvertHub/
├── backend/                 # API Django
│   ├── converthub/         # Configuration principale Django
│   ├── apps/              # Applications Django
│   ├── requirements.txt    # Dépendances Python
│   └── Dockerfile         # Containerisation backend
├── frontend/               # Interface Next.js
│   ├── src/               # Code source React
│   ├── public/            # Assets statiques
│   ├── package.json       # Dépendances Node.js
│   └── Dockerfile         # Containerisation frontend
├── docs/                  # Documentation
├── tests/                 # Tests automatisés
├── docker-compose.yml     # Orchestration des services
└── README.md              # Documentation principale
```

## 🚀 Services

- **Backend Django** : Port 8000
- **Frontend Next.js** : Port 3000
- **PostgreSQL** : Port 5432
- **Redis** : Port 6379

## 🔧 Technologies

### Backend
- Django 5.0.2
- Django REST Framework
- PostgreSQL
- Redis + Celery
- Python 3.11+

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Framer Motion

## 📋 Prochaines étapes

1. ✅ Structure du projet
2. 🔄 Configuration Django
3. 🔄 Modèles de données
4. 🔄 API REST
5. 🔄 Interface utilisateur
6. 🔄 Tests
7. 🔄 Déploiement
