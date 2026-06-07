# 🚀 Automated Outreach Pipeline

A production-grade, 4-stage cold outreach automation system that identifies lookalike companies, finds decision-makers, enriches contact data, and automates personalized email delivery.

## 🌟 Key Features

- **Stage 1 (Ocean.io):** Intelligent lookalike company discovery based on a seed domain.
- **Stage 2 (Prospeo Search):** Targeted decision-maker identification (C-Suite, VP, Founders).
- **Stage 3 (Enrichment):** Dual-method contact enrichment (Prospeo native or Apollo.io fallback).
- **Stage 4 (Brevo):** Automated, personalized outreach via SMTP.
- **Production Controls:** Global rate limiting, safety checkpoints (Y/N), and automatic deduplication.

---

## 🛠️ Tech Stack

- **Language:** Python 3.12+
- **APIs:** Ocean.io (v3), Prospeo (Search & Enrich), Apollo.io (Match), Brevo (v3)
- **Libraries:** `requests`, `python-dotenv`

---

## 📂 Project Structure

- `pipeline.py`: **Primary consolidated pipeline.** Uses Prospeo for both search and enrichment (recommended).
- `Pipeline01.py`: **Apollo.io fallback version.** Uses Prospeo for search and Apollo.io for enrichment.
- `requirements.txt`: Project dependencies.
- `.env.example`: Configuration template for API keys.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.12 or higher installed.
- API keys for Ocean.io, Prospeo, Apollo.io (optional), and Brevo.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Lokeessshhh/Automated_Outreach_Pipeline.git
cd Automated_Outreach_Pipeline

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Rename `.env.example` to `.env` and fill in your credentials:
```env
OCEAN_API_KEY=your_key
PROSPEO_API_KEY=your_key
APOLLO_API_KEY=your_key (required for Pipeline01.py)
BREVO_API_KEY=your_key
SENDER_EMAIL=your_verified_brevo_email
SENDER_NAME=Your Name
```

### 4. Running the Pipeline
```bash
python pipeline.py
```

---

## 📺 Demo
![Demo Video](https://drive.google.com/file/d/1e-EdXy2bHatIzOaVyAYmAirrVUDm2zKL/view?usp=sharing)

---

## 🛡️ Safety & Compliance
- **Rate Limiting:** Built-in 3-second delay between API calls to ensure compliance.
- **Verification:** Mandatory safety checkpoint to review contacts before emails are fired.
- **Deduplication:** Prevents multiple emails to the same contact in a single run.

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.
