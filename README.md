# iKevinY.github.io [![1]][2] <img align="right" width=76 src="theme/static/images/apple-touch-icon-152x152.png?raw=true"/>

This repository contains both the static site files and the source code that generates [kevinyap.ca](http://kevinyap.ca). The site is generated with [Pelican](http://getpelican.com). In order to host with [GitHub Pages](http://pages.github.com), the repository contains two distinct branches; the `src` branch houses the source files that Pelican uses to generate the static files, and the `master` branch contains the generated files. The entire process managed by Travis CI, which runs `deploy.sh` to generate the site file and push them to the `master` branch (see [this blog post](http://kevinyap.ca/2014/06/deploying-pelican-sites-using-travis-ci/) for more information).

The website's styling is based on [Greg Reda](http://www.gregreda.com)'s [Simply](https://github.com/gjreda/gregreda.com/tree/master/theme/simply) theme, which is built using the [Skeleton](http://www.getskeleton.com) framework.

[1]: http://img.shields.io/travis/iKevinY/iKevinY.github.io/src.svg?style=flat "Build Status"
[2]: https://travis-ci.org/iKevinY/iKevinY.github.io
