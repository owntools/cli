default: run

run:
	poetry run python main.py

deps:
	poetry run pip freeze > requirements.txt

spec:
	docker run -v "$(PWD):/src/" cdrx/pyinstaller-linux "pyinstaller main.py"

build:
	docker run -v "$(PWD):/src/" cdrx/pyinstaller-linux

cp:
	sudo cp dist/linux/main /usr/local/bin/ot

install: build cp

clean:
	sudo rm -rf build
	sudo rm -rf dist

.PHONY: build
