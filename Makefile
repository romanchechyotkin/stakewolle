activate:
	source venv/bin/activate

lint:
	isort .

requirements:
	pip freeze > requirements.txt

install_deps:
	pip install -r requirements.txt
