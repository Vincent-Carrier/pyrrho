py = poetry run python -m
lexicons = data/ag/lsj.db

.PHONY: default app test format clean

default: $(lexicons)
	poetry install

app: $(lexicons)
	$(py) app.main

test:
	poetry run pytest

format:
	poetry run black .

clean:
	rm -f $(lexicons)

$(lexicons):
	$(py) seed

