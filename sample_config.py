app:
  name: gutenberg_project
  version: 1.0

data:
  input_dir: data/raw
  output_dir: data/processed
  allowed_extensions: [".txt", ".pdf"]

preprocessing:
  remove_stopwords: true
  lowercase: true
  min_word_length: 3

model:
  embedding_type: "tfidf"
  max_features: 10000

logging:
  level: INFO
  log_file: logs/app.log
