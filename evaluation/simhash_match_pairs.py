#27测试模式运行前100个文档
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gc
import numpy as np
from preprocessing.preprocessor import TextPreprocessor
from lsh.lsh import LSHCache 
 
def detect_cross_duplicates(train_path, valid_path, n_features=2**20, ngram_range=(1,1), 
                           n=128, b=32, r=4, max_shingle=3):
    """
    检测训练集和验证集之间的重复文本（跨数据集重复）
    
    返回:
        cross_duplicates: 训练集和验证集之间的重复对列表
        stats: 包含统计信息的字典
    """
    # 1. 数据预处理
    preprocessor = TextPreprocessor(n_features=n_features, ngram_range=ngram_range)
    preprocessor.load_data(train_path, valid_path)
    preprocessor.apply_cleaning()
    train_token_freqs, valid_token_freqs = preprocessor.get_simhash_inputs()
    print("文件预处理完毕")

    #测试模式下运行前100个文档
    #train_token_freqs = train_token_freqs[:100]
    #valid_token_freqs = valid_token_freqs[:100]
    
    # 2. 初始化LSH缓存
    lsh_cache = LSHCache(n=n, b=b, r=r, max_shingle=max_shingle, hash_method='simhash')
    
    # 3. 插入训练集（直接迭代Series）
    train_ids = []
    for idx, token_freqs in enumerate(train_token_freqs):
        doc_id = f"train_{idx}"
        tokens_with_freq = [token for token, freq in token_freqs.items() for _ in range(freq)]
        lsh_cache.insert(tokens_with_freq, doc_id)
        train_ids.append(doc_id)
    print(f"已插入训练集 {len(train_ids)} 篇文档")

    # 4. 检查验证集中的文档是否与训练集重复（分块+生成器）
    cross_duplicates = []
    valid_duplicate_ids = set()
    chunk_size = 1000

    def generate_tokens(token_freqs):
        for token, freq in token_freqs.items():
            yield from [token] * freq  # Python 3.3+ 语法

    for chunk_start in range(0, len(valid_token_freqs), chunk_size):
        chunk = valid_token_freqs[chunk_start:chunk_start + chunk_size]
        for idx, token_freqs in enumerate(chunk, start=chunk_start):
            doc_id = f"valid_{idx}"
            tokens_with_freq = list(generate_tokens(token_freqs))
            dup_ids = lsh_cache.get_dups_simhash(tokens_with_freq, doc_id)
            
            for dup_id in dup_ids:
                if dup_id.startswith("train_"):
                    cross_duplicates.append((dup_id, doc_id))
        
    # 清理内存
    gc.collect()
    print(f"进度: {chunk_start + len(chunk)}/{len(valid_token_freqs)}")
    
    # 计算统计信息
    total_train = len(preprocessor.train_df)
    total_valid = len(preprocessor.valid_df)
    cross_duplicate_pairs = len(cross_duplicates)
    valid_duplicate_count = len(valid_duplicate_ids)
    
    stats = {
        "total_train_documents": total_train,
        "total_valid_documents": total_valid,
        "cross_duplicate_pairs": cross_duplicate_pairs,
        "valid_duplicate_count": valid_duplicate_count,
        "valid_duplicate_rate": valid_duplicate_count / total_valid if total_valid > 0 else 0,
    }
    
    print("\n跨数据集重复统计:")
    print(f"- test_0000文档数: {total_train}")
    print(f"- validation_0000文档数: {total_valid}")
    print(f"- 跨数据集重复对数: {cross_duplicate_pairs}")
    print(f"- 验证集中重复的文档数: {valid_duplicate_count}")
    print(f"- 验证集与训练集的重复率: {stats['valid_duplicate_rate']:.2%}")
    
    return cross_duplicates, stats

# 设置文件路径
train_path = "evaluation/test-00000-of-00002.parquet"
valid_path = "evaluation/validation-00000-of-00002.parquet"

# 检测跨数据集重复
cross_duplicates, stats = detect_cross_duplicates(
    train_path, 
    valid_path,
    n=64,      # MinHash签名长度
    b=16,       # LSH带数
    r=4,        # 每带行数
    max_shingle=3  # 使用3-shingle
)
