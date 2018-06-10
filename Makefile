# other variables
MAX_LINE_WIDTH = 100
SOURCE = claro


# Make testing of style
styletest:
	autopep8 --max-line-length=$(MAX_LINE_WIDTH) --recursive --diff $(SOURCE) | colordiff
	flake8-2 --max-line-length=$(MAX_LINE_WIDTH) --ignore=W503 $(SOURCE)

reset:
	-rm db.sqlite3
	-find . -path "*/migrations/*.pyc" -delete
	-find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	./manage.py makemigrations
	./manage.py migrate


# Delete all .pyc files
clean:
	find -name "*.pyc" -delete
