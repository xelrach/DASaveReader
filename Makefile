VERSION="snapshot"

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf DASaveReader dist
	rm -f DASaveReader-*.zip

zip: lint test clean
	mkdir DASaveReader
	mkdir dist
	cp -r pygff/ choice/ CHANGELOG README LICENSE *.py DASaveReader
	zip -qr dist/DASaveReader-$(VERSION).zip DASaveReader
	@echo "ZIP created"

lint: clean
	pylint -E choice *.py

test: clean
	python test_suite.py
