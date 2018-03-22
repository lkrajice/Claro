# other variables
MAX_LINE_WIDTH = 100
SOURCE = claro


# Make testing of style
styletest:
	autopep8 --max-line-length=$(MAX_LINE_WIDTH) --recursive --diff $(SOURCE) | colordiff
	flake8-2 --max-line-length=$(MAX_LINE_WIDTH) --ignore=W503 $(SOURCE)

# Delete all .pyc files
clean:
	find -name "*.pyc" -delete
