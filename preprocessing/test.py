from vectorizer import TextVectorizer

if __name__ == "__main__":
    preprocessor = TextVectorizer(n_features=2**20)  # 可以调整特征数量
    train_features, valid_features = preprocessor.preprocess("0000.parquet", "validate_0000.parquet")

    # train_features 和 valid_features 是稀疏矩阵，可以用于后续分析或建模
    print("训练特征形状:", train_features.shape)
    print("验证特征形状:", valid_features.shape)
