#data preprocesing for minhash using n-grams
import pandas as pd
import re
from sklearn.feature_extraction.text import HashingVectorizer

class TextPreprocessor:
    def __init__(self, n_features=2**20, ngram_range=(1, 1)):
        self.n_features = n_features  # 默认使用2^20个特征
        self.ngram_range = ngram_range  # 控制n-grams的范围

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

    def generate_character_ngrams(self, text, k=5):
        """Generate character-level k-grams for MinHash."""
        # 在文本前后添加特殊字符作为边界标记
        text = f"^{text}$"
        # 生成k长度的字符n-grams
        return [text[i:i+k] for i in range(len(text)-k+1)]

    def feature_extraction(self):
        """Extract features using HashingVectorizer with n-grams."""
        # 使用n-grams配置的HashingVectorizer
        vectorizer = HashingVectorizer(
            n_features=self.n_features,
            ngram_range=self.ngram_range,
            analyzer='char'  # 使用字符级n-grams而不是单词级
        )
        self.train_features = vectorizer.fit_transform(self.train_df['cleaned_text'])
        self.valid_features = vectorizer.transform(self.valid_df['cleaned_text'])

        return self.train_features, self.valid_features

    def get_ngrams_for_minhash(self, k=5):
        """Generate k-grams sets for MinHash processing."""
        # 为每个文档生成k-grams集合
        train_ngrams = self.train_df['cleaned_text'].apply(
            lambda x: set(self.generate_character_ngrams(x, k))
        )
        valid_ngrams = self.valid_df['cleaned_text'].apply(
            lambda x: set(self.generate_character_ngrams(x, k))
        )
        
        return train_ngrams, valid_ngrams

    def preprocess(self, train_path, valid_path):
        """Run the complete preprocessing pipeline."""
        self.load_data(train_path, valid_path)
        self.apply_cleaning()
        return self.feature_extraction()
