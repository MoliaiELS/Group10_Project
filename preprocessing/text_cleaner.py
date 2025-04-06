import pandas as pd
import re

class TextCleaner:
    def __init__(self):
        pass

    def clean_text(self, text):
        """Clean the text data."""
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
        text = re.sub(r'\s+', ' ', text).strip().lower()  # Normalize spaces and case
        return text

    def clean(self, train_path, valid_path):
        # 加载数据
        train_df = pd.read_parquet(train_path)
        valid_df = pd.read_parquet(valid_path)
        
        # 应用清洗
        train_df['cleaned_text'] = train_df['text'].apply(self.clean_text)
        valid_df['cleaned_text'] = valid_df['text'].apply(self.clean_text)
        
        return train_df, valid_df
