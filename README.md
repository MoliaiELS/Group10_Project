# Group11_Project

## File Structure

GROUP10_PROJECT\
├── README.md            \# 安装与运行说明\
├── requirements.txt     \# 依赖库\
├── main.py              \# 主入口文件（新增）\
├── preprocessing/\
│   ├── text_cleaner.py  \# 文本清洗\
│   └── vectorizer.py    \# 特征向量化\
├── fingerprinting/\
│   ├── minhash.py       \# MinHash实现\
│   ├── simhash.py       \# SimHash实现\
│   └── bitsample.py     \# Bit Sampling实现\
├── lsh/\
│   ├── bucketing.py     \# LSH分桶策略\
│   └── candidate_pairs.py\
├── evaluation/\
│   ├── metrics.py       \# 重复率计算\
│   └── visualization.py \# 结果可视化\
└── tests/               \# 单元测试
