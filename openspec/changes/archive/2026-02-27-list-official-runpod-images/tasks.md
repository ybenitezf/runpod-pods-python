## 1. Setup

- [x] 1.1 Add `requests` dependency to `pyproject.toml`
- [x] 1.2 Run `uv sync` to install dependencies

## 2. Create list_templates.py

- [x] 2.1 Create `src/runpod_pods_demo/list_templates.py`
- [x] 2.2 Implement `load_api_key()` function
- [x] 2.3 Implement `get_official_images()` with REST API call
- [x] 2.4 Implement `print_images_table()` function
- [x] 2.5 Add error handling for API connection issues
- [x] 2.6 Add main entry point with exit codes

## 3. Code Quality

- [x] 3.1 Run `uv run ruff format` to format code
- [x] 3.2 Run `uv run ruff check` to lint
- [x] 3.3 Verify implementation against specs

## 4. Testing

- [x] 4.1 Run script with valid API key to verify output
- [x] 4.2 Test error handling (missing API key)
