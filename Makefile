run_all:
	docker-compose up -d
	airflow dags trigger data_pipeline

scrape:
	scrapy crawl gutenberg

etl:
	python src/etl.py

embed:
	python src/embed.py

serve:
	uvicorn src.api:app --host 0.0.0.0 --port 8001
