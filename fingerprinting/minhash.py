import numpy as np
import hashlib

# 一些常量
_mersenne_prime = (1 << 61) - 1 # 梅森素数，用于生成伪随机数
_max_hash = (1 << 32) - 1 # 最大哈希值
_hash_range = (1 << 32) # 哈希值范围
 
class MinHash(object):
    def __init__(self, d=128, seed=1, hashfunc=hashlib.sha1, hashvalues=None, permutations=None):
        # Check the hash function.
        if not callable(hashfunc):
            raise ValueError("The hashfunc must be a callable.")
        self.hashfunc = hashfunc

        self.seed = seed
    
        # 初始化
        if hashvalues is not None: # 如果提供了hashvalues，则使用它们来初始化哈希签名
            d = len(hashvalues) # 更新d的值
            self.hashvalues = self._parse_hashvalues(hashvalues) # 解析hashvalues
        else:
            self.hashvalues = self._init_hashvalues(d) # 初始化哈希签名
            
        if permutations is not None:
            self.permutations = permutations
        else: # 如果没有提供排列，则生成随机排列
            generator = np.random.RandomState(self.seed)
            self.permutations = np.array([(generator.randint(1, _mersenne_prime, dtype=np.uint64),
                                           generator.randint(0, _mersenne_prime, dtype=np.uint64))
                                          for _ in range(d)], dtype=np.uint64).T
        
        if len(self) != len(self.permutations[0]):
            raise ValueError("Numbers of hash values and permutations mismatch")

    def _init_hashvalues(self, d):
        return np.ones(d, dtype=np.uint64)*_max_hash # 初始化为最大哈希值
    
    def _parse_hashvalues(self, hashvalues):
        parsed = []
        for hv in hashvalues:
            if isinstance(hv, (int, np.integer)):
                parsed.append(np.uint64(hv))
            elif isinstance(hv, str):
                hv = int(self.hashfunc(hv.encode()).hexdigest(), 16) % _hash_range
                parsed.append(np.uint64(hv))
            elif isinstance(hv, bytes):
                hv = int(self.hashfunc(hv).hexdigest(), 16) % _hash_range
                parsed.append(np.uint64(hv))
            elif hasattr(hv, 'hexdigest'):  # 是hashlib哈希对象
                hv = int(hv.hexdigest(), 16) % _hash_range
                parsed.append(np.uint64(hv))
            else:
                raise ValueError(f"Unsupported hashvalue type: {type(hv)}")
        return np.array(parsed, dtype=np.uint64)


    def add(self, b):
        b = b.encode('utf-8') if isinstance(b, str) else b # 如果是字符串，则编码为字节
        hv = int(self.hashfunc(b).hexdigest(), 16) % _hash_range
        a, b = self.permutations # 取出当前的排列参数
        phv = np.bitwise_and((a * hv + b) % _mersenne_prime, np.uint64(_max_hash)) # 计算哈希值，通过线性变换和模运算来生成，并限制在0到2^32-1之间
        self.hashvalues = np.minimum(phv, self.hashvalues) #保留所有维度上目前为止的最小哈希值 —— 也就是 MinHash 签名向量
    
    def jaccard(self, other):
        # 如果种子不同，抛出异常
        if other.seed != self.seed:
            raise ValueError("different seeds")
        # 如果哈希值不同，抛出异常
        if len(self) != len(other):
            raise ValueError("different numbers of permutation functions")
        return np.float64(np.count_nonzero(self.hashvalues==other.hashvalues)) / np.float64(len(self))

    def __len__(self):
        return len(self.hashvalues)

    def __eq__(self, other):
        return type(self) is type(other) and  self.seed == other.seed and np.array_equal(self.hashvalues, other.hashvalues)
    