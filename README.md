# iKevinY.github.io [![1]][2] <img align="right" width=76 src="content/images/icons/apple-touch-icon-152x152.png?raw=true"/>

This repository contains both the static site files and the source files used
to generate **[kevinyap.ca][kevinyap.ca]**. The site is generated with
[Pelican][pelican], and its theme ([Pneumatic][pneumatic]) is based on a theme
developed by [Greg Reda][greg-reda] using the [Skeleton][skeleton] framework.
In order to host with [GitHub Pages][gh-pages], the repository contains two
distinct branches; the `src` branch contains the source files that Pelican
uses to generate the static files which are automatically [pushed][deploy] to
the `master` branch by Travis CI (see [this blog post][travis-article] for
more information on the process).

Articles are licensed under a [Creative Commons Attribution 4.0 International License][cc-by-4.0].

[1]: http://img.shields.io/travis/iKevinY/iKevinY.github.io/src.svg?style=flat "Build Status"
[2]: https://travis-ci.org/iKevinY/iKevinY.github.io

[kevinyap.ca]: http://kevinyap.ca
[pelican]: http://getpelican.com
[pneumatic]: https://github.com/iKevinY/pneumatic
[greg-reda]: http://www.gregreda.com
[skeleton]: http://www.getskeleton.com
[gh-pages]: http://pages.github.com
[deploy]: https://github.com/iKevinY/iKevinY.github.io/blob/src/deploy.sh#L35
[travis-article]: http://kevinyap.ca/2014/06/deploying-pelican-sites-using-travis-ci/
[cc-by-4.0]: http://creativecommons.org/licenses/by/4.0/
