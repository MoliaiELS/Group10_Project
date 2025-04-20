import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow.parquet as pq
import psutil 
import string
# 增加了内存监控功能


# 添加项目根目录到 sys.path（确保能找到 fingerprinting 目录）
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lsh.lsh import LSHCache 

# LSH算法参数说明：
# 1. num_perm: 哈希函数数量，值越大精度越高但计算越慢（默认128）
# 2. num_tables: 哈希表数量，值越大查全率越高但内存消耗越大（默认16）
# 3. threshold: 相似度阈值，高于此值视为重复（默认0.8）
# 算法流程：
# a) 初始化LSH索引：lsh = LSHCache(num_perm=128, num_tables=16)
# b) 加载数据集并生成特征向量（示例使用原始文本，实际需替换为特征向量）
# c) 插入数据到LSH索引：lsh.insert(id, features, metadata)
# d) 查询相似项：results = lsh.query(features, threshold=0.8)
# e) 统计重复率：重复数/总查询数 ×100%

# 双文件
file_path1 = os.path.join(os.path.dirname(__file__), 'test-00000-of-00002.parquet')
file_path2 = os.path.join(os.path.dirname(__file__), 'validation-00000-of-00002.parquet')

# 示例使用流程：
def run_cross_test(hash_method, params, docs1, docs2):
    """跨数据集重复检测（移植自evaluation2并修改）"""
    print(f"\n=== Testing {hash_method.upper()} ===")
    cache = LSHCache(**params)
    
    # 存储跨数据集重复对
    cross_duplicates = {}
    
    # 建立索引数据集1
    for i, doc in enumerate(docs1):
        doc = doc.strip()
        cache.insert(doc.split(), f"set1_{i}")
    
    # 查询数据集2
    for j, doc in enumerate(docs2):
        doc = doc.strip()
        duplicates = cache.insert(doc.split(), f"set2_{j}")
        if duplicates:
            cross_duplicates[f"set2_{j}"] = [d for d in duplicates if d.startswith("set1_")]
    
    # 统计输出（整合evaluation2和evaluation3的统计逻辑）
    print("\n=== 跨数据集统计 ===")
    total_pairs = sum(len(v) for v in cross_duplicates.values())
    print(f"数据集1文档数: {len(docs1)}")
    print(f"数据集2文档数: {len(docs2)}")
    print(f"跨数据集重复对数: {total_pairs}")
    print(f"重复率: {total_pairs/len(docs2):.2%}")  # 修正重复率计算公式
    
    # 内存监控（保留evaluation3的内存统计）
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    print(f"当前内存占用: {mem_info.rss / 1024 / 1024:.2f} MB")
    
    return cross_duplicates

# 移植自evaluation2的测试配置
test_configs = [
    {
        "hash_method": "minhash",
        "params": {"n": 80, "b": 8, "r": 10, "max_shingle": 3, "hash_method": "minhash"}
    },
    {
        "hash_method": "simhash", 
        "params": {"b":4, "r": 32, "max_shingle": 4, "hash_method": "simhash", "f":128}
    },
    {
        "hash_method": "bitsampling",
        "params": {"b":4, "r": 32, "max_shingle": 4, "hash_method": "bitsampling", "f":128}
    }
]

if __name__ == "__main__":
    # 加载并预处理双数据集
    df1 = pd.read_parquet(file_path1)
    df2 = pd.read_parquet(file_path2)
    
    # 使用evaluation2的预处理逻辑
    # 修正预处理代码格式错误
    docs1 = [
        row.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).strip()
        for row in df1.iloc[:, 1].astype(str)
    ]
    docs2 = [
        row.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).strip()
        for row in df2.iloc[:, 1].astype(str)
    ]

    # 运行多方法测试
    for config in test_configs:
        print(f"\n正在测试 {config['hash_method'].upper()} 方法...")
        # 添加缺失的run_cross_test函数调用参数
        cross_duplicates = run_cross_test(
            config["hash_method"],
            config["params"],
            docs1,
            docs2
        )
        # 输出前10条重复结果
        print("\n前10条跨数据集重复记录:")
        for k, v in list(cross_duplicates.items())[:10]:
            print(f"{k} -> {v}")
