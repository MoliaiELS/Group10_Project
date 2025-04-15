from preprocessor import TextPreprocessor

if __name__ == "__main__":
    preprocessor = TextPreprocessor(n_features=2**20, ngram_range=(3, 5))
    preprocessor.load_data('train.parquet', 'valid.parquet')
    preprocessor.apply_cleaning()
    train_features, valid_features = preprocessor.feature_extraction()
    #input for minhash
    train_ngrams, valid_ngrams = preprocessor.get_ngrams_for_minhash()
    #input for simhash
    train_token_freqs, valid_token_freqs = preprocessor.get_simhash_inputs()
    train_features, valid_features = preprocessor.preprocess('train.parquet', 'valid.parquet')
