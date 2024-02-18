# Social Workout

## Development

### Install dependencies

```bash
pip install -r .\requirements.txt
pip install -r .\requirements-dev.txt
```

### Hot reload

```bash
uvicorn socialworkoutapi.main:app --reload
```

### Pytest

run pytest:

```bash
pytest

# verbose
pytest -v

# show all the fixtures available in the defined tests
pytest --fixtures

# display, for each test, which fixtures it uses
pytest --fixtures-per-test
```
