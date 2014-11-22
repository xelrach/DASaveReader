VERSION="alpha6"

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf DASaveReader dist
	rm -f DASaveReader-*.zip

zip: clean lint
	mkdir DASaveReader
	mkdir dist
	cp -r pygff/ choice/ README LICENSE *.py DASaveReader
	zip -qr dist/DASaveReader-$(VERSION).zip DASaveReader

lint:
	pylint -E choice *.py
