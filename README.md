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
├── main.py              \# 主入口文件（新增）\
├── preprocessing/\
│   ├── text_cleaner.py  \# 文本清洗\
│   └── vectorizer.py    \# 特征向量化\
├── fingerprinting/\
│   ├── minhash.py       \# MinHash实现\
│   ├── simhash.py       \# SimHash实现\
│   └── bitsample.py     \# Bit Sampling实现\
├── lsh/\
│   ├── bucketing.py     \# LSH分桶策略\
│   └── candidate_pairs.py\
├── evaluation/\
│   ├── metrics.py       \# 重复率计算\
│   └── visualization.py \# 结果可视化\


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
### **evaluation**

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

<a href="https://github.com/github_username/repo_name/graphs/contributors">
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
* [Jingyang YI](): Designed and implemented the evaluation metrics. [evaluation part](https://github.com/MoliaiELS/Group10_Project/tree/main/evaluation)
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
