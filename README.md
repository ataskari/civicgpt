# CivicGPT - Social Media Post Reviewer

An AI-powered assistant that reviews social media posts before publication to prevent violations, improve tone, and reduce reputational risk.

## 🎯 What is CivicGPT?

CivicGPT acts as a "second pair of eyes" for social media content creators. It analyzes draft posts for:

- **Sentiment Analysis**: Detects positive, negative, or neutral tone
- **Toxicity Detection**: Identifies potentially harmful language
- **Platform Policy Compliance**: Checks against Twitter/X community guidelines
- **Ethical & Legal Risks**: Flags potential reputational or legal issues
- **Improvement Suggestions**: Provides actionable edits and alternatives

## 🚀 Features

### Core Analysis
- **Real-time Post Review**: Get instant feedback on your draft posts
- **Multi-dimensional Analysis**: Sentiment, toxicity, policy compliance, and ethical risks
- **Platform-Specific Rules**: Currently supports Twitter/X policies
- **Actionable Suggestions**: Receive specific improvement recommendations

### User Experience
- **Clean Web Interface**: Simple, intuitive Streamlit frontend
- **Fast Processing**: Analysis completed in under 3 seconds
- **Clear Results**: Easy-to-understand feedback with severity indicators
- **Export Options**: Copy improved versions or export analysis

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **AI/LLM**: OpenAI GPT API
- **NLP**: TextBlob, VADER Sentiment
- **Containerization**: Docker
- **Testing**: Pytest

## 📁 Project Structure

```
civicgpt/
├── api/                    # FastAPI backend
├── frontend/              # Streamlit frontend
├── services/              # AI/NLP services
│   ├── prompting/         # Prompt templates
│   └── analysis/          # Analysis engines
├── utils/                 # Utility functions
├── config/                # Configuration files
├── tests/                 # Test suite
├── docker/                # Docker files
└── logs/                  # Application logs
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Docker (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd civicgpt
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

4. **Run the application**
   ```bash
   # Start the FastAPI backend
   uvicorn api.main:app --reload
   
   # In another terminal, start the Streamlit frontend
   streamlit run frontend/app.py
   ```

### Docker Deployment

1. **Build and run with Docker**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: http://localhost:8501
   - API: http://localhost:8000

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key_here
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### API Endpoints

- `POST /api/analyze`: Analyze a social media post
- `GET /api/health`: Health check endpoint

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 📊 Performance Metrics

- **Analysis Time**: < 3 seconds per post
- **Accuracy**: Manual verification on sample dataset
- **Suggestion Rate**: % of posts receiving actionable suggestions

## 🔮 Future Enhancements

- Multi-platform support (Instagram, LinkedIn, TikTok)
- Browser extension for real-time review
- User feedback loop for AI improvement
- Multilingual support
- Advanced analytics dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ for content creators who want to make a positive impact online.** 