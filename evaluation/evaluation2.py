import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow.parquet as pq
import psutil 
# 增加了内存监控功能


# 添加项目根目录到 sys.path（确保能找到 fingerprinting 目录）
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入所需的库
from lsh.lsh import LSHCache 
import string
from preprocessing.preprocessor import TextPreprocessor

# 单一文件，单种方法 
file_path = os.path.join(os.path.dirname(__file__), 'validation-00001-of-00002.parquet')


# 定义一个函数来获取当前系统的内存使用情况
def print_memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    print(f"当前内存占用: {mem_info.rss / 1024 / 1024:.2f} MB")

# 读取 parquet 文件
try:
    print("正在读取数据文件...")
    df = pd.read_parquet(file_path)
    total_rows = len(df)
    print(f"读取到 {total_rows} 条记录")
    
    # 添加数据验证
    if total_rows == 0:
        raise ValueError("数据文件为空")
        
    # 将每一行转换为字符串并存储在列表中
    docs = []
    for index, row in enumerate(df.itertuples()):
        # 移除索引和空值
        row_values = [str(v) for v in row[1:] if pd.notna(v)]
        row_str = ' '.join(row_values)
        if row_str.strip():  # 确保不添加空字符串
            docs.append(row_str)
    
    print(f"处理后的文档数量: {len(docs)}")
except FileNotFoundError:
    print(f"找不到文件: {file_path}")
    print("请确保parquet文件位于正确的目录中")
    sys.exit(1)
except Exception as e:
    print(f"读取文件时发生错误: {e}")
    sys.exit(1)


# # 输出前五行的第二列
# try:
#     if len(df.columns) < 2:
#         raise ValueError("数据文件的列数不足，无法输出第二列")
#     print("前五行的第二列数据:")
#     print(df.iloc[:5, 1])
# except Exception as e:
#     print(f"输出第二列时发生错误: {e}")

def run_simple_test(hash_method, params, docs):
    print(f"\n=== Testing {hash_method.upper()} ===")
    cache = LSHCache(**params)
    total_docs = len(docs)
    
    # 添加索引范围验证
    def validate_duplicates(duplicates, max_index):
        """验证重复文档索引是否在有效范围内"""
        return [d for d in duplicates if 0 <= d < max_index]
    
    # 统计变量初始化
    duplicate_docs = set()
    total_pairs = 0
    dups = {}
    
    # 处理文档
    for i, doc in enumerate(docs):
        doc = doc.strip()  # Only strip whitespace, preserve punctuation and structure
        # 获取并验证重复索引
        raw_duplicates = cache.insert(doc.split(), i)
        dups[i] = validate_duplicates(raw_duplicates, total_docs)
        
        if dups[i]:
            duplicate_docs.add(i)
            duplicate_docs.update(dups[i])
            total_pairs += len(dups[i])
    # 第二阶段：输出原始的索引信息
    print("\n=== 重复文档索引信息（显示前100条） ===")
    output_count = 0
    # 遍历存储重复文档索引的字典
    for i, duplist in dups.items():
        if output_count >= 100:  # 限制输出数量
            print("\n... 更多结果已省略 ...")
            break
        if duplist:
            # 如果存在重复文档，打印原始文档的索引
            print(f"orig index: [{i}]")
            # 遍历重复文档索引列表，打印每个重复的索引，并把对应的有序数对存入op
            for dup in duplist:
                print(f"\tdup index: [{dup}]")
                # 将有序数对添加到 OrderPair 实例中
                # op.add_pair((i, dup))
                output_count += 1
        else:
            # 如果没有找到重复文档，打印提示信息
            #print(f"no dups found for doc [{i}]")
            continue
    # 第三阶段：输出统计信息
    print("\n=== 统计信息 ===")
    print(f"总文档数: {total_docs}")
    print(f"重复文档数: {len(duplicate_docs)}")
    print(f"唯一文档数: {total_docs - len(duplicate_docs)}")
    print(f"重复文档对数: {total_pairs}")
    print(f"重复率: {len(duplicate_docs)/total_docs:.2%}")
    print_memory_usage()
            
    # print(op)
    return 
    {
        'duplicate_docs': duplicate_docs,
        'total_pairs': total_pairs,
        'duplicate_rate': len(duplicate_docs)/total_docs
    }


# 处理数据并定义 docs列表
docs = []
# 处理为最简单句子
# 遍历第二列，替换标点符号为空格，并存入列表
if len(df.columns) < 2:
    raise ValueError("数据文件的列数不足，无法处理第二列")

docs = [
    row.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).strip()
    for row in df.iloc[:, 1].astype(str)
]

if __name__ == "__main__":
    # 定义测试配置列表，包含不同哈希方法及其对应的参数
    print("孩子先去吃饭吧")
    print_memory_usage()
    test_configs = [
        # {
        #     # 哈希方法为 minhash
        #     "hash_method": "minhash",
        #     # minhash 方法的参数 - more bands, fewer rows per band
        #     "params": {"n": 80, "b": 8, "r": 10, "max_shingle": 3, "hash_method": "minhash"}
        # } # ,
        # {
        #     # 哈希方法为 simhash
        #     "hash_method": "simhash",
        #     # 修正参数：确保f=b*r
        #     "params": {"b":4,
        #               "r": 32,
        #               "max_shingle": 4,
        #               "hash_method": "simhash",
        #               "f":128}
        # },
        {
            # 哈希方法为 bitsampling
            "hash_method": "bitsampling",
            # 调整后的参数：优化band和行比例
            "params": {"b": 4, 
                      "r": 32, 
                      "max_shingle": 4, 
                      "hash_method": "bitsampling", 
                      "f": 128}
        }
    ]

    # 遍历测试配置列表，对每个配置运行重复检测测试
    for config in test_configs:
        run_simple_test(config["hash_method"], config["params"], docs)


        # 暂停直到输入enter键
        # input("Press Enter to continue...")


# 别急
