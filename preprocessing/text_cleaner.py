import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer

class TextPreprocessor:
    def __init__(self):
        pass

    def load_data(self, train_path, valid_path):
        """Load the parquet files."""
        self.train_df = pd.read_parquet(train_path)
        self.valid_df = pd.read_parquet(valid_path)

    def clean_text(self, text):
        """Clean the text data."""
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
        text = re.sub(r'\s+', ' ', text).strip().lower()  # Normalize spaces and case
        return text

    def apply_cleaning(self):
        """Apply cleaning to the text data."""
        self.train_df['cleaned_text'] = self.train_df['text'].apply(self.clean_text)
        self.valid_df['cleaned_text'] = self.valid_df['text'].apply(self.clean_text)

    def feature_extraction(self):
        """Extract features using CountVectorizer."""
        vectorizer = CountVectorizer()
        self.train_features = vectorizer.fit_transform(self.train_df['cleaned_text'])
        self.valid_features = vectorizer.transform(self.valid_df['cleaned_text'])

        # return the feature matrix and word list
        return self.train_features, self.valid_features, vectorizer.get_feature_names_out()

    def preprocess(self, train_path, valid_path):
        """Run the complete preprocessing pipeline."""
        self.load_data(train_path, valid_path)
        self.apply_cleaning()
        return self.feature_extraction()
