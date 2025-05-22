# Analyse de sentiments avec DistilBERT sur des critiques de films

## Objectif du projet

Mon objectif est de construire un modèle de classification de sentiments (positif ou négatif) à partir de critiques de films.  
Pour cela, j’ai récupéré mon corpus de travail à partir d’une ressource web (sans utiliser d’API), en scrappant le site [Rotten Tomatoes](https://www.rottentomatoes.com).

J’ai affiné le modèle pré-entraîné **DistilBERT** sur mes propres données, en utilisant la classe Trainer de Hugging Face. L’entraînement a été réalisé en 4 époques, avec évaluation à chaque époque.

Le modèle a été évalué sur un jeu de test indépendant, avec génération d’un rapport de classification et d’une matrice de confusion, montrant une précision globale de plus de 90 %.

---

## Données utilisées

Les données proviennent de Rotten Tomatoes, un site d’accès libre.

- J’ai d’abord utilisé `scraper.py` pour récupérer la liste des **20 films les plus populaires de 2025**.
- Ensuite, `scrapper_review.py` a permis de récupérer pour chaque film les **10 premières critiques**.  
  J’ai conservé les colonnes suivantes :
  - `movie`, `url`, `reviewer`, `score`, `review`
  - Les critiques sans score ont été supprimées.
  - Les scores ont été convertis en **décimales** (par exemple : `2/5 → 0.40`)  
  → Résultat : `./raw/filtered_reviews.csv`

- J’ai ensuite utilisé `label.py` pour **ajouter un label de sentiment** :
    > Les critiques sont étiquetées en fonction de leur score (négatif / positif).  
    > Un score ≤ 0,5 est considéré comme négatif, et un score > 0,5 comme positif.

  → Résultat : `labeled_reviews.csv`

- Pour enrichir le corpus, j’ai utilisé `paraphrase_reviews.py` avec le modèle `Vamsi/T5_Paraphrase_Paws` pour créer une **version paraphrasée** de chaque critique.  
  → Résultat : `paraphrased_reviews.csv`

- Enfin, le fichier `split.py` a divisé les données en trois parties :
  - `train.csv` (80 %)
  - `dev.csv` (10 %)
  - `test.csv` (10 %)

---

## Modèle pré-entraîné choisi

J’ai choisi le modèle **DistilBERT** (`distilbert-base-uncased`) pour les raisons suivantes :
- Plus léger et plus rapide que BERT
- Bonnes performances pour les tâches de classification de texte
- Compatible avec la bibliothèque Hugging Face `transformers`

---

## Fine-tuning du modèle

Le modèle a été affiné à l’aide de la classe `Trainer` fournie par Hugging Face.  
Voici les étapes principales :

1. Les labels textuels ont été encodés en entiers avec `LabelEncoder`
2. Les textes ont été tokenisés avec `DistilBertTokenizerFast`
3. Le modèle a été entraîné sur `train.csv`, avec évaluation sur `dev.csv` à chaque epoch
4. La fonction `compute_metrics` a permis de calculer automatiquement `precision`, `recall`, `f1-score`, `accuracy`

---

## Évaluation du modèle

L’évaluation a été réalisée :
- À chaque époque sur le jeu de validation (`evaluation_strategy="epoch"`)
- À la fin de l’entraînement sur le jeu de test, avec :
  - Rapport de classification (`distilbert_results.txt`)
  - Matrice de confusion visualisée (`confusion_matrix.png`)

---

## Exemple de résultats sur le jeu de test

```
              precision    recall  f1-score   support

           0       1.00      0.60      0.75        10
           1       0.89      1.00      0.94        33

    accuracy                           0.91        43
   macro avg       0.95      0.80      0.85        43
weighted avg       0.92      0.91      0.90        43
```

---

## Limites et perspectives

- Le jeu de données est déséquilibré (moins d'exemples négatifs)
- Je n’ai pas utilisé la classe `neutre` pour simplifier la tâche
- Seul un modèle léger a été utilisé (DistilBERT)

Perspectives futures :
- Tester d'autres corpus relatives
- Tester d’autres modèles (comme `roberta-base`)
- Étendre les données (plus de critiques, plus de films, plus de diversité)

---