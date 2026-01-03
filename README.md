# 🚀 GitHub ETL Pipeline: CSV to JSON

> Automated pipeline that moves CSV data from one GitHub repo to another as JSON using Python with Lambda Funtions. Perfect for learning ETL basics!

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub API](https://img.shields.io/badge/GitHub-API-green.svg)](https://docs.github.com/en/rest)

---

## 🎯 What Does This Do?

Extracts CSV from **Repo A** → Transforms to JSON → Loads into **Repo B**

```
CSV Data (Repo A)  →  Python Script  →  JSON Data (Repo B)
   employees.csv         [ETL Magic]       employees.json
```

**Real-world use**: Data migration, format conversion, automated backups, reporting pipelines.

---

## ⚡ Quick Start (5 Minutes)

### 1. Get a GitHub Token
- Go to [GitHub Settings → Tokens](https://github.com/settings/tokens)
- Click "Generate new token (classic)"
- Check `repo` scope
- Copy the token

### 2. Setup Your Repos

**Repo A (Source)**: Create `data/sample.csv`
```csv
id,name,email,department
1,John Doe,john@example.com,Engineering
2,Jane Smith,jane@example.com,Marketing
```

**Repo B (Destination)**: Create empty `data/` folder

### 3. Configure & Run

Update these lines in `etl_pipeline.py`:
```python
GITHUB_TOKEN = "ghp_your_token_here"
SOURCE_OWNER = "your_username"
SOURCE_REPO = "repo_A"
DEST_REPO = "repo_B"
```

Run it:
```bash
python etl_pipeline.py
```

**Done!** ✅ Check Repo B for your JSON file.

---

## 🔧 How It Works

**3 Simple Steps:**

1. **Extract** 📥 - Fetch CSV from GitHub using API
2. **Transform** 🔄 - Convert CSV rows to JSON format
3. **Load** 📤 - Upload JSON back to GitHub

**Key Features:**
- Uses lambda functions for clean code
- Handles file updates automatically

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| `401 Bad credentials` | Check your token is correct |
| `404 Not Found` | Verify repo and file paths |
| `403 Forbidden` | Token needs `repo` scope |
| `No module 'requests'` | Run `pip install requests` |

---

## 💡 What You'll Learn

- ETL pipeline concepts
- GitHub API usage
- Lambda functions in Python
- CSV/JSON data formats
- REST API authentication

---

⭐ **Found this helpful? Star the repo!**

*Made with ❤️ for beginners learning data engineering*
