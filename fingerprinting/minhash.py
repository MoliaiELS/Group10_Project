import struct
import numpy as np
 
#"""左循环位移，模拟SHA-1中的左循环位移操作"""
def left_rotate(n, b):
    return ((n << b) & 0xFFFFFFFFFFFFFFFF) | (n >> (64 - b))

# 默认的哈希函数
# 32位的SHA1哈希函数 
def sha1_hash32(data):
    # 将输入数据转换为字节列表
    data = bytearray(data, 'utf-8')

    # 数据长度（以位为单位）
    original_bit_length = len(data) * 8

    # 填充数据（按照SHA-1的标准填充方式）
    data.append(0x80)  # 追加一个1位后跟着七个0（0x80即10000000）
    while len(data) % 64 != 56:
        data.append(0)  # 填充0直到长度满足64的倍数
    
    # 添加原始数据的长度（以64位的形式表示）
    data.extend(struct.pack('>Q', original_bit_length))  # 使用大端法填充原始长度
    
    # 初始化SHA-1状态变量（5个32位的整数）
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    
    # 处理每一个512位块
    for i in range(0, len(data), 64):
        # 获取当前块
        chunk = data[i:i+64]

        # 将512位块分为16个32位的字（每个32位对应一个整数）
        w = [0] * 80
        for t in range(16):
            w[t] = struct.unpack('>I', chunk[t*4:t*4+4])[0]

        # 扩展为80个32位字
        for t in range(16, 80):
            w[t] = left_rotate(w[t-3] ^ w[t-8] ^ w[t-14] ^ w[t-16], 1)
        
        # 初始化暂存变量
        a, b, c, d, e = h0, h1, h2, h3, h4
        
        # SHA-1 主循环
        for t in range(80):
            if 0 <= t <= 19:
                f = (b & c) | (~b & d)
                k = 0x5A827999
            elif 20 <= t <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= t <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            
            temp = left_rotate(a, 5) + f + e + k + w[t] & 0xFFFFFFFF
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp

        # 更新哈希值
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # 将结果组合成最终哈希值
    final_hash = struct.pack('>5I', h0, h1, h2, h3, h4)
    
    # 提取前4个字节（32位）
    return struct.unpack('<I', final_hash[:4])[0]

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
    def __init__(self, d=128, seed=1, hashfunc=sha1_hash32, hashvalues=None, permutations=None):
        # Check the hash function.
        if not callable(hashfunc):
            raise ValueError("The hashfunc must be a callable.")
        self.hashfunc = hashfunc

        self.seed = seed
    
        # Initialize hash values
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
        return np.ones(d, dtype=np.uint64)*_max_hash
 
    def _parse_hashvalues(self, hashvalues):
        return np.array(hashvalues, dtype=np.uint64)
 
    def add(self, b):
        hv = self.hashfunc(b)
        a, b = self.permutations
        phv = np.bitwise_and((a * hv + b) % _mersenne_prime, np.uint64(_max_hash))
        self.hashvalues = np.minimum(phv, self.hashvalues) #保留所有维度上目前为止的最小哈希值 —— 也就是 MinHash 签名向量
 
    def jaccard(self, other):

        if other.seed != self.seed:
            raise ValueError("different seeds")
        if len(self) != len(other):
            raise ValueError("different numbers of permutation functions")
        return np.float(np.count_nonzero(self.hashvalues==other.hashvalues)) / np.float(len(self))
    # 计算MinHash值
    def __len__(self):
        return len(self.hashvalues)
    
    def __eq__(self, other):
        return type(self) is type(other) and  self.seed == other.seed and np.array_equal(self.hashvalues, other.hashvalues)