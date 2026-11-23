# run in the dir you want to start from, not from scripts/

rg --pcre2 --glob '*.py' \
  --glob '!**/migrations/**' \
  --glob '!**/__pycache__/**' \
  --glob '!**/__init__.py' \
  '^(?!\s*(?:from\b|import\b|$)).*\S' | wc -l