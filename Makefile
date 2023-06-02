py := poetry run python
lexicons := data/ag/lsj.db
partials := $(wildcard build/**.html)
css := $(wildcard static/**.css)
scss := $(wildcard static/**.scss)

.PHONY: default app html export test format clean

default: $(lexicons)
	poetry install
	npm install

watch:
	make $(css) -- -w &
	npx browser-sync start -p 0.0.0.0:8000 -w -f static/** core/** build/** --no-open &
	make app

app: $(lexicons)
	$(py) -m app.main

html: $(partials)

$(partials): $(lexicons) $(wildcard core/render/**)
	$(py) scripts/partials.py

$(css): $(scss)
	sass --load-path=./styles static:static

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

