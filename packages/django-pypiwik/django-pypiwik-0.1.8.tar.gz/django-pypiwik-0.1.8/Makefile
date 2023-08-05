TARGET?=tests

clean:
	rm -r dist build src/*.egg-info

test:
	PYTHONPATH=".:./src" python tests/

coverage:
	coverage erase
	PYTHONPATH=".:./src" coverage run --source='src' --omit='src/test.py' --branch tests/__main__.py
	coverage report -m

release:
	python setup.py sdist upload -r pypi
