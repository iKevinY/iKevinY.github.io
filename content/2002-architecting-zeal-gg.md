Title: Architecting zeal.gg
Date: 2020-03-01
Slug: architecting-zeal-gg

Back while I was interning at Riot Games, I spent one weekend throwing together a prototype for what would eventually become [zeal.gg](https://zeal.gg). The purpose of it was to graph the [solo queue ranking](https://support-leagueoflegends.riotgames.com/hc/en-us/articles/4406004330643-Ranked-Tiers-Divisions-and-Queues) of our intern cohort while we were working there, since like most of the League of Legends population, a handful of us got really competitive about it.

I ended up registering the domain name for fun; _Zeal_ is an item you can purchase in the game, and I was surprised to find that such a short domain name wasn't taken yet. Having a nice domain gave me grander ambitions for the site -- I wanted to polish it up and make it available for other League players to use with their friend groups as well.

This was the perfect task to occupy my free time, since I ended up taking the fall semester of my the final year of my undergrad off. While the initial MVP was a single page that graphed our ranks, the final product would need a landing page where anyone could create a leaderboard for their own friend group.

I worked on final version of the site during November and December, and made an [announcement on /r/leagueoflegends](https://www.reddit.com/r/leagueoflegends/comments/agp6qj/introducing_zealgg_custom_solo_queue_leaderboards) the week before the new ranked season started the following January. To my surprise, over 10k people visited the site on the day I made the post, and I continued to have hundreds of consistent users for weeks afterwards! To top it all off, it still hasn't gone down yet: a mild reassurance that I at least somewhat know what I'm doing in this profession.


## The Stack

I learned a ton building the site; taking an idea from inception to production involves so much more than anything taught in school (which is the reason that working on personal projects is an oft-encouraged activity for those trying to break into the industry). I've been asked on a number of occasions about the tech stack powering the site, so here it is.

### Heroku

For personal projects, I almost always use Heroku, mostly because I don't want to have to worry about manually managing the uptime of all of the processes / databases involved; this is something that I will happily pay Heroku to do for me.

Heroku greatly simplifies my deployment story. I actually have two apps in the same [pipeline](https://devcenter.heroku.com/articles/pipelines) -- one for staging and one for production. Changes pushed to `master` are automatically built and deployed to the staging site, which has its own staging database. Once I am confident that changes are stable, I use Heroku's CLI tool to "promote" that build to the production app, where it is deployed to the main site.

### Flask

Python is slow: we've all heard it before. However, I am extremely comfortable with Python and its ecosystem, so that's what the backend is written in. While it would have been cool to write my backend in Rust (the other language I like using for side projects), I suspect the MVP would have taken far more than a single weekend, and I likely would have lost interest in the project before even making.

In my opinion, pick whatever stack you're most comfortable with and roll with it. I honestly don't think the choice of backend server technology is anywhere close to one of the most important choices when it comes to personal projects -- let's be honest, most side projects will be measuring performance on the order of QPM rather than QPS.

### Postgres

Unsurprisingly, this is where the data for the backend is stored. This includes things like tables containing player info, rank information per player per day, and which players should be associated with which leaderboards. Postgres is my go-to database whenever I need one. I get to use [Postico](https://eggerapps.at/postico/) which is a really nice macOS application, and Heroku has first-class support for hosted Postgres instances.

It might have been cool to experiment with something like [TimescaleDB](https://www.timescale.com), given the fact that the site is essentially a time series graph of people's ranks and also that it's backed by Postgres, but I decided it wasn't worth the extra overhead of figuring out how to deploy and work with it. Vanilla Postgres is virtually always good enough.

### Redis

zeal.gg is simple enough that I probably didn't anything more than Flask & Postgres to back it, but I actually _did_ want to experiment with Redis, as it's a solid piece of technology, and probably has the [cleanest codebase](https://github.com/antirez/redis) out of any C project that I know of. zeal.gg uses Redis to do some simple caching, act as a small state-store across backend API instances, and also to power a job queue (more on that later).


### React

The frontend of the site is built in React, with Chart.js doing the heavy-lifting for drawing the actual graphs. My data visualization skills are nowhere near good enough to have leveraged the power offered by something like D3.

Why React and not something like Angular or Vue? I learned React for the stuff I was working on at Riot at the time, and having a frontend framework under my belt was the sole reason it was possible for me to build a site like this in the first place.


## Technical Decisions & Challenges

There were a few non-trivial things that I had to solve when building the site. Figuring out solutions to these was truly the fun part, and also demonstrates why good design work is so important when it comes to software engineering.


### No User Logins

I knew from the very start that I did _not_ want to support any sort of user logins or anything related; I wasn't about to put myself in the position where I had to start worrying about credentials for a site this simple. The Riot API actually supports a feature where players can "verify" their identity by logging into League and entering a code that is provided by a third-party tool -- I briefly considered somehow making use of this, but quickly decided the complexity was not at all worth it.

As a result, this meant that leaderboards are completely immutable. I had a few people request the ability to, say, add or edit the players contained in a single leaderboard, which isn't possible under this model. I figured that being able to just create a new leaderboard with the updated player set would be good enough, and I still believe this is the case.


### Nice Leaderboard URLs

One feature that I definitely wanted included in zeal.gg was having short URLs for each leaderboard, inspired by link shorteners. While having the leaderboard URLs simply be the concatenation of the player names contained within that leaderboard, this wasn't ideal. The URLs would be very long, and since people can rename their accounts, the same URL would break if a single player decided to change their name. Because the backend tracks players by their account ID, it is able to still recognize a single player across name changes, so having the notion of a mapping between "accounts" and "leaderboards" was definitely the way to go.

For some background, the leaderboard links look like `zeal.gg/BnIS8Hr`. To generate these links, I hash a concatenation of all the player IDs that a given leaderboards comprises. The list is sorted to ensures that different permutations of the same players will be pointed to the same leaderboard, and a connector character is used to join the IDs to prevents situations where a leaderboard with players `AB` & `C` and `A` & `BC` are treated as equivalent.

When a user attempts to create a new leaderboard, I generate the corresponding hash, and take the first 7 characters of its base64 encoding. If this ends up colliding with an existing leaderboard (unlikely but possible), I take more characters of the hash until we reach a unique URL. While this feels a bit hacky and there's probably a better way to do it, it seems to do the job.


### All the World on One Dyno

One caveat with using Heroku is that I wanted to deploy the entire site within a single "project". However, only one dyno within any given project can function as the "web" dyno (which serves HTTP requests), so it was not feasible to spin up the frontend and backend on different dynos: there could only be one.

To solve this problem, I used [nginx](http://nginx.org), which sits at the very front of Heroku. The dyno spins up four nginx workers and four instances of the  API (which compensated for the fact that Flask handles requests synchronously), and directs any requests to `/api/*` to one of them. All other requests are routed to serve the static React frontend that is built during the site deploy.

This comes with another unintended benefit. Another approach could have just been to have the Flask workers themselves serve the static files. However, by siloing off requests to the API and letting nginx serve the frontend, it means that the website remains responsive regardless of how much load is on the API at any given point in time.


### Global Timeout State

In my initial vision for the site, I wanted to refresh everyone's data on a periodic basis, so there would be no need for a manual refresh button on leaderboards. However, the site quickly scaled to a point where I would far exceed my allotted rate limit if I were to do this on anywhere near a regular-enough basis. This was exacerbated by the fact that people would often create a leaderboard to try out the site, and never come back. Would I then be on the hook for refreshing this data? I iterated on solutions to this -- tracking which leaderboards were visited and keeping maintaining a set of "active players", whose data _would_ be refreshed, while letting others rest dormant.

In the end, though, manual refreshes work just fine from a UX perspective, and this is how most League websites operate anyways. The new problem was needing to add a timeout for said refreshes; it would be a waste to allow someone to repeatedly request a leaderboard refresh, since rank data changes on the order of minutes to hours. Since there are multiple instances of the backend running (and requests are distributed across them), simply storing in-memory whether a leaderboard is on its cooldown period won't work.

This is where having Redis around was perfect. The "timeout" of a leaderboard isn't something that I would really want to store within Postgres, but it was perfectly suitable for Redis. The backend writes a value keyed on a leaderboard's unique ID when a refresh is triggered, with the corresponding expiry; upon loading a leaderboard, the existence of that key is checked to determine whether refreshing should be allowed. Redis' native key expiry made this very simple to implement.


### Long-Running Operations

Creating and refreshing a leaderboard can take a while, as the bottleneck is the Riot API. I have leaderboards capped at 12 players, meaning a single request might require as many as 12 different calls to the Riot API. Parallelizing would help a bit, but the response time of an external API isn't something that I wanted bogging down my own API.

To make matters even more worse, since Flask handles requests synchronously, waiting for all external API calls to resolve before completing the request would hog up the backend for much too long, and the performance of the site would be abysmal.

My solution to this was to use a job queue to run these operations in the background. [`RQ`](https://github.com/rq/rq) is a Python library that essentially lets function invocations be queued up as jobs instead of being executed in the current process, and it's backed by Redis.

When a user tries to make a new leaderboard or refresh an existing one, the frontend calls an API endpoint that creates a new "create/refresh leaderboard" job. The API exposes a "job status" endpoint, which gets polled every couple of seconds. When the job has completed, the frontend either redirects the user to the new leaderboard or reloads the page to reflect the refreshed data.

This is simply an implementation detail that is not exposed to the end-user, and I'm particularly proud with how it turned out from a UX perspective. When creating a leaderboard, I draw a loading bar that slowly progresses to give the impression that it's only making a single, long-running request. When refreshing a leaderboard, the refresh icon spins until the job completes and the page reloads.


### Site Announcements

I realized pretty early on that I would need some way of pushing notifications to the site, to alert users in case of an impending maintenance period or to outline new features. However, I didn't want to simply hard-code alerts and have to redeploy the site whenever they changed; I wanted some way of generating them dynamically.

Since I had already created a [subreddit](https://www.reddit.com/r/zealgg/) to discuss changes to the site, I decided to leverage it. I added an endpoint to the backend that uses Reddit's API to check for any posts pinned on the subreddit. The frontend calls that endpoint, and if it finds a pinned post, it displays an alert using the title of the post as the alert text, and links to the full post for futher context.

----

Even though zeal.gg is pretty straightforward at its core, it fills a niche that, to the best of my knowledge, wasn't served by any other of the multitude of League of Legends websites out there. Figuring out that I had the skills to go from _"this would be a cool idea to make for my friends"_ to a site that tens of thousands of League players around the world decided to check out cured my imposter syndrome for a fleeting moment.

At some point, when I feel like it's not worth paying the few dollars a month to host the site anymore, I'll get around to open-sourcing the repository. For now though, I'm keeping the code private, mostly to protect everyone else from laying their eyes upon the monstrosity of the main leaderboard React component.
