py = poetry run python
lexicons = data/ag/lsj.db

.PHONY: default app test format clean

default: $(lexicons)
	poetry install

app: $(lexicons)
	$(py) -m app.main

html: $(lexicons)
	./pyrrho build ag nt

test:
	poetry run pytest

format:
	poetry run black .

db_clean:
	rm -f $(lexicons)

clean:
	rm -rf build

$(lexicons):
	$(py) scripts/seed.py

