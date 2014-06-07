PY=python
PELICAN=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
TEMPDIV=$(BASEDIR)/develop
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

help:
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make devserver                   start local dev server             '
	@echo '   make github                      upload the web site via gh-pages   '
	@echo '                                                                       '

devserver:
	bash generate.sh -d

publish:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

github: publish
	cp .travis.yml output/
	ghp-import -b travis-test $(OUTPUTDIR) -m "Automatically built site files."
	@git push -fq https://${GH_TOKEN}@github.com/$(TRAVIS_REPO_SLUG).git master > /dev/null

.PHONY: devserver publish github
