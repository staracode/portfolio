# Data Science & AI Portfolio

A comprehensive portfolio showcasing various data science, machine learning, and AI projects using Python and R.

## 🏗️ Project Structure

```
portfolio/
├── llm/                 # Medical AI Assistant with SNOMED CT integration
├── ML/                  # Machine learning implementations
├── stats/               # Statistical modeling and GLM examples
├── algos/               # Algorithm implementations and optimizations
├── genomics/            # Single-cell RNA sequencing analysis
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- R 4.0+ (optional, for statistical analysis)
- Streamlit
- PyTorch
- Required Python packages (see installation section)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd portfolio
```

2. Install Python dependencies:
```bash
pip install streamlit torch torchvision requests
```

3. Install R packages (optional, for statistical analysis):
```r
install.packages(c("ggplot2", "rmarkdown", "knitr"))
```

## 📁 Project Components

### 🤖 Medical AI Assistant (`llm/`)

A Streamlit-based medical AI assistant that uses SNOMED CT (Systematized Nomenclature of Medicine) for accurate medical concept identification and filtering.

**Features:**
- Medical question answering with evidence-based responses
- SNOMED CT integration for medical concept validation
- Professional medical disclaimers and safety warnings
- Interactive web interface

**To run:**
```bash
cd llm
streamlit run llm.py
```

**Setup:**
- Requires SNOMED CT API key (sign up at [IHTSDO](https://www.ihtsdo.org/))
- Store API key in `.streamlit/secrets.toml`:
```toml
SNOMED_API_KEY = "your-api-key-here"
```

### 🤖 Machine Learning (`ML/`)

Machine learning implementations and examples.

**Features:**
- MNIST digit classification with PyTorch
- Neural network architecture demonstration
- Training and evaluation pipelines

**Files:**
- `MNIST.py` - Complete MNIST classification pipeline

### 📊 Statistical Modeling (`stats/`)

Statistical analysis examples including Generalized Linear Models (GLM).

**Features:**
- Logistic regression with simulated data
- Data visualization with ggplot2
- Model diagnostics and interpretation

**Files:**
- `glm.qmd` - Quarto document with GLM analysis
- `glm.html` - Generated HTML report

### ⚡ Algorithms (`algos/`)

Algorithm implementations with performance optimizations.

**Features:**
- Multiple Fibonacci sequence implementations
- Performance comparison (recursive vs iterative vs memoization)
- Time complexity analysis

**Files:**
- `fib.py` - Four different Fibonacci implementations

### 🧬 Genomics Analysis (`genomics/`)

Single-cell RNA sequencing analysis examples.

**Files:**
- `singlecell.qmd` - Quarto document with analysis
- `singlecell.html` - Generated HTML report

## 🛠️ Technologies Used

### Python
- **Streamlit** - Web application framework
- **PyTorch** - Deep learning framework
- **Requests** - HTTP library for API calls

### R (Optional)
- **ggplot2** - Data visualization
- **Quarto** - Scientific and technical publishing

### APIs & Services
- **SNOMED CT API** - Medical terminology standards
- **IHTSDO** - International Health Terminology Standards

## 📈 Key Features

### Medical AI Assistant
- ✅ SNOMED CT integration for medical concept validation
- ✅ Evidence-based medical responses
- ✅ Professional safety disclaimers
- ✅ Interactive web interface

### Machine Learning
- ✅ MNIST digit classification
- ✅ Neural network implementation
- ✅ Training and evaluation pipelines
- ✅ GPU acceleration support

### Statistical Modeling
- ✅ Generalized Linear Models (GLM)
- ✅ Logistic regression examples
- ✅ Data visualization
- ✅ Model diagnostics

### Algorithms
- ✅ Multiple Fibonacci implementations
- ✅ Performance optimization techniques
- ✅ Time complexity analysis
- ✅ Educational code examples

## 🔧 Configuration

### Environment Setup

1. **Python Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install streamlit torch torchvision requests
```

2. **R Environment (Optional):**
```r
# Install required packages
install.packages(c("ggplot2", "rmarkdown", "knitr"))
```

### API Configuration

For the Medical AI Assistant, you'll need to:

1. Sign up for SNOMED CT API access at [IHTSDO](https://www.ihtsdo.org/)
2. Create a `.streamlit/secrets.toml` file:
```toml
SNOMED_API_KEY = "your-api-key-here"
```

## 🚀 Usage Examples

### Running the Medical AI Assistant
```bash
cd llm
streamlit run llm.py
```
Then open your browser to `http://localhost:8501`

### Running MNIST Classification
```bash
cd ML
python MNIST.py
```

### Running Fibonacci Algorithms
```bash
cd algos
python fib.py
```

### Generating Statistical Reports
```bash
cd stats
quarto render glm.qmd
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contact

- **Author:** Tara Friedrich
- **Email:** [your-email@example.com]
- **LinkedIn:** [your-linkedin-profile]
- **GitHub:** [your-github-profile]

## 🙏 Acknowledgments

- [IHTSDO](https://www.ihtsdo.org/) for SNOMED CT terminology
- [PyTorch](https://pytorch.org/) for deep learning framework
- [Streamlit](https://streamlit.io/) for web application framework

---

**Note:** This portfolio demonstrates various data science and AI techniques. The medical AI assistant is for educational purposes only and should not be used as a substitute for professional medical advice.
