# 使用代码评估数据集
# 分析代码结果
* The parameters used in this algorithm are the optimal ones obtained through multiple repeated runs and result checks.
## Minhash： 

### 定量分析
* 复杂度
    * 签名生成: O(n*d)
    * lsh: O(b)
####
* evaluation-minhash-self：  


| 测试序号 | 文档名称 | 参数 (n ; b ; r ; max_single ) | 总数 | 重复数 | 唯一数 | 重复对数 | 重复率 |
|---------|----------|----------------------|------|--------|--------|----------|---------|
| min1-1  | test1    | 200 ; 20 ; 10 ; 3         | 81137| 598    | 80539  | 992      | 0.74%   |
| min1-2  | test1    | 80  ; 8  ; 10 ; 3         | 81137| 334    | 80803  | 512      | 0.41%   |
| min1-3  | test2    | 200 ; 20 ; 10 ; 3         | 80593| 544    | 80840  | 763      | 0.67%   |
| min1-4  | validation1    | 200 ; 20 ; 10 ; 3         | 81799| 525    | 81274  | 813      | 0.64%   |
| min1-5  | validation2    | 200 ; 20 ; 10 ; 3         | 81798| 491    | 81307  | 828      | 0.60%   |

* 平均算法部分内存占用 6489.69 MB
* 平均运行时间 10 min (without min 1-2)
####
* evaluation between documents


### 定性分析
* 优势：
    * minhash 指纹生成可以有效保留文章的整体性
        * example 1-1：Q48707369 & Q449303 in min1-1
    * minhash 的运行速度较快（结果来自实践）
* 不足：
    * 容易把固定格式或者有高度相似格式的信息判定为相似
        * example 2-1：Q17599320 & Q17593285 in min1-1 
       
        Both texts are reports on the match results of the Cypriot league. They differ in terms of time and the league level, and contain information with distinct meanings. However, due to their highly similar structures and themes, they have been determined by the algorithm to be similar texts.  
        Moreover, it is difficult to eliminate this kind of error by adjusting the parameters to make the judgment more stringent. This is an inevitable defect of the minhash algorithm, which mainly tends to conduct an overall evaluation. 

        * example 2-2:  Q4889887 & Q5130011 & Q5595596 & Q10748601 & Q7970555 in min1-1
        * same problems as example 2-1

### minhash 总结
* Because the logic of minhash fingerprint generation is to reflect the overall information, this will lead to the situation where data with some sentence patterns and grammar being similar but actually having significant differences in meaning are considered to have a high similarity and are placed in positions that are difficult to remove by changing parameters. What's more, in order to remove this part of errors, it is often necessary to sacrifice many correct results. Therefore, when minhash obtains a relatively ideal duplicate checking result, the duplication rate is relatively high.



## Simhash
### 定量分析
* 复杂度
    * 指纹生成: O( f*d )
    * lsh: O( b*r )
#### 
* evaluation-simhash-self 

| 测试序号 | 文档名称 | 参数 ( b ; r ; max_single ; f ) | 总数 | 重复数 | 唯一数 | 重复对数 | 重复率 | 内存占用 |  
|---------|----------|----------------------|------|--------|--------|----------|---------|----------|  
| Sim 1-1 | test1 | 4;32;4;128 | 81137 | 56 | 81081| 56 | 0.07% | 9755.91MB | 
| Sim 1-2 | test1 | 4;16;4;64 | 81137 | -- | -----| -- | 99.76% | ----------|   
| Sim 1-3 | test2 | 4;32;4;128 | 81137 | 57 | 81080 | 37 | 0.07% | 10671.70MB | 
| Sim 1-4 | validation1 | 4;32;4;128 | 81799 | 46 | 81753| 27 | 0.06% | 10458.50 MB|  
| Sim 1-5 | validation2 | 4;32;4;128 | 81798 | 52 | 81746 | 53 | 0.06% | 10644.37 |   

* average runtime: about 25 min
* 平均内存占用: about 10GB
### 定性分析  
* 优势 
    * simhash方法可以同时保持接近真实值的正确率和重复率(经过人工抽样检查得到的结论)
    * 结果较为稳定，根据大数定理，当随机选取的文本数量达到一个较大值时，每个文本集合应该有相似的重复率。记录的数据正好满足这一点。

* 不足
    * simhash方法对于参数及其敏感。很难找到合适的参数。很难对已有的参数进行微调。(sim 1-2)
    * 内存开销大，运算时间长 (平均时间消耗 20 min ，内存消耗 10 GB)
    * 对于局部异常有强烈反馈，容易忽略文本整体结构。以下两个例子虽然语义相同但是simhash方法会认为他们是不同的。 (example below)
        * Artificial intelligence is revolutionizing various industries, such as healthcare, finance, and transportation. It offers new solutions to complex problems and improves efficiency
        * Artificial intelligence offers new solutions to complex problems and improves efficiency. It is revolutionizing various industries, like healthcare, finance, and transportation. And it's really amazing

### simhash 
* The SimHash method can closely approximate the true values in terms of both accuracy and duplication rate. However, as the data dimension increases, the fingerprint generation step and Hamming distance calculation step of the SimHash method will incur significant time and memory costs. Moreover, SimHash is sensitive to local differences and may make judgments of dissimilarity due to reasons such as reversed word order, which do not change the words used or their meanings. 

## bitsampling
### 定量分析
* 复杂度

| 测试序号 | 文档名称 | 参数 ( b ; r ; max_single ; f ) | 总数 | 重复数 | 唯一数 | 重复对数 | 重复率 | 内存占用 |  
|---------|----------|----------------------|------|--------|--------|----------|---------|----------| 
| bit 1-1 | test1 | 4;28;3;112 | 81137 | 297 | 80840 | 189 | 0.37% | 6835.22MB | 
| bit 1-1。2 | test1 | 4;28;3;112 | 81137 | 264 | 80840 | 176 | 0.33% | 6856.26MB |
| bit 1-2 | test2 | 4;28;3;112 | 81137 | 334 | 80803 | 176 | 0.41% | 6668.39MB | 
| bit 1-3 | validation1 | 4;28;3;112 | 81799 | 304 | 81495 | 163 | 0.36% | 6882.35MB | 
| bit 1-4 | validation2 | 4;28;3;112 | 81798 | 283 | 81515 | 179 | 0.35% | 6918.58MB | 

* 平均内存占用 about 6.8 GB
* 平均运行时间 about 8 min
### 定性分析
* 优势 
    * 代码实现简单易于理解  
    * 计算复杂度低，速度相对较快，适合进行大规模计算 
* 不足
    * 采取抽样的方式，会损失部分细节
    * 抽样具有随机性，运行结果难复现，结果具有偶然性
### bitsampling 总结
Bit Sampling is a fingerprint generation method used for text deduplication. It first converts text into binary vectors and then selects some bits from them according to specific rules to obtain sampled vectors, which are used as text fingerprints to determine text similarity. This method is simple to implement and has a low computational complexity, enabling efficient operation even in resource - constrained environments. However, it has issues such as easy information loss and unstable results. It may miss pairs of similar texts, and the results can vary under different samplings. 


