default: run

debug:
	@echo 'hi' && sleep 0.1 && >&2 echo 'bye from stderr'

err:
	@echo 'hi' && sleep 0.1 && >&2 echo 'bye from stderr' && exit 1

run:
	poetry run python cli.py

help:
	poetry run python cli.py help

spike:
	poetry run python cli.py debug

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
