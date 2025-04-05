import random

# 自定义线性同余生成器（LCG）作为哈希函数
def simple_hash(value, seed=42):
    # 使用线性同余法生成哈希值
    # LCG 参数: a, c, m
    a = 1664525  # 经典的线性同余法常数
    c = 1013904223
    m = 2**32  # 32位数空间
    hash_value = (a * seed + c) % m
    return hash_value

# BitSample 算法的实现
class BitSample:
    def __init__(self, bit_size=128, seed = 1, num_hashes=5):
        self.bit_size = bit_size  # 位向量的大小
        self.num_hashes = num_hashes  # 哈希函数的数量
        self.bit_vectors = []

    def add(self, data):
        """
        对于给定的数据，使用多个哈希函数生成多个哈希值并填充到位向量中
        """
        bit_vector = [0] * self.bit_size  # 初始化一个位向量
        for i in range(self.num_hashes):
            hash_value = simple_hash(data, i)  # 对数据应用哈希函数
            index = hash_value % self.bit_size  # 将哈希值映射到位向量的索引上
            bit_vector[index] = 1  # 设置对应位为1
        self.bit_vectors.append(bit_vector)

    def jaccard_similarity(self, other):
        """
        计算两个集合之间的 Jaccard 相似度
        """
        intersection = 0
        union = 0
        for bit_vec1, bit_vec2 in zip(self.bit_vectors, other.bit_vectors):
            intersection += sum([1 for b1, b2 in zip(bit_vec1, bit_vec2) if b1 == b2 == 1])
            union += sum([1 for b1, b2 in zip(bit_vec1, bit_vec2) if b1 == 1 or b2 == 1])
        return intersection / union if union > 0 else 0

# 示例代码：创建两个集合并计算它们的 Jaccard 相似度
if __name__ == "__main__":
    # 创建 BitSample 实例
    sample1 = BitSample(bit_size=128, num_hashes=5)
    sample2 = BitSample(bit_size=128, num_hashes=5)

    # 向集合中添加元素
    sample1.add("apple")
    sample1.add("banana")
    sample1.add("cherry")

    sample2.add("banana")
    sample2.add("cherry")
    sample2.add("date")

    # 计算 Jaccard 相似度
    similarity = sample1.jaccard_similarity(sample2)
    print(f"Jaccard 相似度: {similarity}")
