.PHONY: app
py = poetry run python
lexicons = data/lsj.db

app: $(lexicons)
	$(py) -m app.main

.DEFAULT: $(lexicons)
	$(py) -m cli.main

$(lexicons):
	$(py) -m core.seed
