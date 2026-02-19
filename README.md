# CSV Chatbot

Built using FastAPI, Streamlit, Pandas, and Google Gemini API.

---


## How it is structured

The backend is a FastAPI application with a single POST endpoint at `/ask`. It loads the dataset once at startup, then for every request it runs three steps: parse the question into a structured query, execute that query on the DataFrame, and generate a natural language answer. Each of those steps lives in its own service module.

```
csv_chatbot/
├── api/
│   └── main.py                 — FastAPI app, /ask endpoint
├── data/
│   └── books_cleaned.csv       — The dataset
├── services/
│   ├── llm_parser.py           — Converts natural language to structured query
│   ├── preprocessing.py        — Cleans and normalizes the CSV on load
│   ├── query_executor.py       — Runs filters, sorting, and limit on the DataFrame
│   └── response_generator.py  — Generatea the natural language answer via Gemini
├── utils/
│   └── prompts.py              — Prompting templates
├── app.py                      — Streamlit frontend
├── .env                        — API key 
└── requirements.txt
```
---

## API response format

Every response from the `/ask` endpoint 

The `response` field is the natural language answer. The `metadata` array contains the raw book records that were used to generate it.

---

## To run it locally

We will need a Gemini API key from Google AI Studio(https://aistudio.google.com/app/apikey).

```bash
# Clone and enter the project
git clone https://github.com/Dikashmashree/csv_chatbot.git
cd csv_chatbot

# Set up environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux

pip install -r requirements.txt

# Add your API key
echo GEMINI_API_KEY=your_key_here > .env

# Terminal 1 — start the backend
uvicorn api.main:app --reload

# Terminal 2 — start the frontend
streamlit run app.py
```

The API will be at `http://127.0.0.1:8000` and the chat interface at `http://localhost:8501`. The interactive API docs are at `http://127.0.0.1:8000/docs`.

---

## Tech stack

- Python 3.10+
- FastAPI and Uvicorn for the backend
- Google Gemini (`gemini-2.5-flash-latest`) for query parsing and answer generation
- Pandas for data processing and querying
- Streamlit for the frontend
- python-dotenv for environment config

---

## Dataset

The dataset has thee following columns: `isbn13`, `title`, `subtitle`, `authors`, `categories`, `description`, `published_year`, `average_rating`, `num_pages`, `ratings_count`.


---

## Demo
https://github.com/user-attachments/assets/7d12d235-cd9e-4cee-8694-ca229bc37a5c


