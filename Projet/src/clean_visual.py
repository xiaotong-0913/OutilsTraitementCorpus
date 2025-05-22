import pandas as pd
import re 
import os
import string
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
nlp = spacy.load("en_core_web_sm")

nltk.download('punkt')
nltk.download('stopwords')


df = pd.read_csv("../data/raw/filtered_reviews.csv")
reviews = df["review"].astype(str)


stop_words = set(stopwords.words('english'))

# nettoyage
def clean_review(text):
    text = text.lower()
    text = re.sub(r"<.*?>", "", text)  
    text = re.sub(r"http\S+", "", text)  
    text = text.translate(str.maketrans('', '', string.punctuation))  
    text = re.sub(r"\d+", "", text)  
    text = re.sub(r"[^\w\s]", "", text)  
     
    doc = nlp(text)
    lemmatized = [
        token.lemma_ for token in doc
        if token.lemma_ not in stop_words and not token.is_punct and not token.is_space and len(token.lemma_) > 1
    ]
    return " ".join(lemmatized)
  

df["clean_text"] = df["review"].astype(str).apply(clean_review)

all_tokens = " ".join(df["clean_text"]).split()
word_freq = Counter(all_tokens)
top_words = word_freq.most_common(20)

df = df.drop(columns=["review"])


df.to_csv("../data/clean/filtered_reviews_cleaned.csv", index=False)
print("the cleaned file is saved as filtered_reviews_cleaned.csv")


df["longueur"] = df["clean_text"].apply(lambda x: len(x.split()))

# visualisation
# longueur des textes

plt.figure(figsize=(8, 5))
plt.hist(df["longueur"], bins=20, color='skyblue', edgecolor='black')
plt.title("Distribution de la longueur des textes")
plt.xlabel("Nombre de mots par texte")
plt.ylabel("Nombre de textes")
plt.grid(True)
plt.tight_layout()
plt.savefig("../figures/longueur_textes.png")
plt.show()


# Zipf 
all_words = " ".join(df["clean_text"]).split()
freq = Counter(all_words)
top_n = 20
most_common = word_freq.most_common(top_n)
words, freqs = zip(*most_common)

plt.figure(figsize=(12, 6))
plt.plot(words, freqs, marker="o")
plt.title("Loi de Zipf : mots les plus fréquents")
plt.xlabel("Rang")
plt.ylabel("Fréquence")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("../figures/zipf_mots_fréquents.png")
plt.show()