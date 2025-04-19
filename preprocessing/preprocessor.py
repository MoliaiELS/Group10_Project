import pandas as pd
import re
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer

class TextPreprocessor:
    def __init__(self, n_features=2**20, ngram_range=(1, 1)):
        self.n_features = n_features  # 默认使用2^20个特征
        self.ngram_range = ngram_range  # 控制n-grams的范围
        self.train_df=None
        self.vald_df=None

    def load_data(self, train_path, valid_path):
        """Load the parquet files."""
        # 使用 iterator 分块读取大数据
        self.train_df = pd.read_parquet(train_path, engine='pyarrow')
        self.valid_df = pd.read_parquet(valid_path, engine='pyarrow')

    def clean_text(self, text):
        """Clean the text data."""
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
        text = re.sub(r'\s+', ' ', text).strip().lower()  # Normalize spaces and case
        return text
       
    def apply_cleaning(self):
    #原地修改，减少临时对象
        for df in [self.train_df, self.valid_df]:
            df['cleaned_text'] = df['text'].map(self.clean_text, na_action='ignore')

    def generate_character_ngrams(self, text, k=5):
    #生成器模式返回 n-grams，避免列表存储
        text = f"^{text}$"
        for i in range(len(text) - k + 1):
            yield text[i:i+k]  # 或 yield hash(text[i:i+k])  # 直接生成哈希值节省内存  

    def get_ngrams_for_minhash(self, k=5):
        """分批处理 + 生成器"""
        train_ngrams = self.train_df['cleaned_text'].map(
            lambda x: {ngram for ngram in self.generate_character_ngrams(x, k)})
        valid_ngrams = self.valid_df['cleaned_text'].map(
            lambda x: {ngram for ngram in self.generate_character_ngrams(x, k)})
        return train_ngrams, valid_ngrams

    def tokenize_text_for_simhash(self, text):
        """Tokenize text into words for SimHash (can be customized for specific needs)."""
        # 这里使用简单的空格分词，可以根据需求替换为更复杂的分词器（如nltk、spacy等）
        return text.split()

    def get_token_frequency_dict(self, text):
        """Convert text into a token frequency dictionary for SimHash."""
        tokens = self.tokenize_text_for_simhash(text)
        freq_dict = {}
        for token in tokens:
            freq_dict[token] = freq_dict.get(token, 0) + 1
        return freq_dict

    def get_simhash_inputs(self):
        """Generate token frequency dictionaries for all documents (for SimHash)."""    
        train_token_freqs = self.train_df['cleaned_text'].apply(self.get_token_frequency_dict)
        valid_token_freqs = self.valid_df['cleaned_text'].apply(self.get_token_frequency_dict)
        return train_token_freqs, valid_token_freqs

    def feature_extraction(self):
        """Extract features using HashingVectorizer with n-grams."""
        vectorizer = HashingVectorizer(
            n_features=self.n_features,
            ngram_range=self.ngram_range,
            analyzer='char'  # 使用字符级n-grams而不是单词级
        )
        self.train_features = vectorizer.fit_transform(self.train_df['cleaned_text'])
        self.valid_features = vectorizer.transform(self.valid_df['cleaned_text'])
        return self.train_features, self.valid_features

    def preprocess(self, train_path, valid_path):
        """Run the complete preprocessing pipeline."""
        self.load_data(train_path, valid_path)
        self.apply_cleaning()
        return self.feature_extraction()
