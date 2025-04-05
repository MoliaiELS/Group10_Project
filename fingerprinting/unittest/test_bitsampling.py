import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simhash import Simhash
from bitsampling import BitSamplingHash

class TestBitSamplingHash(unittest.TestCase):
    def setUp(self):
        self.text1 = "The quick brown fox jumps over the lazy dog"
        self.text2 = "The fast brown fox jumps over the lazy dog"
        self.text3 = "Quantum mechanics explores particle behavior"
        self.f = 64
        self.sample_size = 8
        self.seed = 42

        # SimHash 指纹
        self.sim1 = Simhash(self.text1, f=self.f)
        self.sim2 = Simhash(self.text2, f=self.f)
        self.sim3 = Simhash(self.text3, f=self.f)

        # Bit Sampling 哈希器
        self.bsh = BitSamplingHash(num_bits=self.f, sample_size=self.sample_size, seed=self.seed)

    def test_sample_hash_length(self):
        h1 = self.bsh.hash(self.sim1.fingerprint)
        self.assertEqual(len(h1), self.sample_size)
        self.assertTrue(all(bit in [0, 1] for bit in h1))

    def test_similarity_with_similar_text(self):
        h1 = self.bsh.hash(self.sim1.fingerprint)
        h2 = self.bsh.hash(self.sim2.fingerprint)
        sim = self.bsh.similarity(h1, h2)

        self.assertGreaterEqual(sim, 0.5)
        self.assertLess(sim, 1.01)  # 容错允许 1.0

    def test_similarity_with_different_text(self):
        h1 = self.bsh.hash(self.sim1.fingerprint)
        h3 = self.bsh.hash(self.sim3.fingerprint)
        sim = self.bsh.similarity(h1, h3)

        self.assertLess(sim, 1.0)

    def test_consistent_hash_with_seed(self):
        bsh1 = BitSamplingHash(num_bits=self.f, sample_size=self.sample_size, seed=123)
        bsh2 = BitSamplingHash(num_bits=self.f, sample_size=self.sample_size, seed=123)
        self.assertEqual(bsh1.selected_bits, bsh2.selected_bits)

    def test_hash_int_output(self):
        # 额外方法：测试整数输出版本（如你加入 hash_int 方法）
        h1_bits = self.bsh.hash(self.sim1.fingerprint)
        h1_int = int("".join(map(str, h1_bits)), 2)
        self.assertIsInstance(h1_int, int)
        self.assertGreaterEqual(h1_int, 0)
        self.assertLess(h1_int, 2 ** self.sample_size)

if __name__ == "__main__":
    unittest.main()
