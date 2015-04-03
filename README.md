# iKevinY.github.io [![1]][2] <img align="right" width=76 src="content/images/icons/apple-touch-icon-152x152.png?raw=true"/>

This repository contains both the static site files and the source files used
to generate **[kevinyap.ca]**. The site is generated with [Pelican], and its
theme ([Pneumatic]) is based on a theme developed by [Greg Reda] using the
[Skeleton] framework. In order to host with [GitHub Pages], the repository
contains two distinct branches; the [`src`] branch contains the source files
that Pelican uses to generate the static files which are automatically
[pushed][generate.sh] to the [`master`] branch by Travis CI (see
[this blog post][travis-article] for more information on the process).

Code is licensed under the [MIT License], and articles under a [Creative
Commons Attribution License].

[1]: http://img.shields.io/travis/iKevinY/iKevinY.github.io/src.svg?style=flat "Build Status"
[2]: https://travis-ci.org/iKevinY/iKevinY.github.io

[kevinyap.ca]: http://kevinyap.ca
[Pelican]: http://getpelican.com
[Pneumatic]: https://github.com/iKevinY/pneumatic
[Greg Reda]: http://www.gregreda.com
[Skeleton]: http://www.getskeleton.com
[`src`]: https://github.com/iKevinY/iKevinY.github.io/tree/src
[`master`]: https://github.com/iKevinY/iKevinY.github.io/tree/master
[GitHub Pages]: http://pages.github.com
[generate.sh]: https://github.com/iKevinY/iKevinY.github.io/blob/src/generate.sh#L44
[travis-article]: http://kevinyap.ca/2014/06/deploying-pelican-sites-using-travis-ci/
[MIT License]: http://github.com/iKevinY/iKevinY.github.io/blob/src/LICENSE
[Creative Commons Attribution License]: http://creativecommons.org/licenses/by/4.0/
