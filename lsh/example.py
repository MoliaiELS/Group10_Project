import pprint
import sys
import os

sys.path.insert(0, os.path.abspath('../..'))
from lsh import LSHCache  

# 数据集
docs = [
    "pig",
    "lipstick on a pig",
    "you can put lipstick on a pig",
    "you can put lipstick on a pig but it's still a pig",
    "you can put lipstick on a pig it's still a pig",
    "i think they put some lipstick on a pig but it's still a pig",
    "putting lipstick on a pig",
    "you know you can put lipstick on a pig",
    "they were going to send us binders full of women",
    "they were going to send us binders of women",
    "a b c d e f",
    "a b c d f"
]

def run_simple_test(hash_method, params, docs):
    """
    运行简单的重复检测测试并打印结果。
    """
    print(f"\n=== Testing {hash_method.upper()} ===")
    
    cache = LSHCache(**params)
    
    dups = {}
    for i, doc in enumerate(docs):
        dups[i] = cache.insert(doc.split(), i)

    for i, duplist in dups.items():
        if duplist:
            print(f"orig [{i}]: {docs[i]}")
            for dup in duplist:
                print(f"\tdup : [{dup}] {docs[dup]}")
        else:
            print(f"no dups found for doc [{i}] : {docs[i]}")

if __name__ == "__main__":
    # 测试配置
    test_configs = [
        {
            "hash_method": "minhash",
            "params": {"n": 100, "b": 25, "r": 4, "max_shingle": 1, "hash_method": "minhash"}
        },
        {
            "hash_method": "simhash",
            "params": {"b": 8, "r": 8, "max_shingle": 1, "hash_method": "simhash", "f": 64}
        },
        {
            "hash_method": "bitsampling",
            "params": {"b": 8, "r": 8, "max_shingle": 1, "hash_method": "bitsampling", "f": 64}
        }
    ]

    for config in test_configs:
        run_simple_test(config["hash_method"], config["params"], docs)