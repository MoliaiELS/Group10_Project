import hashlib
import numpy as np
import re
from itertools import groupby
from collections.abc import Iterable

class Simhash:
    def __init__(self, value, f=64, hashfunc=None, token_pattern=r'[a-zA-Z]{2,}'):
        if hashfunc is None:
            self.hashfunc = lambda x: int.from_bytes(
                hashlib.sha1(x).digest(), byteorder='big'
            )
            self._hashbits = 160  # sha1 输出位数
        elif callable(hashfunc):
            self.hashfunc = hashfunc
            self._hashbits = 256  # 默认 assume 高位保留使用 256，用户自定义需保证位数足够
        else:
            raise ValueError("哈希函数必须可调用")

        if f % 8 != 0:
            raise ValueError("指纹位数必须是8的倍数")
        self.f = f
        self.reg = re.compile(token_pattern)

        if isinstance(value, str):
            self.build_by_text(value)
        elif isinstance(value, Iterable):
            self.build_by_features(value)
        else:
            raise TypeError("输入类型必须是字符串或可迭代对象")

    def _tokenize(self, text):
        return [word.lower() for word in re.findall(self.reg, text) if len(word) >= 3]

    def _truncate_hash(self, h):
        if not isinstance(h, int):
            raise TypeError("hashfunc must return int")
        return h >> (self._hashbits - self.f)

    def build_by_text(self, text):
        words = self._tokenize(text)
        features = list(self._count_features(words))
        self.build_by_features(features)

    def _count_features(self, words):
        sorted_words = sorted(words)
        for word, group in groupby(sorted_words):
            yield (word, sum(1 for _ in group))

    def build_by_features(self, features):
        vector = np.zeros(self.f, dtype=np.int64)
        processed_features = []
        for item in features:
            if isinstance(item, tuple) and len(item) == 2:
                token, weight = item
                if weight <= 0:
                    raise ValueError("权重必须为正值")
            else:
                token = item
                weight = 1
            processed_features.append((token, weight))

        for token, weight in processed_features:
            h = self.hashfunc(token.encode())
            hash_val = self._truncate_hash(h)
            bits = np.array([(hash_val >> i) & 1 for i in range(self.f)])
            vector += np.where(bits, weight, -weight)

        self.fingerprint = int(''.join(
            '1' if bit > 0 else '0'
            for bit in vector
        ), 2)

    def hamming_distance(self, other):
        xor = self.fingerprint ^ other.fingerprint
        return bin(xor).count('1')

    def similarity(self, other):
        return 1 - self.hamming_distance(other) / self.f

    @property
    def hex(self):
        return f"{self.fingerprint:0{self.f//4}x}"

# 测试代码
if __name__ == "__main__":
    text = "The quick brown fox jumps over the lazy dog"
    text2 = "The fast brown fox jumps over the lazy dog"
    
    hash1 = Simhash(text, f=8)
    hash2 = Simhash(text2, f=8)

    print(f"文本1指纹: {hash1.hex}")
    print(f"文本2指纹: {hash2.hex}")
    print(f"汉明距离: {hash1.hamming_distance(hash2)}")
    print(f"相似度: {hash1.similarity(hash2):.2f}")