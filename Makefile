.PHONY: build push release

build:
	python setup.py sdist bdist_wheel

push:
	python3 -m twine upload dist/*

release: build push
