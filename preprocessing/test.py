if __name__ == "__main__":
    vectorizer = TextVectorizer(n_features=2**20)
    train_features, valid_features = vectorizer.preprocess("0000.parquet", "validate_0000.parquet")
    
    print("训练特征形状:", train_features.shape)
    print("验证特征形状:", valid_features.shape)
