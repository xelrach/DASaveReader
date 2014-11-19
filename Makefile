VERSION="alpha4"

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf DASaveReader dist
	rm -f DASaveReader-*.zip

zip: clean
	mkdir DASaveReader
	mkdir dist
	cp -r pygff/ choice/ README LICENSE *.py DASaveReader
	zip -qr dist/DASaveReader-$(VERSION).zip DASaveReader
