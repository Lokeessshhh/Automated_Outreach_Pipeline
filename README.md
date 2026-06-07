# 🚀 Automated Outreach Pipeline

A fully automated, 4-stage cold outreach system — one domain in, personalized emails out. Zero manual steps.

---

## 🌟 How It Works

| Stage | Tool | What it does |
|-------|------|-------------|
| 1 | Ocean.io | Finds 5 lookalike companies from seed domain |
| 2 | Prospeo Search | Finds C-Suite/VP/Founder decision-makers |
| 3 | Prospeo Enrich / Apollo.io | Gets verified work emails |
| 4 | Brevo | Sends personalized cold emails |

---

## 🛠️ Tech Stack

- **Language:** Python 3.12+
- **APIs:** Ocean.io (v3), Prospeo (Search & Enrich), Apollo.io (fallback), Brevo (v3)
- **Libraries:** `requests`, `python-dotenv`

---

## 📂 Project Structure

| File | Description |
|------|-------------|
| `pipeline.py` | Main pipeline using Prospeo for enrichment (recommended) |
| `Pipeline01.py` | Apollo.io version for email enrichment |
| `requirements.txt` | Dependencies |
| `.env.example` | API keys template |

---

## 🚀 Getting Started

### 1. Clone & Install
```bash
git clone https://github.com/Lokeessshhh/Automated_Outreach_Pipeline.git
cd Automated_Outreach_Pipeline
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure `.env`
```env
OCEAN_API_KEY=your_key
PROSPEO_API_KEY=your_key
APOLLO_API_KEY=your_key
BREVO_API_KEY=your_key
SENDER_EMAIL=your_verified_brevo_email
SENDER_NAME=Your Name
```

### 3. Run
```bash
python pipeline.py
```

Enter a seed domain (e.g. `stripe.com`) and the pipeline runs automatically.

---

## 📺 Demo

[Watch the Demo Video on Google Drive](https://drive.google.com/file/d/1e-EdXy2bHatIzOaVyAYmAirrVUDm2zKL/view?usp=sharing)

---

## 🛡️ Safety Features

- ⏱️ 3-second rate limiting between API calls
- ✋ Safety checkpoint — review all contacts before emails fire
- 🔁 Deduplication — no duplicate emails in one run

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
