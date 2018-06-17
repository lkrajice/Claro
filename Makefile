# other variables
MAX_LINE_WIDTH = 100
SOURCE = claro


# Make testing of style
styletest:
	flake8 --max-line-length 100 . --exclude "staticfiles/bower_components, ./*/migrations/"

reset:
	-rm db.sqlite3
	-find . -path "*/migrations/*.pyc" -delete
	-find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	./manage.py makemigrations
	./manage.py migrate


# Delete all .pyc files
clean:
	find -name "*.pyc" -delete
