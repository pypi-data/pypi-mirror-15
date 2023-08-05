SRC = $(shell pwd)

all: build

.PHONY: build docs

docs:
	cd docs; make html

build:
	python setup.py build_ext --inplace

clean:
	python setup.py clean
	rm -r -f pyspace/*.cpp

cleanall: clean
	rm -r -f pyspace/*.so

install:
	python setup.py install

develop:
	python setup.py develop

test:
	python2 `which nosetests` --exe -v pyspace

