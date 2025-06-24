# 🌐 TILT-Telugu

**TILT-Telugu** (Instruction Tuning for Telugu using Mixed-Quality Web Data) is a research and engineering project focused on building and evaluating instruction-tuned large language models (LLMs) for the Telugu language using data sourced from diverse web sources of varying quality.

> 🔬 This project aims to improve the instruction-following ability of LLMs in low-resource, morphologically rich languages like Telugu by collecting realistic data and fine-tuning open models.

---

## 📌 Project Goals

- ✅ Collect Telugu text data from diverse sources (news, forums, metadata, etc.)
- ✅ Detect and tag script type: `Telugu`, `Romanised`, `Code-mixed`
- ✅ Create high-quality instruction–response pairs in Telugu
- ✅ Fine-tune open LLMs using LoRA/QLoRA
- ✅ Evaluate performance using automatic and human metrics
- ✅ Publish and open-source the resulting models, datasets, and evaluation code

---

## 🗂️ Repository Structure

```

tilt-telugu/
│
├── data\_collection/        # Scripts to scrape, clean, and classify Telugu data
├── dataset/                # Processed instruction-tuning dataset (WIP)
├── notebooks/              # Jupyter notebooks for EDA, training logs, etc.
├── models/                 # Trained model artifacts or configs (excluded from Git)
├── evaluation/             # Evaluation scripts for model output
├── utils/                  # Helper scripts and common functions
│
├── requirements.txt        # Python dependencies
├── bbc\_telugu\_urls.txt     # Example input URL file for scraping
├── LICENSE
└── README.md

````

---

## 🧠 Script Types in Use

- 📝 **Telugu**: Native Telugu script (Unicode)
- 🔤 **Romanised**: Telugu written in Latin characters
- 🌐 **Code-mixed**: Sentences mixing both scripts

Script detection is powered by Unicode-aware regex (`regex` module with `\p{Telugu}`).

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/dipika-desaboyina/tilt-telugu.git
cd tilt-telugu
````

### 2. Set up your virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run a scraping script

```bash
python data_collection/weburl_scraper.py
```

Output will be saved as CSV files in the current directory.

---

## 🛠 Tools & Libraries Used

* `requests`, `BeautifulSoup` – Web scraping
* `regex` – Script detection (Unicode-aware)
* `pandas` – Data processing and CSV export
* `transformers`, `datasets`, `peft`, `trl` – Model tuning (coming soon)
* `Hugging Face Hub` – Model & dataset sharing (planned)

---

## 📊 Roadmap

* [x] Collect & tag data from BBC Telugu
* [x] Detect and classify script types
* [ ] Aggregate and deduplicate dataset
* [ ] Generate instruction–response pairs
* [ ] Fine-tune LLMs (Mistral, LLaMA, Falcon)
* [ ] Evaluate & publish results
* [ ] Upload to Hugging Face Hub with model cards

---

## 🤝 Contributing

Contributions are welcome, especially from native Telugu speakers, linguists, and NLP researchers interested in low-resource languages.

To contribute:

* Open an issue
* Fork and submit a pull request
* Suggest improvements via Discussions

---

## 📄 License

This project is licensed under the MIT License.
See the [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgments

* Hugging Face ecosystem
* Open-source Telugu corpora and online content
* Community researchers working on LLMs for Indian languages

---

## ⭐ Support the Project

If this project inspires or helps you, consider starring the repository or contributing back! Together, we can improve AI for low-resource languages like Telugu.
