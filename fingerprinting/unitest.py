# test_minhash.py
import unittest
import numpy as np
import hashlib 
import struct

from minhash import MinHash
import my_hash as mh

def test_sha1_hash32(data):
    data = bytearray(data, 'utf-8') # 将输入数据转换为字节列表
    return struct.unpack('<I', hashlib.sha1(data).digest()[:4])[0]

class TestMinHash(unittest.TestCase):
    def setUp(self):
        self.seed = 42
        self.test_strings = [
            "apple", "banana", "cherry",
            "date", "elderberry", "fig"
        ]

    # 测试SHA-1哈希函数
    def test_sha1_hash32(self):
        # 已知测试用例（验证来源：python hashlib）
        self.assertEqual(mh.sha1_hash32("hello"), test_sha1_hash32("hello"))
        self.assertEqual(mh.sha1_hash32("minhash"), test_sha1_hash32("minhash"))
        self.assertEqual(mh.sha1_hash32("test"), test_sha1_hash32("test"))
        # 空字符串
        self.assertEqual(mh.sha1_hash32(""), test_sha1_hash32(""))

    # 测试MinHash初始化
    def test_initialization(self):
        # 默认初始化
        m = MinHash(seed=self.seed)
        self.assertEqual(len(m), 128)
        self.assertTrue(np.all(m.hashvalues == 0xFFFFFFFF))

        # 自定义hashvalues初始化
        custom_hash = [100, 200, 300]
        m = MinHash(hashvalues=custom_hash)
        self.assertTrue(np.array_equal(m.hashvalues, np.array(custom_hash, dtype=np.uint64)))

    # 测试add方法更新哈希签名
    def test_add_operation(self):
        m = MinHash(d=3, seed=self.seed)
        initial_hash = m.hashvalues.copy()

        # 第一次添加
        m.add("apple")
        self.assertFalse(np.array_equal(initial_hash, m.hashvalues))

        # 添加相同元素不应改变最小值
        prev_hash = m.hashvalues.copy()
        m.add("apple")
        self.assertTrue(np.array_equal(prev_hash, m.hashvalues))

    # 测试Jaccard相似度计算
    def test_jaccard_similarity(self):
        # 完全相同的数据
        m1 = MinHash(seed=self.seed)
        m2 = MinHash(seed=self.seed)
        for s in self.test_strings[:3]:
            m1.add(s)
            m2.add(s)
        self.assertAlmostEqual(m1.jaccard(m2), 1.0, delta=1e-6)

        # 完全不同的数据
        m3 = MinHash(seed=self.seed)
        m4 = MinHash(seed=self.seed)
        for s in self.test_strings[:3]:
            m3.add(s)
        for s in self.test_strings[3:]:
            m4.add(s)
        self.assertAlmostEqual(m3.jaccard(m4), 0.0, delta=1e-6)

        # 部分重叠（预期相似度≈0.5）
        m5 = MinHash(seed=self.seed)
        m6 = MinHash(seed=self.seed)
        for s in self.test_strings[:2]:
            m5.add(s)
            m6.add(s)
        m6.add(self.test_strings[2])
        self.assertAlmostEqual(m5.jaccard(m6), 0.666, delta=0.1)

    # 测试异常处理
    def test_error_handling(self):
        m1 = MinHash(d=128, seed=1)
        m2 = MinHash(d=128, seed=2)

        # 不同种子应抛出异常
        with self.assertRaises(ValueError):
            m1.jaccard(m2)

        # 不同哈希函数数量
        m3 = MinHash(d=64)
        with self.assertRaises(ValueError):
            m1.jaccard(m3)

    # 测试梅森素数逻辑
    def test_mersenne_prime_logic(self):
        m = MinHash(d=2, seed=self.seed)
        a, b = m.permutations

        # 验证生成的参数在合理范围内
        self.assertTrue(np.all(a > 0))
        self.assertTrue(np.all(a < (1 << 61) - 1))
        self.assertTrue(np.all(b < (1 << 61) - 1))

    # 测试边界条件
    def test_edge_cases(self):
        # 空MinHash对象比较
        m1 = MinHash(d=10)
        m2 = MinHash(d=10)
        self.assertEqual(m1.jaccard(m2), 1.0)  # 所有哈希值初始化为MAX，所以相等

        # 单个元素的最小值
        m = MinHash(d=1, hashvalues = [mh.sha1_hash32("test")])
        self.assertEqual(m.hashvalues[0], mh.sha1_hash32("test"))

if __name__ == '__main__':
    unittest.main()