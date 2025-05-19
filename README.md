# Social Workout

## Documentation

https://socialworkout-api.samiarar.com/docs

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

### Deploy with Docker

```bash
docker-compose up --build -d
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
