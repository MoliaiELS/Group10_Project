import pandas as pd
import re
from sklearn.feature_extraction.text import HashingVectorizer

class TextPreprocessor:
    def __init__(self, n_features=2**20):
        self.n_features = n_features  # 默认使用2^20个特征

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
        """Extract features using HashingVectorizer."""
        vectorizer = HashingVectorizer(n_features=self.n_features)
        self.train_features = vectorizer.fit_transform(self.train_df['cleaned_text'])
        self.valid_features = vectorizer.transform(self.valid_df['cleaned_text'])

        # 注意：HashingVectorizer不会返回特征名称
        return self.train_features, self.valid_features

    def preprocess(self, train_path, valid_path):
        """Run the complete preprocessing pipeline."""
        self.load_data(train_path, valid_path)
        self.apply_cleaning()
        return self.feature_extraction()

"""usage example
if __name__ == "__main__":
    preprocessor = TextPreprocessor(n_features=2**20)  # 可以调整特征数量
    train_features, valid_features = preprocessor.preprocess("0000.parquet", "validate_0000.parquet")

    # train_features 和 valid_features 是稀疏矩阵，可以用于后续分析或建模
    print("训练特征形状:", train_features.shape)
"""
    print("验证特征形状:", valid_features.shape)
