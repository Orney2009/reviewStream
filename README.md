# reviewStream — Plateforme d'analyse de sentiments pour commentaires de films

Description
- Transformez les retours spectateurs en insights actionnables. reviewStream capture les commentaires de films en temps réel, les enrichit et les classe par polarité pour aider les équipes produit, marketing et contenu à prendre des décisions rapides et étayées.

Valeur ajoutée
- Surveillance instantanée du ressenti public sur vos titres.
- Segmentation automatique par polarité, thèmes et intensité émotionnelle.
- Intégration simple avec Kafka, base de données relationnelle et API REST pour la diffusion des résultats.

Cas d'usage
- Détection précoce des crises d'image après sortie d'un film.
- Priorisation des retours utilisateurs pour corriger des scènes, sous-titres ou métadonnées.
- Mesure d'impact des campagnes marketing sur le sentiment du public.

Composants clés
- Ingestion: `productor.py` et `kafka/producer.py` envoient les commentaires vers les topics Kafka.
- Traitement: `first_consumer.py`, `second_consumer.py` et `consumer/` appliquent nettoyage, transformation et enrichissement.
- Stockage: `data/db/` contient l'initialisation et les modèles SQLAlchemy pour persister les données.
- Modèle: `sa_model/Model.py` implémente l'analyse de sentiments ; `sa_model/training_model.ipynb` documente l'entraînement.
- Exposition: `flask_.py` propose une API REST pour récupérer métriques et résultats agrégés.

Prérequis rapides
- Python 3.8+
- Broker Kafka opérationnel (ou service compatible)
- Base de données compatible SQLAlchemy (Postgres recommandée)

Installation rapide
1. Cloner le dépôt et activer un virtualenv (optionnel).

```bash
git clone <repo_url>
cd reviewStream
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Paramétrer les connexions dans `lib/variables.py` et `data/db/database.py`.
3. Lancer Kafka (local ou distant) et créer les topics nécessaires.

Démarrages courants
- Lancer le producteur de tests : `python productor.py`
- Lancer un consommateur : `python first_consumer.py`
- Démarrer l'API : `python flask_.py`

Intégration produit
- Exportez les scores de sentiment via l'API pour les dashboards BI.
- Utilisez les sorties enrichies (thèmes, intensité) pour alimenter les tableaux de bord de contenu et la gestion produit.

Recommandations pour la production
- Containeriser les services et orchestrer via `docker-compose` ou Kubernetes.
- Ajouter une pipeline CI pour tests unitaires et validation du modèle.
- Mettre en place des métriques (Prometheus/Grafana) et la surveillance des topics Kafka.

Prochaines améliorations suggérées
- Fichier `requirements.txt` et `Dockerfile` pour chaque composant.
- Exemple `docker-compose.yml` avec Kafka + Zookeeper + Postgres + API.
- Scripts d'évaluation du modèle et jeux de données de validation.

Support & contribution
- Pour contribuer, créez une issue ou une PR sur le dépôt. Consultez l'historique Git pour les auteurs et contributeurs.
