import pandas as pd

def label_reviews(input_path, output_path):
    """
    Reviews are labeled according to their score (negative / positive).
    A score ≤ 0.5 is negative, > 0.5 is positive.
    """
    df = pd.read_csv(input_path)

    def label_score(score):
        return "negative" if score <= 0.5 else "positive"

    df["label"] = df["score"].apply(label_score)

    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Labeled data saved to: {output_path}")


if __name__ == "__main__":
    label_reviews(
        input_path="../data/clean/filtered_reviews_cleaned.csv",
        output_path="../data/clean/labeled_reviews.csv"
    )
