default: run

run:
	poetry run python cli.py

deps:
	poetry run pip freeze > requirements.txt

spec:
	docker run --rm -it -v "$(PWD):/src/" cdrx/pyinstaller-linux "pyinstaller --onefile cli.py"

build:
	docker run --rm -it -v "$(PWD):/src/" cdrx/pyinstaller-linux

setup:
	env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.6.10
	cd ..; cd cli; pip install pyinstaller; pip install -r requirements.txt

mac:
	# pyinstaller --onefile cli.py
	pyinstaller --clean -y --dist ./dist/mac --workpath /tmp *.spec
	cp dist/mac/cli /usr/local/bin/ot

cp:
	sudo cp dist/linux/cli /usr/local/bin/ot

install: spec build cp

clean:
	sudo rm -rf build
	sudo rm -rf dist

.PHONY: build
