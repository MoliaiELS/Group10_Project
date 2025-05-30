from collections import defaultdict
import numpy as np
import random
import sys
import time
import logging
from functools import reduce
from pathlib import Path

# 添加 fingerprinting 目录到 sys.path
# 将父目录路径添加到 Python 的模块搜索路径中，以便可以导入 fingerprinting 目录下的模块
parent_dir = Path.cwd().parent.resolve()
sys.path.append(str(parent_dir / 'fingerprinting'))

# 修改导入路径以匹配实际文件结构
from fingerprinting.minhash import MinHash
from fingerprinting.simhash import Simhash
from fingerprinting.bitsampling import BitSamplingHash

logging.getLogger().setLevel(logging.INFO)  # 设置日志级别为 INFO

class LSHCache:
    def __init__(self, n=100, b=20, r=5, max_shingle=3, hash_method='minhash', f=None):
        # 初始化 LSHCache 类的参数
        self._n = n  # MinHash 签名的长度
        self._b = b  # LSH 的带数（bands）或采样器数量
        self._r = r  # 每个带的行数（rows）或采样位数
        self._max_shingle = max_shingle  # 最大 shingle 长度
        self.hash_method = hash_method.lower()  # 哈希方法，支持 'minhash', 'simhash', 'bitsampling'
        self._f = f  # Simhash/BitSampling 的指纹长度

        # 参数检查和初始化
        if self.hash_method == 'minhash':
            # 检查 MinHash 的参数是否匹配
            assert self._b * self._r == self._n, f'Minhash bands/rows/length mismatch: _b*_r != _n, _b={self._b}, _r={self._r}, _n={self._n}'
        elif self.hash_method == 'simhash':
            # 检查 Simhash 的参数是否匹配
            if self._f is None:
                self._f = self._b * self._r  # 默认 f = b * r
            assert self._f == self._b * self._r, f'Simhash fingerprint length mismatch: f must equal b*r, f={self._f}, b={self._b}, r={self._r}'
            assert self._f % 8 == 0, f'Simhash fingerprint length must be a multiple of 8, got f={self._f}'
        elif self.hash_method == 'bitsampling':
            # 检查 BitSampling 的参数是否匹配
            if self._f is None:
                self._f = 64  # 默认指纹长度
            assert self._f >= self._r, f'BitSampling requires f >= r, got f={self._f}, r={self._r}'
            # 初始化 b 个 BitSamplingHash 实例，每个采样 r 位
            self._bitsamplers = [BitSamplingHash(num_bits=self._f, sample_size=self._r, seed=i) for i in range(self._b)]
        else:
            raise ValueError(f"Unsupported hash_method: {self.hash_method}. Use 'minhash', 'simhash', or 'bitsampling'.")

        assert self._max_shingle > 0, f'_max_shingle must be greater than 0. Current _max_shingle={self._max_shingle}'

        # 初始化内部变量
        self._seen = set()  # 存储已插入的文档 ID
        self._shingles = {}  # 存储 shingle 到 ID 的映射
        self._counter = 0  # 计数器，用于生成唯一的 shingle ID
        self._num_docs = 0  # 已插入的文档数量
        self._most_recent_insert = 0  # 最近插入文档的时间戳
        self._cache = [defaultdict(list) for _ in range(self._b)]  # LSH 的缓存结构
        self.docs = {}  # 初始化 docs 属性，用于存储文档 ID 和内容的映射

    def _get_shingle_vec(self, doc):
        # 将文档分解为 shingle 向量
        logging.debug('entering with len(doc)=%d', len(doc))
        v = {}
        doc = list(doc)  # 将文档转换为列表
        for n in range(self._max_shingle):
            doc.insert(0, '<start>')  # 在文档开头插入占位符
            for j in range(len(doc) - n):
                s = doc[j:j+n+1]  # 提取长度为 n+1 的 shingle
                if tuple(s) not in self._shingles:
                    self._shingles[tuple(s)] = self._counter  # 为新的 shingle 分配唯一 ID
                    self._counter += 1
                v[self._shingles[tuple(s)]] = 1  # 将 shingle ID 添加到向量中
        return v

    def _get_sig(self, doc):
        # 生成文档的签名
        shingle_vec = self._get_shingle_vec(doc)
        logging.debug('got shingle_vec: len(shingle_vec)=%d', len(shingle_vec))

        if self.hash_method == 'minhash':
            # 使用 MinHash 生成签名
            minhash = MinHash(d=self._n, seed=1)
            for shingle_id in shingle_vec.keys():
                minhash.add(str(shingle_id).encode('utf-8'))
            signature = minhash.hashvalues
            logging.debug('got minhash sig: len(sig)=%d', len(signature))
        elif self.hash_method in ['simhash', 'bitsampling']:
            # 对于 Simhash 和 BitSampling，先生成 Simhash 指纹
            features = [str(shingle_id) for shingle_id in shingle_vec.keys()]
            simhash = Simhash(features, f=self._f)
            signature = simhash.fingerprint
            logging.debug('got simhash sig: fingerprint=%d', signature)
        else:
            raise ValueError(f"Unknown hash_method: {self.hash_method}")

        return signature

    def _get_lsh(self, sig):
        # 根据签名生成 LSH
        lsh = []
        if self.hash_method == 'minhash':
            # MinHash: 将向量分成 b 个带，每带 r 个元素
            for i in range(self._b):
                band = sig[i * self._r : i * self._r + self._r]
                lsh.append(hash(tuple(band)))
        elif self.hash_method == 'simhash':
            # Simhash: 将指纹的二进制位分成 b 个带，每带 r 位
            bitstring = bin(sig)[2:].zfill(self._f)
            for i in range(self._b):
                start = i * self._r
                end = start + self._r
                band_bits = bitstring[start:end]
                band_int = int(band_bits, 2)
                lsh.append(band_int)
        elif self.hash_method == 'bitsampling':
            # BitSampling: 使用 b 个采样器，每采样 r 位
            for sampler in self._bitsamplers:
                sampled_bits = sampler.hash(sig)
                band_int = int(''.join(map(str, sampled_bits)), 2)  # 将位列表转为整数
                lsh.append(band_int)
        return lsh

    def _get_lsh_from_doc(self, doc):
        # 从文档生成 LSH
        logging.debug('got tokenized doc: len(doc)=%d', len(doc))
        sig = self._get_sig(doc)
        lsh = self._get_lsh(sig)
        return lsh

    def _insert_lsh(self, lsh, doc_id, date_added):
        # 插入 LSH 到缓存中
        if doc_id in self._seen:
            return
        else:
            dup_buckets = []
            self._num_docs += 1
            if date_added > self._most_recent_insert:
                self._most_recent_insert = date_added
            self._seen.add(doc_id)
            for i, band_bucket in enumerate(lsh):
                if doc_id not in self._cache[i][band_bucket]:
                    dup_buckets.append(self._cache[i][band_bucket])
                    self._cache[i][band_bucket].append(doc_id)
            return dup_buckets

    @classmethod
    def prepare_dup_buckets(cls, buckets, id=None):
        # 准备重复的桶
        all_ids = list(set(reduce(list.__add__, buckets, [])))
        if id and id in all_ids:
            all_ids.remove(id)
        return all_ids

    def get_dup_buckets(self, doc):
        # 获取文档的重复桶
        if not doc:
            print('[process_doc]\tfound empty doc, skipping')
            return
        lsh = self._get_lsh_from_doc(doc)
        dups = [self._cache[i][band_bucket] for i, band_bucket in enumerate(lsh)]
        return dups

    def get_dups(self, doc, id):
        # 获取文档的重复项
        lsh = self._get_lsh_from_doc(doc)
        simhash = Simhash(doc, f=self._f) if self.hash_method in ['simhash', 'bitsampling'] else None
        candidates = set()
        for i, band_bucket in enumerate(lsh):
            for cand_id in self._cache[i][band_bucket]:
                candidates.add(cand_id)
        dups = []
        if simhash:  # 仅对 Simhash 和 BitSampling 使用汉明距离阈值
            for cand_id in candidates:
                cand_doc = self.docs[cand_id]  # 使用类属性 self.docs
                cand_simhash = Simhash(cand_doc.split(), f=self._f)
                hamming_threshold = 3
                if simhash.hamming_distance(cand_simhash) <= hamming_threshold:  # 自定义阈值
                    dups.append(cand_id)
        else:  # MinHash 使用默认桶匹配
            dups = self.prepare_dup_buckets(self.get_dup_buckets(doc), id)
        return dups

    def insert(self, doc, id, date_added=int(time.time()), passive=True):
        # 插入文档到缓存中
        self.docs[id] = doc  # 将文档存储到 self.docs 中
        lsh = self._get_lsh_from_doc(doc)
        logging.debug('id: %d lsh: %s', id, lsh)
        dup_buckets = self._insert_lsh(lsh, id, date_added)
        return self.prepare_dup_buckets(dup_buckets, id=id)

    def insert_batch(self, doc_tuples):
        # 批量插入文档
        dup_buckets = {}
        print(f'[add_docs]\tentering with len(doc_tuples)={len(doc_tuples)}')
        for i, doc_tuple in enumerate(doc_tuples):
            if i % 100 == 0:
                print(f'\r[add_docs]\tprocessed {i} / {len(doc_tuples)} docs:', end='')
            dup_buckets[i] = self.insert(*doc_tuple)
        print()
        return dup_buckets

    def num_docs(self):
        # 返回文档数量
        return self._num_docs

    def most_recent_insert(self):
        # 返回最近插入的时间戳
        return self._most_recent_insert

    def num_shingles(self):
        # 返回 shingle 的数量
        return self._counter