import sys
import os

# 添加上级目录到 sys.path
sys.path.insert(0, os.path.abspath('../..'))
import kgrams
from fingerprinting import minhash
from lsh import lsh
from lsh import example

if __name__ == "__main__":
    # 初始化预处理器
    preprocessor = TextPreprocessor(n_features=2**20, ngram_range=(3, 5))
    
    # 加载并预处理数据
    train_features, valid_features = preprocessor.preprocess("0000.parquet", "validate_0000.parquet")
    
    # 获取n-grams集合
    train_ngrams, valid_ngrams = preprocessor.get_ngrams_for_minhash(k=5)
    
    # 为训练集和验证集生成MinHash签名
    print("为训练集生成MinHash签名...")
    train_minhashes = create_minhash_signatures(train_ngrams, num_perm=128)
    
    print("\n为验证集生成MinHash签名...")
    valid_minhashes = create_minhash_signatures(valid_ngrams, num_perm=128)
    
    # 转换为矩阵并保存
    train_matrix = minhashes_to_matrix(train_minhashes)
    valid_matrix = minhashes_to_matrix(valid_minhashes)
    
    np.save("train_minhash.npy", train_matrix)
    np.save("valid_minhash.npy", valid_matrix)
    
    print("\nMinHash签名生成完成！")
    print(f"训练集签名矩阵形状: {train_matrix.shape}")
    print(f"验证集签名矩阵形状: {valid_matrix.shape}")

    test_configs = {
            "hash_method": "minhash",
            "params": {"n": 100, "b": 20, "r": 5, "max_shingle": 3, "hash_method": "minhash"}
        }
    for config in test_configs:
        run_simple_test(config["hash_method"], config["params"], docs)
