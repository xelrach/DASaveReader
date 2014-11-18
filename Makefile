VERSION="alpha3"

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf dist

zip: clean
	mkdir dist
	zip -qr dist/DASaveReader-$(VERSION).zip pygff/ choice/ README LICENSE *.py
