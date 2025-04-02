import numpy as np
import my_hash as mh

# 一些常量
_mersenne_prime = (1 << 61) - 1 # 梅森素数，用于生成伪随机数
_max_hash = (1 << 32) - 1 # 最大哈希值
_hash_range = (1 << 32) # 哈希值范围
 
# class MinHash
#  MinHash类实现了MinHash算法，用于计算集合的Jaccard相似度
class MinHash(object):
    # @param d: 需要的哈希函数数量
    # @param seed: 随机种子
    # @param hashfunc: 哈希函数，默认为sha1_hash32
    # @param hashvalues: 如果提供了这些值，它们将用来初始化哈希签名
    # @param permutations: 如果传入了排列，使用这些排列来生成哈希值
    def __init__(self, d=128, seed=1, hashfunc=mh.sha1_hash32, hashvalues=None, permutations=None):
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
    
    # 初始化哈希值
    # @param d: 哈希值的数量
    def _init_hashvalues(self, d):
        return np.ones(d, dtype=np.uint64)*_max_hash # 初始化为最大哈希值
    
    # 解析哈希值
    # @param hashvalues: 哈希值
    # @return: 解析后的哈希值
    def _parse_hashvalues(self, hashvalues):
        return np.array(hashvalues, dtype=np.uint64) # 解析为无符号64位整数，限制在0到2^64-1之间
    
    # 添加哈希值
    # @param b: 需要添加的哈希值
    def add(self, b):
        hv = self.hashfunc(b) # 计算哈希值
        a, b = self.permutations # 取出当前的排列参数
        phv = np.bitwise_and((a * hv + b) % _mersenne_prime, np.uint64(_max_hash)) # 计算哈希值，通过线性变换和模运算来生成，并限制在0到2^32-1之间
        self.hashvalues = np.minimum(phv, self.hashvalues) #保留所有维度上目前为止的最小哈希值 —— 也就是 MinHash 签名向量
    
    # 计算Jaccard相似度
    # @param other: 另一个MinHash对象
    # @return: Jaccard相似度
    def jaccard(self, other):
        # 如果种子不同，抛出异常
        if other.seed != self.seed:
            raise ValueError("different seeds")
        # 如果哈希值不同，抛出异常
        if len(self) != len(other):
            raise ValueError("different numbers of permutation functions")
        return np.float64(np.count_nonzero(self.hashvalues==other.hashvalues)) / np.float64(len(self))
    
    # 重载len函数，返回哈希值
    def __len__(self):
        return len(self.hashvalues)
    
    # 重载 ==，判断两个MinHash对象是否相等
    def __eq__(self, other):
        return type(self) is type(other) and  self.seed == other.seed and np.array_equal(self.hashvalues, other.hashvalues)
    