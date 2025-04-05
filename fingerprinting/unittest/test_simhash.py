import unittest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simhash import Simhash

class TestSimhash(unittest.TestCase):
    def setUp(self):
        self.text1 = "The quick brown fox jumps over the lazy dog"
        self.text2 = "The fast brown fox jumps over the lazy dog"
        self.text3 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        self.token_list = [("apple", 2), ("banana", 1), "cherry"]

    # 测试基本构建和相似度计算
    def test_text_similarity(self):
        h1 = Simhash(self.text1, f=64)
        h2 = Simhash(self.text2, f=64)
        sim = h1.similarity(h2)

        self.assertGreater(sim, 0.5)
        self.assertLess(sim, 1.0)
        self.assertEqual(h1.f, 64)
        self.assertIsInstance(h1.fingerprint, int)

    # 测试完全相同的输入
    def test_identical_texts(self):
        h1 = Simhash(self.text1, f=64)
        h2 = Simhash(self.text1, f=64)
        self.assertEqual(h1.similarity(h2), 1.0)
        self.assertEqual(h1.hamming_distance(h2), 0)

    # 测试完全不同的文本
    def test_different_texts(self):
        h1 = Simhash(self.text1, f=64)
        h3 = Simhash(self.text3, f=64)
        self.assertLess(h1.similarity(h3), 0.6)

    # 测试自定义特征构建
    def test_token_weight_input(self):
        h = Simhash(self.token_list, f=64)
        self.assertEqual(h.f, 64)
        self.assertIsInstance(h.fingerprint, int)

    # 测试短文本、小f位
    def test_small_fingerprint(self):
        h1 = Simhash(self.text1, f=8)
        h2 = Simhash(self.text2, f=8)
        sim = h1.similarity(h2)
        self.assertGreaterEqual(sim, 0.0)
        self.assertLessEqual(sim, 1.0)

    # 测试边界异常处理
    def test_invalid_inputs(self):
        with self.assertRaises(TypeError):
            Simhash(12345)  # 非字符串或可迭代

        with self.assertRaises(ValueError):
            Simhash(self.text1, f=7)  # 非8的倍数

        with self.assertRaises(ValueError):
            Simhash([("apple", -1)])  # 权重非法

        with self.assertRaises(TypeError):
            Simhash(["apple"], hashfunc=lambda x: x)  # hashfunc 不返回 int

if __name__ == '__main__':
    unittest.main()
