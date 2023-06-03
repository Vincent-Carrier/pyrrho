py := poetry run python
lexicons := data/ag/lsj.db
static := app/static
partials = $(wildcard build/**.html)
scss = $(wildcard $(static)/**.scss)
css = $(scss:.scss=.css)

.PHONY: default app partials css export test format clean

default: $(lexicons)
	poetry install
	npm install

watch:
	npx sass -Istyles -Inode_modules $(static):$(static) --watch &
	make app

app: $(lexicons)
	$(py) -m app.main

partials:
	$(py) scripts/partials.py

css: $(css)
$(css): $(scss)
	npx sass -Istyles -Inode_modules $(static):$(static)

test:
	poetry run pytest

format:
	poetry run black .

db_clean:
	rm -f $(lexicons)

partials_clean:
	rm -rf build/

assets_clean:
	rm -rf $(static)/**.map $(static)/**.css

$(lexicons):
	$(py) scripts/seed.py

