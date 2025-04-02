import struct

# """左循环位移，模拟SHA-1中的左循环位移操作"""
def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF  # 使用32位掩码

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
            
            temp = (left_rotate(a, 5) + f + e + k + w[t]) & 0xFFFFFFFF
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
