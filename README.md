# iKevinY.github.io [![1]][2] <img align="right" width=76 src="content/images/icons/apple-touch-icon.png?raw=true"/>

This repository contains both the static site files and the source files used
to generate **[kevinyap.ca]**. The website is generated with [Pelican] using a
custom theme: [Pneumatic]. In order to host with [GitHub Pages], the repository
contains two distinct branches; the [`src`] branch contains the source files
that Pelican uses to generate the static files which are automatically
[pushed][generate.sh] to the [`master`] branch by Travis CI (see
[this blog post][travis-article] for more information on the process).

Code is licensed under the [MIT License], and articles under the [Creative
Commons Attribution-ShareAlike License].

[1]: http://img.shields.io/travis/iKevinY/iKevinY.github.io/src.svg?style=flat "Build Status"
[2]: https://travis-ci.org/iKevinY/iKevinY.github.io

[kevinyap.ca]: http://kevinyap.ca
[Pelican]: http://getpelican.com
[Pneumatic]: https://github.com/iKevinY/pneumatic
[`src`]: https://github.com/iKevinY/iKevinY.github.io/tree/src
[`master`]: https://github.com/iKevinY/iKevinY.github.io/tree/master
[GitHub Pages]: http://pages.github.com
[generate.sh]: generate.sh#L66
[travis-article]: http://kevinyap.ca/2014/06/deploying-pelican-sites-using-travis-ci/
[MIT License]: LICENSE
[Creative Commons Attribution-ShareAlike License]: http://creativecommons.org/licenses/by-sa/4.0/
