<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/MoliaiELS/Group10_Project">
    <img src="logo.webp" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">2106 Group 10</h3>

  <p align="center">
    this is a LSH realization from group 10
    <br />
    <a href="https://github.com/MoliaiELS/Group10_Project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/MoliaiELS/Group10_Project">View Demo</a>
    &middot;
    <a href="https://github.com/MoliaiELS/Group10_Project/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/MoliaiELS/Group10_Project/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

### File Structure

GROUP10_PROJECT\
├── README.md            \# 安装与运行说明\
├── requirements.txt     \# 依赖库\
├── preprocessing/\
│   ├── text_cleaner.py  \# 文本清洗\
│   └── vectorizer.py    \# 特征向量化\
├── fingerprinting/\
│   ├── minhash.py       \# MinHash实现\
│   ├── simhash.py       \# SimHash实现\
│   └── bitsample.py     \# Bit Sampling实现\
├── lsh/\
│   ├── example.py     
│   └── lsh.py         \# LSH\
├── evaluation/\
│   ├── metrics.py       \# 重复率计算\
│   └── visualization.py \# 结果可视化


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
### Prerequisites
- **Python 3.7+**: Ensure Python 3.7 or higher is installed.  
  Check the version via terminal:
  ```bash
  python --version  # or python3 --version
  ```

### Installing Dependencies

#### Using `pip` (Recommended)
1. **Create and Activate Virtual Environment** (optional but recommended):
   ```bash
   # Create virtual environment
   python -m venv myenv

   # Activate environment
   # For Windows
   myenv\Scripts\activate
   # For Linux/macOS
   source myenv/bin/activate
   ```

2. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

---

#### Using `conda`
1. **Create and Activate Virtual Environment**:
   ```bash
   # Create environment (optional to specify Python version)
   conda create -n myenv python=3.9

   # Activate environment
   conda activate myenv
   ```

2. **Install Required Libraries**:
   - Directly via `pip` (recommended):
     ```bash
     pip install -r requirements.txt
     ```
   - Or manually via `conda`:
     ```bash
     conda install numpy pandas scikit-learn
     ```

---

### Verifying Installation
Run the following command to check if dependencies are installed successfully:
```bash
python -c "import pandas, sklearn, numpy; print('All libraries loaded successfully!')"
```
If no errors occur, the environment setup is complete.

### Notes:
- **Virtual Environment**: Strongly recommended to use virtual environments (such as `venv` or `conda`) to isolate project dependencies and avoid global package conflicts.
- **Dependency Versions**: The versions in `requirements.txt` are minimum requirements. The actual installation will automatically fetch compatible latest versions.
- **OS Differences**: Note that virtual environment activation commands differ slightly between Windows and Linux/macOS.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
### **preprocessing**
Here are the usage examples for the data preprocessor:
- Before using this code, make sure to add the files that need deduplication to the current directory.

---

```python
from preprocessor import TextPreprocessor:
preprocessor = TextPreprocessor(n_features=2**20, ngram_range=(3, 5))
preprocessor.load_data('test.parquet', 'valid.parquet') #change it to your file path
preprocessor.apply_cleaning()
train_features, valid_features = preprocessor.feature_extraction()
#dataset used for minhash
train_ngrams, valid_ngrams = preprocessor.get_ngrams_for_minhash()
#dataset used for simhash
train_token_freqs, valid_token_freqs = preprocessor.get_simhash_inputs()
train_features, valid_features = preprocessor.preprocess('train.parquet', 'valid.parquet')
```
---
#### **Parameters in TextPreprocessor Class**
- **`n_features=2**20`**: This parameter sets the number of features for the HashingVectorizer. A larger number of features allows for capturing more nuances in the data, but it also increases computational complexity and memory usage.
- **`ngram_range=(3, 5)`**: This parameter specifies the range of n-grams to consider during feature extraction. Here, n-grams of size 3 to 5 characters are used. This means that sequences of 3, 4, and 5 characters are extracted from the text for feature representation. Character-level n-grams are particularly useful for capturing patterns in texts where spelling variations or typos might occur.


### **fingerprinting**
#### quick verification
For quick verification, you can directly run and view files in the UnitTest folder
Here are the English version usage examples for the three hash implementations:

---

#### **1. SimHash Usage Example**
```python
from simhash import Simhash

# Example 1: Generate fingerprints from text
text1 = "Natural language processing is a key field in artificial intelligence"
text2 = "Natural language processing belongs to critical areas of AI"
hash1 = Simhash(text1, f=64)
hash2 = Simhash(text2, f=64)

print(f"Fingerprint of text1 (hex): {hash1.hex}")
print(f"Hamming distance: {hash1.hamming_distance(hash2)}")
print(f"Similarity: {hash1.similarity(hash2):.2f}")

# Example 2: Generate fingerprints from feature list
features = [("apple", 3), ("banana", 2), ("orange", 5)]
hash3 = Simhash(features, f=64)
print(f"Feature list fingerprint: {hash3.hex}")
```

---

#### **2. BitSamplingHash Usage Example**
```python
from bitsampling import BitSamplingHash
from simhash import Simhash

# Generate two Simhash fingerprints
text1 = "The quick brown fox jumps over the lazy dog"
text2 = "The fast brown fox jumps over the lazy dog"
simhash1 = Simhash(text1, f=64)
simhash2 = Simhash(text2, f=64)

# Initialize bit sampler (randomly selects 8 bits from 64)
sampler = BitSamplingHash(num_bits=64, sample_size=8, seed=42)

# Sample fingerprints
bits1 = sampler.hash(simhash1.fingerprint)
bits2 = sampler.hash(simhash2.fingerprint)

print(f"Sampled bit indices: {sampler.selected_bits}")
print(f"Sampled bits 1: {bits1}")
print(f"Sampled bits 2: {bits2}")
print(f"Post-sampling similarity: {sampler.similarity(bits1, bits2):.2f}")
```

---

#### **3. MinHash Usage Example**
```python
from minhash import MinHash

# Initialize two MinHash objects (must use same seed)
minhash1 = MinHash(d=128, seed=42)
minhash2 = MinHash(d=128, seed=42)

# Add elements to MinHash
data1 = ["apple", "banana", "orange", "grape"]
data2 = ["apple", "banana", "pear", "mango"]

for word in data1:
    minhash1.add(word)
for word in data2:
    minhash2.add(word)

# Calculate Jaccard similarity
similarity = minhash1.jaccard(minhash2)
print(f"Set similarity: {similarity:.2f}")

# Error example: Different seeds will raise error
try:
    minhash3 = MinHash(seed=123)
    minhash1.jaccard(minhash3)
except ValueError as e:
    print(f"Error caught: {e}")
```

---

#### **Key Features**
| Algorithm       | Core Purpose                      | Typical Use Cases           |
|-----------------|-----------------------------------|-----------------------------|
| **SimHash**     | Text fingerprinting & similarity | Duplicate detection, Plagiarism check |
| **BitSampling** | Dimensionality reduction for fast approximate matching | Large-scale fingerprint pre-screening |
| **MinHash**     | Set similarity estimation (Jaccard index) | Recommendation systems, Document similarity |

All examples are directly executable and demonstrate core functionalities of each algorithm.
### **lsh**
#### 1. **Initializing the `LSHCache`**
To use the `LSHCache`, you need to initialize it with specific parameters. The initialization process involves setting up various configurations such as the hashing method, the number of bands, rows per band, and shingles.

```python
from lshcache import LSHCache

# Initialize LSHCache with MinHash as the hashing method
lsh_cache = LSHCache(n=100, b=20, r=5, max_shingle=3, hash_method='minhash')
```

##### Explanation of Parameters:
- **`n=100`**: The **signature length** for MinHash, which determines the size of the hash signatures that represent each document. This will be the total length of the MinHash signature.
- **`b=20`**: The **number of bands** for Locality Sensitive Hashing (LSH). This refers to how the signature is divided into smaller groups (bands) during the hashing process. More bands improve the ability to detect duplicates but also increase memory usage.
- **`r=5`**: The **number of rows per band**. Each band consists of `r` rows. In the case of MinHash, this means that the hash signature is divided into `b` bands, with each band containing `r` rows.
- **`max_shingle=3`**: This specifies the **maximum length of shingles** (substrings) used to generate the document signature. A shingle is a contiguous sequence of characters in the document, and this parameter controls the size of those sequences.
- **`hash_method='minhash'`**: The **hashing technique** used to generate the signatures. Options are:
  - **`minhash`**: Uses MinHash to generate a signature for each document.
  - **`simhash`**: Uses SimHash for generating document signatures.
  - **`bitsampling`**: Uses BitSampling hashing to generate document signatures.

---

#### 2. **Inserting Documents into the Cache**
After initializing the `LSHCache`, you can insert documents into the cache by calling the `insert` method. This method calculates the LSH signature for the document and stores it in the cache for future duplicate detection.

```python
# Insert a document into the LSHCache
doc = "Natural language processing is a key field in artificial intelligence."
doc_id = 1
lsh_cache.insert(doc, doc_id)
```

##### Explanation:
- **`doc`**: The document to insert into the cache. It can be any string, representing the content of the document.
- **`doc_id`**: A **unique identifier** for the document. This ID will help in referencing the document when searching for duplicates or performing other operations.
- The method calculates the LSH signature for the document and stores it in the cache.

---

#### 3. **Checking for Duplicate Documents**
Once documents are inserted into the cache, you can check if a new document is similar to any of the stored documents by using the `get_dups` method. This method finds potential duplicates by comparing the LSH signatures.

```python
# Check for duplicates of the document with ID 1
duplicates = lsh_cache.get_dups(doc, doc_id)
print(duplicates)
```

##### Explanation:
- **`doc`**: The document to check for duplicates. This is the new document whose similarity you want to check against the documents in the cache.
- **`doc_id`**: The **unique identifier** for the document you are checking. This ensures that the document itself is not returned as a duplicate.
- The method returns a list of **duplicate document IDs** based on the similarity of their LSH signatures.

---

#### 4. **Batch Insertion of Documents**
The `insert_batch` method allows you to insert multiple documents into the cache at once. It accepts a list of document-ID tuples, and processes all documents in the batch.

```python
# Insert a batch of documents
doc_tuples = [(doc1, 1), (doc2, 2), (doc3, 3)]
batch_duplicates = lsh_cache.insert_batch(doc_tuples)
```

##### Explanation:
- **`doc_tuples`**: A list of **tuples**, where each tuple consists of a document and its unique ID.
- The method inserts all documents from the batch into the cache and returns a dictionary of **duplicate documents** found for each document.

---

#### 5. **Querying for Document Count and Recent Insert Time**
You can retrieve information about the cache, such as the total number of documents stored and the timestamp of the most recent insert.

```python
# Get the number of documents stored in the cache
num_docs = lsh_cache.num_docs()
print(f"Number of documents: {num_docs}")

# Get the timestamp of the most recent insert
recent_insert_time = lsh_cache.most_recent_insert()
print(f"Most recent insert time: {recent_insert_time}")
```

##### Explanation:
- **`num_docs()`**: Returns the total **number of documents** currently stored in the cache. This is useful for tracking the size of the cache.
- **`most_recent_insert()`**: Returns the timestamp of the most recent document insertion. This helps in knowing when the latest document was added.

---

#### Summary of Key Methods and Their Usage:

- **`insert(doc, doc_id)`**: Inserts a document and computes its LSH signature.
- **`get_dups(doc, doc_id)`**: Checks if the document has duplicates in the cache.
- **`insert_batch(doc_tuples)`**: Inserts multiple documents in batch and checks for duplicates.
- **`num_docs()`**: Retrieves the total number of documents stored in the cache.
- **`most_recent_insert()`**: Retrieves the timestamp of the most recent insert.

There is a more detailed example in /lsh/example.py. You can visit this for better understanding.
### **evaluation**
#### environment 
`pip install pandas numpy matplotlib seaborn pyarrow psutil `
#### evaluation2.py：check duplicate within one file
#### evaluation3.py：check duplicate between file

#### parameters and their effects

```
{
    "hash_method": "minhash",
    "params": {
        "n": 80,           # length of fingerprint
        "b": 8,            # band num
        "r": 10,           # The number of rows per band
        "max_shingle": 3   # n-gram
    }
}
{
    "hash_method": "simhash",
    "params": {
        "b": 4,            # band num
        "r": 32,           # The number of rows per band
        "max_shingle": 4,  # n-gram
        "f": 128           # length of fingerprint
    }
}
{
    "hash_method": "bitsampling",
    "params": {
        "b": 4,            #  Number of samplers
        "r": 32,           #  Number of samplers bits 
        "max_shingle": 4,  # n-gram
        "f": 128          #  Feature vector length
    }
}
```
#### MinHash
- n: Signature length. Positively correlated with accuracy and computational cost.
- b: Smaller values make the judgment stricter.
- r: Larger values make the judgment stricter.
- Shingle length: Longer lengths correspond to longer phrase relationships and make it stricter.

**n = b * r**

#### SimHash
- b: Larger values make it stricter.
- r: Larger values make it stricter.
- Shingle length: Larger values make it stricter.

**r has an exponential impact on memory. The time complexity is f. f = b * r**

#### BitSampling
- b: Number of samplers. Larger values lead to higher precision.
- r: Length of the sampler. Larger values make it stricter.
- f: Fingerprint length, feature vector length

**f = b * r** 

#### output example 
##### within one file 
```
orig index: [0]
  dup index: [0]
orig index:[1463]
  dupindex::[1462]
orig index:[3425]
  dupindex:[2432]
  dup index:[2432]
  dup index:[3425]
..............
=== Statistical Information ===
Total number of documents: 81798
Number of duplicate documents: 283
Number of unique documents: 81515
Number of duplicate document pairs: 179
Duplication rate: 0.35%
Current memory usage: 6918.58 MB
```
##### between files 

```
=== Testing MINHASH ===
Number of documents in Database 1: 81137
Number of documents in Database 2: 81799
Number of duplicate records between databases: 992
Duplication rate: 1.21%
Current memory usage: 6489.69 MB
Top 10 duplicate records between databases:
set2_0 -> ['set1_123','set1_456'] 
```










<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/MoliaiELS/Group10_Project/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=github_username/repo_name" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact
For any questions or feedback, feel free to reach out:
- **GitHub Repository**: [Group10_Project](https://github.com/MoliaiELS/Group10_Project)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Keyu HU](https://github.com/XXX616519): Implemented the Loc-Salityensitive Hashing (LSH) algorithm. [LSH part](https://github.com/MoliaiELS/Group10_Project/tree/main/lsh) 
* [Ocean Kun Hei OU](https://github.com/oukunhei): Responsible for data preprocessing and cleaning. [preprocessing part](https://github.com/MoliaiELS/Group10_Project/tree/main/preprocessing)
* [Jingyang YI](https://github.com/jyi664): Designed and implemented the evaluation metrics. [evaluation part](https://github.com/MoliaiELS/Group10_Project/tree/main/evaluation)
* [Ye GUO](https://github.com/MoliaiELS): Developed the fingerprinting module. [fingerprinting part](https://github.com/MoliaiELS/Group10_Project/tree/main/fingerprinting)

We appreciate everyone's contributions! 🙌
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/MoliaiELS/Group10_Project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/MoliaiELS/Group10_Project/forks
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/MoliaiELS/Group10_Project/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/MoliaiELS/Group10_Project/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/MoliaiELS/Group10_Project/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
