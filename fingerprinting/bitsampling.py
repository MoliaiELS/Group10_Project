import numpy as np
import random

class BitSamplingHash:
    def __init__(self, num_bits=64, sample_size=8, seed=None):
        """
        num_bits: 原始向量长度（如 Simhash 位数）
        sample_size: 需要采样的位数
        seed: 随机种子（可复现）
        """
        self.num_bits = num_bits
        self.sample_size = sample_size
        self.rng = random.Random(seed)
        self.selected_bits = sorted(self.rng.sample(range(num_bits), sample_size))

    def hash(self, fingerprint):
        """
        fingerprint: 一个整数（Simhash 输出）
        返回采样后的bit列表（也可转为整数）
        """
        return [(fingerprint >> (self.num_bits - 1 - i)) & 1 for i in self.selected_bits]

    def hamming_distance(self, bits1, bits2):
        return sum(b1 != b2 for b1, b2 in zip(bits1, bits2))

    def similarity(self, bits1, bits2):
        return 1 - self.hamming_distance(bits1, bits2) / self.sample_size

if __name__ == "__main__":
    # 示例
    num_bits = 64
    sample_size = 8
    seed = 42

    # 创建 BitSamplingHash 实例
    bsh = BitSamplingHash(num_bits, sample_size, seed)

    # 假设有一个 Simhash 输出的指纹
    fingerprint1 = 0b1101101010110101010101010101010101010101010101010101010101010101
    fingerprint2 = 0b1101101110110101010101010101010101010101010101010101010101010101

    # 进行哈希采样
    bits1 = bsh.hash(fingerprint1)
    bits2 = bsh.hash(fingerprint2)

    # 计算相似度
    similarity_score = bsh.similarity(bits1, bits2)
    print(f"Similarity Score: {similarity_score:.2f}")