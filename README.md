# **vcrypto - Secure Secrets Management in Python**
vcrypto is a simple and effective utility for securely storing passwords and secrets in Python. It leverages **Fernet encryption** from the [cryptography](https://cryptography.io/en/latest/) module instead of reinventing the wheel.

## **🔒 Why vcrypto?**
Managing secrets in Python, especially in collaborative projects, can be cumbersome. Our approach simplifies it:

👉 **One master private password** (ignored in Git)\
👉 **A structured dictionary file with encrypted secrets**\
👉 **Easily shareable** - only the master password needs to be exchanged once\
👉 **Version-controlled secrets** - since only encrypted values are stored

This package makes it easy to **store and retrieve encrypted secrets** in **JSON** or **YAML** formats.

---

## **📌 Features**
- 🔐 **AES-128 Encryption** (Fernet) for secure storage.
- 📂 **JSON/YAML Support** for structured secret storage.
- 🛠️ **Environment Variable Support** for flexible key management.
- 🔑 **Simple API** for saving and retrieving secrets.

---

## **📝 Installation**
Install via **pip**:
```sh
pip install vcrypto
```

---

## **🚀 Quickstart**
### **1️⃣ Initialize vcrypto**
Before using `vcrypto`, initialize it with:
```python
from vcrypto import init_vcrypto

init_vcrypto(secrets_file="secrets.yaml", environ_var_name="MY_ENV_VAR")
```

> [!TIP]
> You only need to initialize it **once**.

This ensures `vcrypto` knows where to store secrets and how to retrieve the master password.

### **2️⃣ Store and Retrieve Secrets**
#### **Save a Secret**
```python
from vcrypto import save_secret

save_secret("SECRET_TOKEN", "super_secret_value")
```

#### **Retrieve a Secret**
```python
from vcrypto import read_secret

token = read_secret("SECRET_TOKEN")
print(token)  # Output: super_secret_value
```

---

## **⚙️ Customization**
The `init_vcrypto` function allows customization:

| Parameter                 | Description |
|---------------------------|-------------|
| `secrets_file`            | Path to the encrypted secrets file (JSON/YAML) |
| `filename_master_password`| Path to the master password file (optional, defaults to `master.password`) |
| `environ_var_name`        | Name of an environment variable to retrieve the master password |

**Example:**
```python
init_vcrypto(secrets_file="config/secrets.yaml", filename_master_password="config/master.secret")
```
This setup stores **both** the `master.password` and `secrets.yaml` in the `config/` folder.

---

## **🛠️ Development**
This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management.

### **Install dependencies**
```sh
pip install uv
uv venv
uv install
```

---

## **💜 License**
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## **👤 Author**
- **[Arnau Villoro](https://villoro.com)**

---
