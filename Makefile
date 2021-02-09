#!/usr/bin/make
.PHONY: buildout cleanall test instance

bin/pip:
	python3 -m venv .
	touch $@

bin/buildout: bin/pip
	./bin/pip install -r requirements.txt
	touch $@

buildout: bin/buildout
	./bin/buildout -t 7

test: buildout
	./bin/test

instance: buildout
	./bin/instance fg

cleanall:
	rm -rf bin develop-eggs downloads include lib lib64 parts .installed.cfg .mr.developer.cfg bootstrap.py parts/omelette local share
