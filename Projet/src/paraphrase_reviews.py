import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from tqdm import tqdm
import os

# Load the model and tokenizer
model_name = "Vamsi/T5_Paraphrase_Paws"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
paraphraser = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=-1)  # -1 = CPU

# Load the input CSV
input_path = os.path.join("..", "data", "clean", "labeled_reviews.csv")
df = pd.read_csv(input_path)
print(f"Loaded {len(df)} reviews")

# Truncate helper to shorten long texts
def truncate(text, max_words=30):
    return " ".join(str(text).split()[:max_words])

# Generate paraphrased output
augmented = []
for i, row in tqdm(df.iterrows(), total=len(df)):
    original = truncate(row["clean_text"])
    try:
        result = paraphraser("paraphrase: " + original, max_length=64, do_sample=False, num_return_sequences=1)
        rewritten = result[0]["generated_text"]
    except:
        rewritten = "ERROR"

    augmented.append({
        "movie": row["movie"],
        "url": row["url"],
        "reviewer": row["reviewer"],
        "score": row["score"],
        "clean_text": original,
        "paraphrased_text": rewritten
    })

# Save the output CSV
output_path = os.path.join("..", "data", "clean", "paraphrased_reviews.csv")
pd.DataFrame(augmented).to_csv(output_path, index=False)
print(f"Done. Output saved to {output_path}")
