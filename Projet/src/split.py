import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv("../data/clean/paraphrased_reviews.csv")


assert {"clean_text", "paraphrased_text", "label"}.issubset(df.columns)


df_original = df[["clean_text", "label"]].rename(columns={"clean_text": "text"})
df_augmented = df[["paraphrased_text", "label"]].rename(columns={"paraphrased_text": "text"})


df_all = pd.concat([df_original, df_augmented], ignore_index=True).dropna()

# 80/10/10
train_df, temp_df = train_test_split(df_all, test_size=0.2, stratify=df_all["label"], random_state=42)
dev_df, test_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df["label"], random_state=42)


train_df.to_csv("../data/clean/train/train.csv", index=False, encoding="utf-8")
dev_df.to_csv("../data/clean/train/dev.csv", index=False, encoding="utf-8")
test_df.to_csv("../data/clean/train/test.csv", index=False, encoding="utf-8")

print("train file have be saved as：")
print("   - ../data/train/clean/train.csv")
print("   - ../data/clean/train/dev.csv")
print("   - ../data/clean/train/test.csv")
