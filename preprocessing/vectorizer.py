from sklearn.feature_extraction.text import HashingVectorizer
from cleaner import TextCleaner  # 导入清洗模块

class TextVectorizer:
    def __init__(self, n_features=2**20):
        self.n_features = n_features
        self.cleaner = TextCleaner()  # 组合使用TextCleaner

    def vectorize(self, train_df, valid_df):
        """Extract features using HashingVectorizer."""
        vectorizer = HashingVectorizer(n_features=self.n_features)
        train_features = vectorizer.fit_transform(train_df['cleaned_text'])
        valid_features = vectorizer.transform(valid_df['cleaned_text'])
        return train_features, valid_features

    def preprocess(self, train_path, valid_path):
        """Run the complete preprocessing pipeline."""
        # 先清洗数据
        train_df, valid_df = self.cleaner.clean(train_path, valid_path)
        # 然后向量化
        return self.vectorize(train_df, valid_df)

"""usage example
if __name__ == "__main__":
    vectorizer = TextVectorizer(n_features=2**20)
    train_features, valid_features = vectorizer.preprocess("0000.parquet", "validate_0000.parquet")
    
    print("训练特征形状:", train_features.shape)
    print("验证特征形状:", valid_features.shape)
"""
