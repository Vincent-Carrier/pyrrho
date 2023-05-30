py := poetry run python
lexicons := data/ag/lsj.db
chunks := $(wildcard build/chunks/**.html)
css := static/styles.css
sass := $(wildcard styles/**.sass)

.PHONY: default app html export test format clean

default: $(lexicons)
	poetry install
	npm install

app: $(lexicons)
	$(py) -m app.main

html: $(chunks)

.DELETE_ON_ERROR:
$(html): $(lexicons)
	./pyrrho build ag nt

$(css): $(sass)
	sass styles/styles.sass $@

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

