## 1. Update Imports

- [x] 1.1 Update `scripts/list_gpus.py` to import `load_api_key` from `create_pod` instead of `create_template`

## 2. Rename Environment Variable

- [x] 2.1 In `src/runpod_pods_demo/create_pod.py`, rename variable `template_env` to `pod_env`
- [x] 2.2 Update the `os.getenv("TEMPLATE_ENV")` call to `os.getenv("POD_ENV")`

## 3. Delete Template Files

- [x] 3.1 Delete `src/runpod_pods_demo/create_template.py`
- [x] 3.2 Delete `src/runpod_pods_demo/delete_template.py`
- [x] 3.3 Delete `src/runpod_pods_demo/list_templates.py`

## 4. Verify

- [x] 4.1 Run `uv run ruff format` to check formatting
- [x] 4.2 Run `uv run ruff check` to verify no import errors
- [x] 4.3 Verify `main.py` still works (can test import)
