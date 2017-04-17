Title: Styling Code Blocks Using Pelican
Date: 2013-12-10

Although [Monokai](http://studiostyl.es/schemes/monokai) is my colour scheme of choice when coding in [Sublime Text 2](http://www.sublimetext.com), it was not the best option for displaying code blocks on my website. Favouring a lighter colour scheme, I opted to use a GitHub style colour scheme and also add line numbers (because why not). Referring to a [blog post by Alex Peattie](http://alexpeattie.com/blog/github-style-syntax-highlighting-with-pygments/) explaining how to implement this using Pygments, I made some modifications to make it work with my website. While the process is largely the same as what he already explained, I felt like writing this Pelican-specific guide on the off chance that it might be useful to somebody in the future.

While Alex's tutorial implemented line numbering using CSS, the [CodeHilite](http://pythonhosted.org/Markdown/extensions/code_hilite.html) extension for [Python-Markdown](https://pypi.python.org/pypi/Markdown) has the option to add line numbers automatically, which saves a bit of work. To enable them, CodeHilite's `linenums` setting needs to be set to `True`. This can be done through the `MD_EXTENSIONS` option in the settings file supplied to Pelican.

```
#!python
MD_EXTENSIONS = ['codehilite(linenums = True)']
```

The next step is to download a stylesheet that is compatible with Pygments. I used the one [linked in Alex's tutorial](https://github.com/richleland/pygments-css/blob/master/github.css), but deleted the first line of the file because I did not need to change the background colour of the code block. This stylesheet should be linked to in the base template file of your website -- `base.html` for the theme that I am currently using.

Some custom styling is then done in order to change the appearance of the code blocks. The following three blocks of code would be placed in the primary stylesheet of the site's theme. First of all, basic styling is added to the code block to control basic properties of the code, as well as create the border around the code block and ensure that it scrolls correctly if a line of code is too large for the block. While this is generally not an issue when being viewed on a computer screen, it is important for if the code is being viewed on a mobile device.

```
#!css
.codehilitetable {
	font-family: "Source Code Pro", monospace;
	font-size: 12px;
	overflow: auto;
	display: block;
	border: solid 1px #d9d9d9;
	border-radius: 3px;
}
```

Following this, the line numbering is styled by modifying the `linenos` class. The background of the numbering is made grey, the sides of the actual line numbers are padded, and a border is added separating the numbering from the actual code. The multitude of vendor-prefixed `user-select` properties are added in order to make the line numbers unselectable making selecting and copying code a lot easier.

The horizontal margins of the `codehilite` class, which controls the code itself, are increased to add spacing between the code snippets and the line numbers.

```
#!css
.linenos {
	border-right: 1px solid #d9d9d9;
	background: #eee;
	padding: 0.5em 0.8em;
	-webkit-user-select: none;
	-khtml-user-select: none;
	-moz-user-select: none;
	-ms-user-select: none;
	user-select: none;
}

.codehilite {
	margin: 0 1em;
}
```

After following these steps, everything should be working properly. Of course, the stylesheet used and properties of the code blocks can be changed depending on personal preference.
