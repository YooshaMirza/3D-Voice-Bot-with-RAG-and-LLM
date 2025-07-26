# Offline Model Usage

If you encounter authentication issues with Hugging Face when downloading the model, you can manually download and set up the model by following these steps:

1. Visit https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 and create an account if needed
2. Download the model files manually
3. Place the downloaded files in the `model_cache` directory with the following structure:

```
model_cache/
  └── sentence-transformers/
      └── all-MiniLM-L6-v2/
          ├── config.json
          ├── pytorch_model.bin
          ├── sentence_bert_config.json
          ├── special_tokens_map.json
          ├── tokenizer_config.json
          └── vocab.txt
```

Alternatively, you can use a different environment variable to specify your Hugging Face token:

```
HUGGINGFACE_TOKEN=your_token_here
```

Add this to your .env file.
