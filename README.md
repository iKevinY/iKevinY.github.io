# iKevinY.github.io

This repository contains both the static site files and the source code that generates [kevinyap.ca](http://kevinyap.ca). The site is generated with [Pelican](http://getpelican.com). In order to host with [GitHub Pages](http://pages.github.com), the repository contains two distinct branches; the `src` branch houses the source files that Pelican uses to generate the static files, and the `master` branch contains the generated files. The entire process is (somewhat) managed by `generate.sh`, which is used to test changes locally and push changes to the `master` branch. For further information, see [this blog post](http://kevinyap.ca/2013/12/hosting-with-github-pages/).

The website's styling is based on [Greg Reda](http://www.gregreda.com)'s [Simply](https://github.com/gjreda/gregreda.com/tree/master/theme/simply) theme, which is built using the [Skeleton](http://www.getskeleton.com) framework.
