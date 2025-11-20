# Cold Email Generator

A Streamlit application that generates personalized cold emails for job postings using Groq's LLM API.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Groq API key:
   - Get your API key from [Groq Console](https://console.groq.com/)
   - Create a `.env` file in the root directory
   - Add the following line to `.env`:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. Run the application:
```bash
streamlit run app/main.py
```

## Usage

Enter a job posting URL in the Streamlit interface, and the application will:
1. Scrape the job posting from the URL
2. Extract job details (role, experience, skills, description)
3. Match relevant portfolio items based on skills
4. Generate a personalized cold email

## Requirements

- Python 3.8+
- Groq API key

## Troubleshooting

### ChromaDB Connection Error

If you encounter a `ValueError: Could not connect to tenant default_tenant` error:

1. The application will automatically try to fix this by removing and recreating the vectorstore
2. If the error persists, manually delete the `vectorstore` directory in the project root
3. The vectorstore will be automatically recreated on the next run