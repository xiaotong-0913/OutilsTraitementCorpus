import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from transformers import DataCollatorWithPadding
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
import evaluate
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# === Manually set paths ===
train_path = "../data/clean/train/train.csv"
dev_path = "../data/clean/train/dev.csv"
test_path = "../data/clean/train/test.csv"
result_file = "../results/distilbert_results.txt"

# 1. Load data
train_df = pd.read_csv(train_path)
dev_df = pd.read_csv(dev_path)
test_df = pd.read_csv(test_path)

# 2. Encode string labels into integers
label_encoder = LabelEncoder()
train_df["label"] = label_encoder.fit_transform(train_df["label"])
dev_df["label"] = label_encoder.transform(dev_df["label"])
test_df["label"] = label_encoder.transform(test_df["label"])

# 3. Convert to HuggingFace Datasets
dataset = DatasetDict({
    "train": Dataset.from_pandas(train_df),
    "validation": Dataset.from_pandas(dev_df),
    "test": Dataset.from_pandas(test_df)
})

# 4. Load tokenizer and tokenize the text data
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

def tokenize_fn(example):
    return tokenizer(example["text"], truncation=True)

tokenized_dataset = dataset.map(tokenize_fn, batched=True)

# 5. Load pre-trained model
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# 6. Data collator
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# 7. Metrics
classification_output = ""

def compute_metrics(eval_pred):
    global classification_output
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    report = classification_report(labels, predictions, digits=2)
    classification_output += "\n[Validation] Classification Report:\n" + report
    print(report)

    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='weighted')
    acc = accuracy_score(labels, predictions)
    return {
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }

# 8. Training args
training_args = TrainingArguments(
    output_dir="../models/distilbert-sentiment",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=4,
    weight_decay=0.01,
    logging_dir="../logs",
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)

# 9. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()

# 10. Final test evaluation
test_predictions = trainer.predict(tokenized_dataset["test"])
y_true = test_predictions.label_ids
y_pred = np.argmax(test_predictions.predictions, axis=1)

report = classification_report(y_true, y_pred, digits=2)
classification_output += "\n[Test] Classification Report:\n" + report
print(report)

# 11. Confusion Matrix Visualization
# Compute confusion matrix
cm = confusion_matrix(y_true, y_pred)
labels = label_encoder.classes_

# Plot the heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)


plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix (Test Set)")
plt.tight_layout()

# Save and show the plot
plt.savefig("../results/confusion_matrix.png", dpi=300)
plt.show()



# Save to file
with open(result_file, "w", encoding="utf-8") as f:
    f.write(classification_output)
    print(f"Results saved to {result_file}")
