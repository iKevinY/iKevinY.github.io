This (currently nameless) single-author Pelican theme is derived from a [theme](https://github.com/gjreda/gregreda.com/tree/master/theme/simply) developed by [Greg Reda](http://www.gregreda.com) based on the [Skeleton](http://www.getskeleton.com) framework. There are no templates for author, category, and tag pages, so `AUTHORS_SAVE_AS`, `CATEGORY_SAVE_AS`, `CATEGORIES_SAVE_AS`, and `TAGS_SAVE_AS` should all be set to `''`. Here are theme-specific settings that should be present in the Pelican configuration file:

|  Variable           | Description                                            |
|:-------------------:|--------------------------------------------------------|
| `SITENAME`          | Text displayed under avatar in sidebar                 |
| `BIO_TEXT`          | Text displayed under site name                         |
| `FOOTER_TEXT`       | Text displayed in site footer                          |
| `SITE_AUTHOR`       | Used for author `<meta>`                               |
| `TWITTER_USERNAME`  | Used for Twitter Cards `<meta>`                        |
| `GOOGLE_PLUS_URL`   | Used for Google+ `<meta>`                              |
| `INDEX_DESCRIPTION` | Used for description `<meta>` on index page            |
| `SIDEBAR_LINKS`     | List of links displayed under bio text                 |
| `SOCIAL_ICONS`      | List of tuples in the form `(link, title, icon-class)` |


## Screenshots

![Index Page](screenshots/index.png?raw=true)

![Article](screenshots/article.png?raw=true)

![Archive](screenshots/archive.png?raw=true)
