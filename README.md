# Gutenberg Project

This project includes a Scrapy scraper, MinIO for object storage, DuckDB for tabular storage, Chroma for vector embeddings, and FastAPI for serving results.
Here is the link for descriptive video on this project:
(https://drive.google.com/file/d/1Exv9rxKQwd9ZUYvBgfekmQILz1QJ82r4/view?usp=sharing)


  The architecture of this project is as: 
  ┌──────────────────────────────┐
│     Scraper (src/scraper.py)│
│ - Uses BeautifulSoup         │
│ - Respects robots.txt        │
│ - Extracts raw HTML/text     │
│ - Stores raw .txt/.html in   │
│   MinIO /tmp/ or /bronze     │
└───────────────┬──────────────┘
                │
       Raw scraped data (.txt/.html)
                │
                ▼
┌──────────────────────────────┐
│        MinIO Object Store    │
│ - Buckets: /bronze, /silver, /gold│
│ - Stores raw and processed data  │
│ - Data mounted as volumes        │
└───────────────┬──────────────┘
                │
        Triggered by Airflow DAG
                │
                ▼
┌──────────────────────────────┐
│    Airflow Orchestrator (dags/) │
│ - DAG for ETL pipeline        │
│ - Bronze: cleans raw          │
│ - Silver: enriches            │
│ - Gold: ready-for-embedding   │
│ - Mounted in container        │
└───────────────┬──────────────┘
                │
          Loads structured data
                │
                ▼
┌──────────────────────────────┐
│      DuckDB Catalog (catalog/)│
│ - Catalogs structured tables │
│ - Can run SQL queries        │
│ - Supports querying gold layer │
└───────────────┬──────────────┘
                │
   Reads gold-layer cleaned text
                │
                ▼
┌──────────────────────────────┐
│   Embeddings Generator (src/)│
│ - Uses HuggingFace model     │
│   (all-MiniLM-L6-v2)         │
│ - Generates document vectors │
└───────────────┬──────────────┘
                │
        Stores vectors
                │
                ▼
┌──────────────────────────────┐
│  ChromaDB Vector Store (/embeddings) │
│ - Stores document embeddings │
│ - Persistent storage enabled │
└───────────────┬──────────────┘
                │
     Accessed via FastAPI endpoint
                │
                ▼
┌──────────────────────────────┐
│     FastAPI RAG API (src/)   │
│ - Endpoints: /rag/ingest, /rag/ask │
│ - Ingests data into vector DB│
│ - Queries vectors using question │
│ - Returns context documents  │
└───────────────┬──────────────┘
                │
    Sends prompt + context to LLM
                │
                ▼
┌──────────────────────────────┐
│        Ollama LLM (Local)    │
│ - Model: deepseek-llm        │
│ - Responds with answers      │
└──────────────────────────────┘
