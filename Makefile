py := poetry run python
lexicons := data/ag/lsj.db
static := app/static
partials := $(wildcard build/**.html)
scss := $(wildcard $(static)/**.scss)
css := $(scss:.scss=.css)

.PHONY: default app html css export test format clean

default: $(lexicons)
	poetry install
	npm install

watch:
	make css -- -w &
	npx browser-sync start -p :8000 -w -f $(static)/** core/** build/** --no-open &
	make app

app: $(lexicons)
	$(py) -m app.main

html: $(partials)
$(partials): $(lexicons)
	$(py) scripts/partials.py

css: $(css)
$(css): $(scss)
	npx sass --load-path=./styles $(static):$(static)

test:
	poetry run pytest

format:
	poetry run black .

db_clean:
	rm -f $(lexicons)

clean:
	rm -rf build $(css) $(static)/**.map

$(lexicons):
	$(py) scripts/seed.py

