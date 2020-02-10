default: run

run:
	poetry run python main.py

requirements.txt:
	poetry run pip freeze > $@

deps: requirements.txt

spec:
	docker run -v "$(PWD):/src/" cdrx/pyinstaller-linux "pyinstaller main.py"

build: deps
	docker run -v "$(PWD):/src/" cdrx/pyinstaller-linux

clean:
	sudo rm -rf build
	sudo rm -rf dist

.PHONY: build dist
