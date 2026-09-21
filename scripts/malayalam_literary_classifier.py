# ==============================================================================
# Malayalam Literary Genre Classification
# MALO - Malayalam Literary Ontology Project
# ==============================================================================

import sqlite3
import random
import re
from collections import OrderedDict

import nltk
from nltk.tokenize import word_tokenize


# ==============================================================================
# Step 0: Download NLTK resources
# ==============================================================================

nltk.download("punkt")
nltk.download("punkt_tab")


# ==============================================================================
# Step 1: Database Setup & Malayalam Dataset
# ==============================================================================

conn = sqlite3.connect("malayalam_literature.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS literary_works")

c.execute("""
CREATE TABLE literary_works (
    workTitle TEXT,
    workText TEXT,
    workID TEXT,
    category TEXT
)
""")


def populate_malayalam_data():
    """Populate SQLite with sample Malayalam literary excerpts."""

    poetry_samples = [
        (
            "കവിത 1",
            "ചങ്ങമ്പുഴ കൃഷ്ണപിള്ളയുടെ രമണൻ എന്ന കാവ്യം പ്രേമകഥയാണ്. "
            "വനമാലയും കുയിലുകളും നിറഞ്ഞ ഗ്രാമീണ സൗന്ദര്യം.",
            "p1"
        ),
        (
            "കവിത 2",
            "കുമാരനാശാന്റെ വീണപൂവ് ജീവിതത്തിന്റെ അസ്ഥിരതയെക്കുറിച്ച് "
            "ഓർമ്മിപ്പിക്കുന്നു. പുഷ്പത്തിന്റെ ജനനവും മരണവും.",
            "p2"
        ),
        (
            "കവിത 3",
            "വള്ളത്തോളിന്റെ കവിതകൾ ദേശസ്നേഹവും പ്രകൃതിഭംഗിയും "
            "നിറഞ്ഞവയാണ്. മാതൃഭൂമിക്ക് പ്രണാമം.",
            "p3"
        )
    ]

    novel_samples = [
        (
            "നോവൽ 1",
            "വൈക്കം മുഹമ്മദ് ബഷീറിന്റെ ബാല്യകാലസഖി പ്രണയവും "
            "അതിജീവനവും പറയുന്ന മനോഹരമായ നോവലാണ്. "
            "മജീദും സുഹറയും കഥാപാത്രങ്ങളാണ്.",
            "n1"
        ),
        (
            "നോവൽ 2",
            "തകഴി ശിവശങ്കരപ്പിള്ളയുടെ ചെമ്മീൻ കടലോരത്തെ "
            "മനുഷ്യരുടെ ജീവിതവും വിശ്വാസങ്ങളും ചിത്രീകരിക്കുന്നു. "
            "കറുത്തമ്മയും പരീക്കുട്ടിയും.",
            "n2"
        ),
        (
            "നോവൽ 3",
            "എം ടി വാസുദേവൻ നായരുടെ രണ്ടാമൂഴം മഹാഭാരത കഥയെ "
            "ഭീമന്റെ കാഴ്ചപ്പാടിലൂടെ പുനരാഖ്യാനം ചെയ്യുന്നു.",
            "n3"
        )
    ]

    for _ in range(40):

        # Add poetry
        title, text, work_id = random.choice(poetry_samples)

        c.execute(
            "INSERT INTO literary_works VALUES (?, ?, ?, ?)",
            (
                title,
                text,
                work_id + str(random.randint(100, 999)),
                "kavitha"
            )
        )

        # Add novel
        title, text, work_id = random.choice(novel_samples)

        c.execute(
            "INSERT INTO literary_works VALUES (?, ?, ?, ?)",
            (
                title,
                text,
                work_id + str(random.randint(100, 999)),
                "novel"
            )
        )

    conn.commit()


populate_malayalam_data()


# ==============================================================================
# Step 2: Malayalam Preprocessing & Tokenization
# ==============================================================================

malayalam_stopwords = {
    "എന്ന",
    "ഒരു",
    "ആണ്",
    "ഉള്ള",
    "എന്ന്",
    "ഈ",
    "അത്",
    "മറ്റും",
    "അവർ",
    "എല്ലാം",
    "കൂടെ",
    "അല്ലങ്കിൽ",
    "ഏറെ",
    "വളരെ"
}


def clean_malayalam_text(sql_query):
    """Retrieve and preprocess Malayalam literary texts."""

    c.execute(sql_query)
    rows = c.fetchall()

    raw_word_list = []
    processed_documents = []

    for row in rows:

        title, body = row[0], row[1]

        full_text = f"{title} {body}"

        # Keep Malayalam Unicode characters and whitespace
        clean_chars = re.sub(
            r"[^\u0D00-\u0D7F\s]",
            "",
            full_text
        )

        # Tokenize
        tokens = word_tokenize(clean_chars)

        # Remove stopwords and very short tokens
        filtered_words = [
            word
            for word in tokens
            if word not in malayalam_stopwords
            and len(word) > 1
        ]

        raw_word_list.extend(filtered_words)
        processed_documents.append(filtered_words)

    return processed_documents, raw_word_list


# ==============================================================================
# Process both literary categories
# ==============================================================================

categories = [
    "kavitha",
    "novel"
]

data = {}

for category in categories:

    query = f"""
    SELECT workTitle, workText
    FROM literary_works
    WHERE category = '{category}'
    """

    documents, words = clean_malayalam_text(query)

    # Calculate word frequencies
    frequency_distribution = nltk.FreqDist(words)

    # Words occurring only once
    hapaxes = set(
        frequency_distribution.hapaxes()
    )

    cleaned_documents = []
    final_word_list = []

    for document in documents:

        cleaned_document = [
            word
            for word in document
            if word not in hapaxes
        ]

        cleaned_documents.append(cleaned_document)
        final_word_list.extend(cleaned_document)

    data[category] = {
        "wordMatrix": cleaned_documents,
        "all_words": final_word_list
    }


# ==============================================================================
# Step 3: Feature Extraction & Dataset Splitting
# ==============================================================================

holdout_length = 10

kavitha_docs = data["kavitha"]["wordMatrix"]
novel_docs = data["novel"]["wordMatrix"]


# Training data
labeled_train = (
    [
        (document, "kavitha")
        for document in kavitha_docs[holdout_length:]
    ]
    +
    [
        (document, "novel")
        for document in novel_docs[holdout_length:]
    ]
)


# Holdout data
holdout_data = (
    [
        (document, "kavitha")
        for document in kavitha_docs[:holdout_length]
    ]
    +
    [
        (document, "novel")
        for document in novel_docs[:holdout_length]
    ]
)


# ==============================================================================
# Build global vocabulary
# ==============================================================================

global_vocabulary = list(
    OrderedDict.fromkeys(
        data["kavitha"]["all_words"]
        +
        data["novel"]["all_words"]
    )
)


def extract_features(document):
    """
    Create Bag-of-Words binary features.

    Each feature indicates whether a vocabulary word
    occurs in the document.
    """

    document_words = set(document)

    return {
        f"contains({word})": (
            word in document_words
        )
        for word in global_vocabulary
    }


# Prepare training data
prepared_train_data = [
    (extract_features(document), label)
    for document, label in labeled_train
]


# Prepare holdout data
prepared_holdout_data = [
    extract_features(document)
    for document, label in holdout_data
]


holdout_true_labels = [
    label
    for document, label in holdout_data
]


# Shuffle training data
random.shuffle(prepared_train_data)


# 75/25 train-test split
split_index = int(
    len(prepared_train_data) * 0.75
)

train_set = prepared_train_data[:split_index]
test_set = prepared_train_data[split_index:]


# ==============================================================================
# Step 4: Naive Bayes Classification
# ==============================================================================

nb_classifier = nltk.NaiveBayesClassifier.train(
    train_set
)


accuracy = nltk.classify.accuracy(
    nb_classifier,
    test_set
)


print("\n" + "=" * 60)
print("MALAYALAM LITERARY GENRE CLASSIFICATION")
print("=" * 60)

print(
    f"\nNaive Bayes Accuracy: {accuracy:.2%}"
)


print(
    "\nTop 10 Differentiating Malayalam Terms:"
)

nb_classifier.show_most_informative_features(
    10
)


# ==============================================================================
# Step 5: Decision Tree Classification
# ==============================================================================

print("\n" + "=" * 60)
print("DECISION TREE CLASSIFICATION")
print("=" * 60)


dt_classifier = nltk.DecisionTreeClassifier.train(
    train_set
)


predicted_labels = dt_classifier.classify_many(
    prepared_holdout_data
)


# ==============================================================================
# Step 6: Confusion Matrix
# ==============================================================================

confusion_matrix = nltk.ConfusionMatrix(
    holdout_true_labels,
    predicted_labels
)


print("\nConfusion Matrix on Holdout Dataset:")
print(confusion_matrix)


# ==============================================================================
# Step 7: Example Predictions
# ==============================================================================

print("\n" + "=" * 60)
print("EXAMPLE HOLDOUT PREDICTIONS")
print("=" * 60)

for index, (true_label, predicted_label) in enumerate(
    zip(holdout_true_labels, predicted_labels),
    start=1
):

    print(
        f"Document {index}: "
        f"Actual = {true_label}, "
        f"Predicted = {predicted_label}"
    )


# ==============================================================================
# Step 8: Close database
# ==============================================================================

conn.close()

print("\n" + "=" * 60)
print("Classification pipeline completed successfully.")
print("=" * 60)
