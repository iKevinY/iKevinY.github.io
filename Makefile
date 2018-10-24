all: install build

build:
	@pelican -s publishconf.py

deploy:
	@./generate.sh deploy

diff:
	@./generate.sh diff

install:
	pip install -r requirements.txt
	gem install sass -v 3.4.25

serve:
	@./generate.sh serve

.PHONY: all build deploy diff install serve
