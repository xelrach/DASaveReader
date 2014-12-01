VERSION="alpha9"

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf DASaveReader dist
	rm -f DASaveReader-*.zip

zip: clean lint test clean
	mkdir DASaveReader
	mkdir dist
	cp -r pygff/ choice/ CHANGELOG README LICENSE *.py DASaveReader
	zip -qr dist/DASaveReader-$(VERSION).zip DASaveReader
	@echo "ZIP created"

lint:
	pylint -E choice *.py

test:
	python choice/test_suite.py
