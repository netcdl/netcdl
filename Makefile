

test:
	PYTHONPATH=./netcdl py.test --verbose --cov-report term --cov=netcdl tests

testhtml:
	PYTHONPATH=./netcdl py.test --verbose --cov-report html --cov=netcdl tests

testwatch:
	PYTHONPATH=./netcdl ptw
