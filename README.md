# SmartIDS

## Système Intelligent de Détection des Intrusions Réseau basé sur le Data Mining et le Machine Learning

Ce projet implémente un système intelligent de détection d'intrusions réseau (NIDS) basé sur la méthodologie standard **CRISP-DM** et entraîné sur le jeu de données **NSL-KDD**. Il couple une étude approfondie de Data Mining (Notebook Jupyter) à une application Web interactive de déploiement en temps réel réalisée sous **Flask**.

---

## 🚀 Fonctionnalités Clés

1. **Double Mode de Détection** :
   - **Mode Binaire** : Normal vs. Attaque (détection d'intrusion globale).
   - **Mode Multiclasse** : Classification précise en 5 catégories (Normal, DoS, Probe, R2L, U2R).
2. **Dashboard Interactif** : Une interface moderne (Dark Mode, Glassmorphism) pour visualiser les métriques globales et les tendances de menaces réseau.
3. **Graphiques Dynamiques** : Rendu interactif via **Chart.js** pour analyser les proportions d'attaques détectées.
4. **Journal d'Analyse (Historique)** : Stockage des analyses précédentes dans une base de données **SQLite** persistante avec possibilité de réviser ou supprimer les rapports.
5. **Rapports PDF Professionnels** : Génération et téléchargement automatiques d'un rapport de sécurité au format PDF à la fin de chaque scan.

---

## 📁 Structure du Projet

```text
SmartIDS/
│
├── Dataset/
│   ├── KDDTrain+.txt              # Dataset d'entraînement (téléchargé automatiquement)
│   └── KDDTest+.txt               # Dataset de test (téléchargé automatiquement)
│
├── DataMining/
│   ├── DM_Classification.ipynb    # Notebook Jupyter complet (CRISP-DM)
│   ├── model_binary.pkl           # Meilleur modèle de classification binaire
│   ├── model_multiclass.pkl       # Meilleur modèle de classification multiclasse
│   ├── scaler.pkl                 # StandardScaler pré-entraîné
│   ├── encoder.pkl                # OneHotEncoder pré-entraîné
│   └── feature_columns.pkl        # Informations sur la structure des colonnes
│
├── WebApp/
│   ├── app.py                     # Serveur Flask principal
│   ├── database.db                # Base de données SQLite de l'historique (auto-générée)
│   │
│   ├── templates/                 # Interfaces HTML (Jinja2)
│   │     ├── base.html            # Layout commun
│   │     ├── index.html           # Tableau de bord principal
│   │     ├── upload.html          # Formulaire d'analyse de fichier
│   │     ├── result.html          # Affichage des prédictions et graphiques
│   │     ├── history.html         # Journal d'analyse
│   │     └── about.html           # Description du projet et du dataset
│   │
│   ├── static/
│   │     ├── css/
│   │     │     └── style.css      # Design moderne de l'interface
│   │     ├── js/
│   │     │     └── main.js        # Scripts de navigation et graphiques Chart.js
│   │     └── images/
│   │
│   ├── uploads/                   # Dossier temporaire pour les analyses
│   └── reports/                   # Dossier pour les rapports PDF générés
│
├── RunApp.ipynb                   # Fichier pour démarrer l'application depuis Jupyter
├── requirements.txt               # Liste des dépendances Python
└── README.md                      # Présentation du projet
```

---

## ⚙️ Installation & Lancement

### Prérequis

Avoir installé **Python 3.8+** ou une distribution **Anaconda**.

### 1. Installation des dépendances

Installez toutes les bibliothèques requises en exécutant la commande suivante dans votre terminal :

```bash
pip install -r requirements.txt
```

### 2. Partie I : Entraînement des modèles (Data Mining)

Si vous souhaitez exécuter ou comprendre le processus d'analyse exploratoire, de prétraitement et d'entraînement des modèles :
1. Lancez **Jupyter Notebook**.
2. Ouvrez le fichier `DataMining/DM_Classification.ipynb`.
3. Exécutez l'ensemble des cellules pour suivre la méthodologie **CRISP-DM**.

*(Remarque : Les modèles finaux `model_binary.pkl` et `model_multiclass.pkl` ainsi que les objets de transformation seront sauvegardés à la fin du notebook).*

### 3. Partie II : Lancement de l'application Web

Vous pouvez démarrer le serveur Web de deux manières :

#### Option A (Recommandée) : Depuis Jupyter Notebook
1. Ouvrez le fichier de raccourci `RunApp.ipynb` à la racine du projet.
2. Exécutez la dernière cellule contenant la commande `!python WebApp/app.py`.

#### Option B : Depuis le Terminal
Exécutez la commande suivante à la racine du projet :

```bash
python WebApp/app.py
```

Une fois le serveur démarré, ouvrez votre navigateur internet et accédez à l'adresse suivante :
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🛠️ Technologies Utilisées

- **Manipulation de Données** : Pandas, NumPy
- **Visualisation de Modélisation** : Matplotlib, Seaborn
- **Machine Learning** : Scikit-learn, Joblib
- **Serveur Web** : Flask (Python)
- **Base de Données** : SQLite (SQL)
- **Design Front-End** : HTML5, CSS3 (Custom Glassmorphism), JavaScript (Chart.js), FontAwesome
- **Génération de Rapports** : FPDF2
