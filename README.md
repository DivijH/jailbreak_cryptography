# When “Competency” in Reasoning Opens the Door to Vulnerability: Jailbreaking LLMs via Novel Complex Ciphers

Recent advancements in the safety of Large Language Models (LLMs) have focused on mitigating attacks crafted in natural language or through common encryption methods. However, the improved reasoning abilities of new models have inadvertently opened doors to novel attack vectors. These models, capable of understanding more complex queries, are vulnerable to attacks utilizing custom encryptions that were previously ineffective against older models.

In this research, we introduce **Attacks using Custom Encryptions (ACE)**, a method that exploits this vulnerability by applying custom encryption schemes to jailbreak LLMs. Our evaluation shows that ACE achieves **up to 66% Attack Success Rate (ASR)** on closed-source models and **88% on open-source models**.

Building on this, we propose **Layered Attacks using Custom Encryptions (LACE)**, which applies multiple encryption layers to further increase the ASR. LACE increases the ASR of GPT-4o from **40% to 78%**, a 38% improvement. Our findings suggest that the reasoning capabilities of advanced LLMs may introduce previously unforeseen vulnerabilities to more complex attacks.

## Repository Overview

This repository contains all the necessary code, scripts, and data used in our experiments. Below is an overview of the directory structure and the key components.

### Directory Structure

```
├── README.md                             # This file
├── requirements.txt                      # Python dependencies
├── src/
│   ├── data_gen/
│   │   └── main.py                       # Script to generate encrypted data for jailbreaking LLMs
│   ├── cipherbench/
│   │   └── generate_encryptions.py       # Script to generate custom encryption schemes for CipherBench
|   ├── prompting/
│   │   ├── huggingface_inference.py      # Script for using huggingface models
│   │   └── prompting.py                  # Script for using Proprietary models (Gemini, GPT-4o)
|   ├── evaluation
├── keys/
│   ├── gemini.key                        # Gemini API key for querying closed-source models
│   ├── openai.key                        # OpenAI API key for querying models like GPT-4o
│   └── huggingface.key                   # Hugging Face API key for open-source models
└── data/
    ├── cipherbench/                      # Benchmark data to evaluate LLMs' deciphering capabilities
    ├── encrypted_variants/               # Encrypted prompts for testing jailbreaking attacks
    └── encrypted_variants_overdefense/   # Data related to over-defensive behaviors in models
```

### Key Components

- **ACE (Attacks using Custom Encryptions):** The novel method that uses custom encryption schemes to jailbreak advanced LLMs.
- **LACE (Layered Attacks using Custom Encryptions):** An extension of ACE that applies multiple layers of encryption to further enhance the success rate.
- **CipherBench:** A benchmark used to assess the deciphering capabilities of LLMs when faced with novel and complex ciphers.

### Scripts

- **`src/data_gen/`:** This directory contains all the encryptions used for jailbreaking attacks. You can modify or customize the encryption schemes here.
  
- **`src/cipherbench/generate_encryptions.py`:** This script generates CipherBench, a set of custom encryption schemes used to test the decryption capabilities of the target LLMs.

## Installation

To set up the environment and install the required dependencies, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/DivijH/jailbreak_cryptography.git
   cd jailbreak_cryptography
   ```

2. **Install dependencies:**

   Make sure you have Python 3.11+ installed. Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Add API keys:**

   Make sure to add your API keys for the LLM models you are testing:

   - `keys/gemini.key` for Gemini models.
   - `keys/openai.key` for OpenAI models (e.g., GPT-4).
   - `keys/huggingface.key` for Hugging Face models.


<!--
## Citation

If you find this work useful, please consider citing our paper:

```
@article{llm_jailbreaking_vulnerabilities,
  title={When "Competency" in Reasoning Opens the Door to Vulnerability: Jailbreaking LLMs via Novel Complex Ciphers},
  author={Your Name, Co-author Name},
  journal={ArXiv},
  year={2024},
}
```

---

For any questions or support, please open an issue or contact us at [email@example.com].
-->
