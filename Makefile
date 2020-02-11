default: run

run:
	poetry run python cli.py

deps:
	poetry run pip freeze > requirements.txt

spec:
	docker run -v "$(PWD):/src/" cdrx/pyinstaller-linux "pyinstaller --onefile cli.py"

build:
	docker run -v "$(PWD):/src/" cdrx/pyinstaller-linux

cp:
	sudo cp dist/linux/cli /usr/local/bin/ot

install: spec build cp

clean:
	sudo rm -rf build
	sudo rm -rf dist

.PHONY: build
