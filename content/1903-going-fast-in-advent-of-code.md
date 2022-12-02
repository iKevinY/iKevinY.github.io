Title: Going Fast in Advent of Code
Date: 2019-12-08

I have been a big fan of [Advent of Code](https://adventofcode.com) since it started back in 2015, and have spent every December since diligently solving as many problems as I can right at 9pm. Rather than a chocolate hiding behind each day like with a regular advent calendar, in Advent of Code, every day brings a two-part holiday-themed puzzle -- the first part introducing the context, and the second part building on the theme of the first.

I think my favourite part of Advent of Code is that, unlike with [ICPC-style](https://en.wikipedia.org/wiki/International_Collegiate_Programming_Contest) programming contests, the puzzles are simpler and don't require knowledge of esoteric algorithms to solve. This makes it more approachable to a wider variety of people, and can also be done for fun and used as a learning tool.

There are a lot of developers who work through Advent of Code at a relaxed pace, either to help learn a new programming language or solidify their skills in general, but every year there is a dedicated group of people who compete for [global leaderboard points](https://adventofcode.com/2019/leaderboard).

The first 100 people to collect a "star" (ie. solve a part of the puzzle) on each day collect points based on what position they finished in. I have placed somewhere on the global leaderboard every year (peaking at 11th place in 2016), but the competition is only getting tougher. The top competitors often clock in at under 5 minutes for finishing *both parts* of the problem.

This year, I decided it would be a good idea to also use Advent of Code as an opportunity to help other developers learn as well, so I decided to start [streaming my attempts](https://www.twitch.tv/Pewqazz) (with a delay to preserve the sanctity of the global leaderboard). Since I can't multi-task and narrate my solves when I'm competing for points, I also decided to write up this blog post to describe my general approach to solving problems, to help other people who are also aiming to land on the leaderboard.


## Pre-Solve

Solving an Advent of Code problem quickly starts before the day's puzzle even unlocks. Being well-prepared is key, since getting off on the wrong foot puts you at an instant disadvantage.

### Language

My language of choice is Python, and I imagine a significant portion of the global leaderboard regulars also use Python. While it has characteristics that arguably make it not the optimal choice for production software engineering, there are a number of reasons that I like Python:

**Light on syntax**. Python reads and writes like pseudocode, meaning once I have a rough outline of the correct algorithm in my head, there is less of a barrier to translating it into code than with other, more verbose languages.

**No typing**. Types requiring typing (on your keyboard), and keystrokes are valuable when you want to go fast. In addition, taking advantage of [duck typing](https://en.wikipedia.org/wiki/Duck_typing) often leads to janky but short implementations than something that is formally correct.

**Powerful standard library**. Python has an extremely powerful standard library. If you write Python and don't know about [`collections`](https://docs.python.org/3/library/collections.html) and [`itertools`](https://docs.python.org/3/library/itertools.html), learn them now.

Regardless of what language you choose, you should definitely be familiar with basic control flow structure and common idioms of that language. There's one thing that's faster than reading through documentation, and that's *not having to read through documentation*.

### Editor

I use Sublime Text with "Vintage Mode" enabled for Vim keybindings. I'm not proficient enough with Vim to jump around without my mouse 100% of the time, and Sublime's multi-cursor / multi-edit keybindings are deeply ingrained in my muscle memory. Really though, the best editor is the one that you are most comfortable with, since fumbling around with an unfamiliar environment is not a great feeling when you're aiming for speed.

### Miscellaneous

Instead of starting with a blank file, I use a [starter template](https://github.com/iKevinY/advent/blob/master/2019/starter.py) that contains useful `import`s, as well as some preliminary code to parse the problem input. I've also built up a [utility methods file](https://github.com/iKevinY/advent/blob/master/2019/utils.py) that contains some useful things, though the majority of the time I forget what I've written in them. Still, it's nice to have.

I also have an alias (`aoc`) that is mapped to `pbpaste | python file.py`. On macOS, `pbpaste` will `echo` the current contents of your clipboard. This allows me to quickly swap between running my program on the sample inputs and the true input just by leveraging my clipboard, instead of having to juggle different input files around. (This is probably my favourite tip.)

Building on this, you should at least have *some* alias that runs your program (and compiles it if you're working in a compiled language). Minimizing iteration time is key, as when a bug inevitably crops up, you want to be able to quickly make changes and test your new implementation.


## Solving the Problem

With the pre-solve out of the way, we can finally get to solving the actual problem itself. This is a two-step process: 1) read the word problem and turn it into an algorithm, then 2) turn the algorithm into a *bug-free program*. This is, of course, easier said than done, so let's break it down further.

### Reading the Problem

While it may be natural to read the problem from top to bottom, I find that it is faster to *go in reverse*, starting at the bottom of the problem and working backwards.

**Scroll to the bottom and open the puzzle input**. Just by glancing at the puzzle input, you may be able to intuit what type of an implementation you will need to write. Does it look like a bunch of different passwords, one per line, that we will probably need to iterate over and validate? Or maybe they seem like coordinates in 3-D space. Knowing what the input looks like often provides a nice framework for reading through the actual problem.

**Read the goal of the puzzle**. The final paragraph of the problem text will describe the goal of the puzzle (what you will need to type into the text box). The bolded text will clue you into some keywords or key ideas that will help guide the reading of the rest of the problem.

**Look at the sample test cases**. The test cases will provide a pretty good idea of how the problem input gets transformed into the desired output. It might even be possible to guess at the algorithm without even reading the rest of the problem text!

**Parse missing information from the rest of the problem**. At this point, continue reading upwards, making liberal use of `Ctrl+F` to seek out whatever information is necessary to complete your understanding of the problem.

With that, it's time for the fun part.

### Write the Code

There isn't really a sure-fire procedure for "writing the correct program", so I'll just provide some tips instead.

**Know your data structures and algorithms**. While not ICPC-level, it will be tricky to get through Advent of Code without at least a basic understanding of DS&A. At a bare minimum, being familiar with your language's [hash table](https://en.wikipedia.org/wiki/Hash_table), and be comfortable with constructing and [traversing graphs](https://en.wikipedia.org/wiki/Breadth-first_search).

**Utilize the test cases**. The test cases are doubly helpful because they provide us with something to test our implementation on later on. Submitting an incorrect result is extremely punishing, and there's no worse feeling than having to wait over a minute to submit after implementing a 5-second bug fix.

**Debug efficiently**. Nobody writes bug-free code all the time, and writing bug-free code is even harder when under time pressure. This means that being efficient at debugging your code is all the more important. At a high level, this means getting good at "guessing" at what point in your code you may have typo'd or forgotten something, so that the "problem spot" can be identified as quickly as possible. This comes with practice.

----

If you want to see what all of this looks like in action, I created a [collection of my streamed attempts here](https://www.twitch.tv/collections/cspts5QT3RUiTA). I'm also hoping to upload a slower, narrated solve that goes through the concepts discussed in this post (I attempted to do this earlier today, but accidentally just created a 40-minute long silent film).

Happy Advent of Coding! 🎄

----

**Edit: December 2, 2022**

It's been a few years since I wrote this post, and figured it was due for an update! Both [betaveros](https://blog.vero.site/post/advent-leaderboard) and [mcpower](https://gist.github.com/mcpower/87427528b9ba5cac6f0c679370789661), two people who perform *significantly* better on the global leaderboard than I do, have written their own posts with tips and tricks for going quickly; I highly recommend giving them a read.

Also, for 2022, I'm [streaming my attempts on YouTube](https://www.youtube.com/@iKevinY) -- come watch if you're interested!
