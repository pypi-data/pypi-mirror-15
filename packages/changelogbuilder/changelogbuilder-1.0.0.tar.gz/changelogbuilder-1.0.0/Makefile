install:
	virtualenv -p /usr/bin/python3 venv
	venv/bin/pip install -r requirements.txt


deps:
	sudo apt-get install git
	

deps_mac:
	brew install git

test:
	rm -rf .tox
	detox

clean:
	rm -rf venv

tag-release:
	sed -i "/__version__/c\__version__ = '$(v)'" changelogbuilder/__init__.py
	git add changelogbuilder/__init__.py && git commit -m "Automated version bump to $(v)" && git push
	git tag -a release/$(v) -m "Automated release of $(v) via Makefile" && git push origin --tags

package:
	rm -rf build
	python setup.py clean
	python setup.py build sdist bdist_wheel

distribute:
	twine upload -r pypi -s dist/changelogbuilder-$(v)*

release:
	$(MAKE) tag-release
	$(MAKE) package
	$(MAKE) distribute
