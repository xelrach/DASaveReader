VERSION="snapshot"

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf DASaveReader
	rm -f DASaveReader-*.zip

zip: clean
	mkdir DASaveReader
	mkdir dist
	cp -r pygff/ choice/ README LICENSE *.py DASaveReader
	zip -qr dist/DASaveReader-$(VERSION).zip DASaveReader
