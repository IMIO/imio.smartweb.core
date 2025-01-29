#!/usr/bin/make
.PHONY: buildout run cleanall test test-coverage
all: buildout

bin/buildout: bin/pip buildout.cfg
	bin/pip install -I -r requirements.txt

buildout: bin/instance

bin/instance: bin/buildout
	bin/buildout

bin/pip:
	python3.12 -m venv .

run: bin/instance
	bin/instance fg

test: bin/instance
	bin/test

test-coverage: bin/instance
	bin/test-coverage

cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib lib64 include bin .mr.developer.cfg local/

upgrade-steps:
	bin/instance -O plone run scripts/run_portal_upgrades.py
