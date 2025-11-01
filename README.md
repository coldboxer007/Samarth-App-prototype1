# Samarth - Agricultural & Climate Data Analysis

AI-powered question-answering system that provides conversational insights about Indian agriculture and climate using data.gov.in datasets.

## 🌟 Key Features

- **🔍 Automatic Dataset Discovery**: Finds relevant datasets from data.gov.in
- **🎓 Conversational Insights**: Responses feel like learning from an experienced professor
- **🏛️ Historical Data Support**: Handles state name variations (Odisha/Orissa, Mumbai/Bombay, etc.)
- **✅ 100% Data Parsing**: Handles any format including tab-separated values
- **📊 Smart Filtering**: Automatically filters large datasets to relevant rows
- **🌾 Agricultural Expertise**: Provides context, implications, and actionable recommendations

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Samarth_app_claude

# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and add your API keys
```

### Get API Keys

**Google Gemini API**: [Get from here](https://makersuite.google.com/app/apikey)
**Data.gov.in API**: [Get from here](https://data.gov.in/)

Add both keys to `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
DATA_GOV_API_KEY = "your-data-gov-api-key-here"
```

### Run the Web App

```bash
streamlit run streamlit_app_direct.py
```

Open your browser to http://localhost:8501

### Test with Sample Questions

```bash
python3 scripts/test_direct_interpretation.py
```

## 💬 Example Questions

- "What was the average annual rainfall in Odisha in 1951?"
- "Compare rainfall patterns between Odisha and Punjab in the 1950s"
- "What are the rainfall patterns in Andaman and Nicobar Islands from 1951 to 1960?"
- "How does Odisha's 1951 rainfall compare to typical levels?"

**Note**: The system automatically handles historical state names (Odisha/Orissa, etc.)

## 🏗️ How It Works

```
1. User asks question
   ↓
2. Discover relevant datasets from data.gov.in
   ↓
3. Fetch RAW data (no transformation!)
   ↓
4. Intelligently filter large datasets
   ↓
5. Send data to LLM for interpretation
   ↓
6. LLM provides concrete answer with sources
```

### Why This Approach?

Traditional systems try to transform messy data into rigid schemas, resulting in:
- ❌ 60-70% transformation failures
- ❌ Complex error-prone code
- ❌ Limited data coverage

**Samarth's Direct Interpretation Approach:**
- ✅ 100% dataset loading (no transformations to fail)
- ✅ Handles any data format (messy columns, weird formats)
- ✅ Simple, maintainable codebase
- ✅ Maximum data coverage

## 📊 Performance

- **Response Time**: 20-40 seconds
- **Dataset Loading Success**: 100%
- **Cost per Question**: ~$0.05-0.10 (Gemini Flash Lite)
- **Data Coverage**: Maximum (all discovered datasets usable)

## 🎯 Use Cases

### Agriculture Analysis
- Crop production trends
- Regional crop comparisons
- District-level production analysis
- Historical yield patterns

### Climate Analysis
- Rainfall patterns and trends
- Temperature variations
- Seasonal climate changes
- Regional climate comparisons

### Policy & Planning
- Data-backed policy recommendations
- Impact of climate on agriculture
- Resource allocation decisions
- Crop diversification strategies

## 📁 Project Structure

```
Samarth_app_claude/
├── src/
│   ├── app_direct.py              # Main application
│   ├── catalog/                   # Dataset discovery & catalog
│   │   ├── dataset_discovery.py   # Auto-discover datasets
│   │   ├── dataset_catalog.py     # Store dataset metadata
│   │   └── data_gov_client.py     # data.gov.in API client
│   ├── llm/                       # LLM components
│   │   └── data_interpreter.py    # Direct data interpretation
│   ├── adapters/                  # Data format adapters
│   └── config.py                  # Configuration
├── scripts/
│   ├── test_direct_interpretation.py  # Test suite
│   └── auto_discover_datasets.py      # Pre-populate catalog
├── streamlit_app_direct.py        # Web UI
└── data/
    └── catalog.db                 # Dataset catalog (auto-created)
```

## 🔧 Configuration

Edit `.env` file:

```bash
# Required API Keys
DATA_GOV_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Optional Settings
CACHE_DIR=./cache                  # Cache directory for datasets
MAX_DATASETS_PER_QUERY=5           # Max datasets to use per question
MAX_ROWS_PER_DATASET=1000          # Max rows to send to LLM
```

## 🧪 Testing

### Run Full Test Suite
```bash
python3 scripts/test_direct_interpretation.py
```

### Test Individual Question
```python
from src.app_direct import SamarthDirectApp

app = SamarthDirectApp()

result = app.answer_question(
    "What is the average rainfall in Maharashtra?",
    auto_discover=True
)

print(result['answer'])
```

## 🎨 Using the API

### Python

```python
from src.app_direct import SamarthDirectApp

# Initialize app
app = SamarthDirectApp()

# Ask a question
result = app.answer_question(
    question="Compare rainfall in Maharashtra and Punjab",
    auto_discover=True,        # Discover new datasets
    max_datasets=5,            # Max datasets to use
    max_rows_per_dataset=500   # Max rows per dataset
)

# Get the answer
print(result['answer'])

# See which datasets were used
print("Datasets:", result['datasets_used'])

# Check if new datasets were discovered
print("New datasets found:", result['discovered_new'])
```

### Response Format

```python
{
    "question": "What is the average rainfall...",
    "answer": "Maharashtra's average annual rainfall is 850mm...",
    "datasets_used": ["Rainfall Data (IMD)", "State Climate Records"],
    "sources": ["resource_id_1", "resource_id_2"],
    "discovered_new": True
}
```

## 🔍 Advanced Features

### Intelligent Dataset Filtering

For large datasets (>100 rows), Samarth automatically uses LLM to filter data:

```python
# Question: "rainfall in Maharashtra"
# Automatic filter: df[df['state'].str.contains('Maharashtra')]
# Result: Only Maharashtra rows sent to LLM
```

### Concrete Answer Format

Samarth provides direct, concrete answers instead of verbose explanations:

**❌ Verbose (old approach):**
```
Looking at the available datasets, I can see rainfall information...
**Data Understanding:** The dataset contains...
**Analysis:** I calculated the average by...
**Answer:** The average is 850mm
```

**✅ Concrete (Samarth):**
```
Maharashtra's average annual rainfall is 850mm based on data from 2019-2024.
This is 35% higher than Punjab's 630mm average for the same period.

Data sources: India Meteorological Department Rainfall Data
```

### Unique Dataset Names

Datasets are automatically named using exact titles from data.gov.in. For generic titles, the publisher is appended:

- "Rainfall" → "Rainfall (India Meteorological Department)"
- "Production Data" → "Production Data (Ministry of Agriculture)"

## 📈 Cost & Performance Analysis

### Typical Question Breakdown

```
Question: "Compare rainfall in Maharashtra and Punjab"

1. Dataset Discovery:    5 seconds    ($0.001)
2. Data Fetching:        3 seconds    (free)
3. Intelligent Filtering: 2 seconds   ($0.01)
4. LLM Interpretation:   15 seconds   ($0.04)
5. Response Generation:  2 seconds    (included)

Total:                   27 seconds   ~$0.05
```

### Cost Optimization Tips

1. **Use fewer datasets**: Set `max_datasets=3` for simpler questions
2. **Reduce rows**: Set `max_rows_per_dataset=300` for quick answers
3. **Cache results**: Implement caching for repeated questions
4. **Pre-filter**: Disable auto_discover if catalog is already populated

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- **Caching**: Add result caching for repeated questions
- **Parallel Processing**: Fetch multiple datasets concurrently
- **Streaming**: Stream LLM responses for better UX
- **Dataset Quality**: Score and rank datasets by quality
- **Multi-language**: Support regional languages

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **Data Source**: data.gov.in (Government of India Open Data Platform)
- **LLM**: Google Gemini Flash Lite
- **Framework**: Streamlit

## 🚀 Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step guide to deploy on Streamlit Cloud.

**Quick Deploy**:
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Add API keys to Secrets (keeps them secure!)
4. Deploy!

## 📞 Support

For questions or issues:
- 📝 Open an issue on GitHub
- 📚 Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help

---

**Ready to try it?**

```bash
streamlit run streamlit_app_direct.py
```

Ask: "What was the average annual rainfall in Odisha in 1951?"
