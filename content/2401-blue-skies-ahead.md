Title: Blue Skies Ahead
Date: 2024-12-27

I joined Twitter in December of 2008, making me 12 years old at the time. Funnily enough, the fact that I signed up before turning 13 caused issues nearly a decade later, when my account got locked due to some automated process flagging me as an *under-13-year-old* per [COPPA](https://en.wikipedia.org/wiki/Children%27s_Online_Privacy_Protection_Act), and some manual intervention was needed to unlock my account. It also means that I've been on Twitter for more than half of my life — a wild realization.

For over a decade, Twitter was the way that I kept up with current events, my hobbies, career trends, and more. On top of this, bot accounts were actually a force for good, doing public services like tweeting the day's [xkcd](https://xkcd.com/).

Sadly, and this goes without saying, Twitter has fallen off a cliff ever since its takeover. While writing this post, I opened the app to do a quick survey, and these were the first fifteen things on my timeline:

- 1 tweet from someone I actually follow
- 5 "normal" tweets from accounts I don't follow
- 5 garbage tweets from low-quality aggregator accounts
- 4 (!) advertisements

Admittedly, this is a biased sample since most people I follow have already abandoned the site. I guess this algorithmic muck is what other platforms have devolved into anyways, but since I used Twitter back when the timeline was exclusively reverse-chronological and people wrote `QT:` to quote-tweet, it's appalling to me that this is what it's become.

One of my friends gave me an invite code to Bluesky back in 2023, so I made an account to reserve my handle. Nobody really seemed to be using the site at the time, though, so I didn't bother exploring it any further. At the time, I was still twiddling my thumbs, waiting for Mastodon to finally take off.

Fast forward to this November: I noticed a bunch of communities that I follow starting to migrate to Bluesky. I used [Sky Follower Bridge](https://github.com/kawamataryo/sky-follower-bridge) to help rebuild my network, and magically, my timeline became reminiscent of my Twitter timeline of the past, albeit with a bit less activity (though this picked up as the weeks went on).

I've been happy that microblogging is something I'm doing again, and wanted to write about things that I think are cool and refreshing about the platform.

## A Friendlier Algorithm

Much like [John Siracusa](https://hypercritical.co/about/), I'm a timeline completionist. My brain treats the timeline the same obsessive way it treats my email inbox: I skim every single post written by everyone I follow. Yes, this means that when waking up in the morning, I pick up where I left off before bed, working my way *back up my timeline* to the most recent post. In this sense, I never treated Twitter as an "infinite feed of content" — once I caught back up with all the tweets I missed, I was done. Sadly, algorithmic feeds makes this usage pattern impossible, since posts are delivered in whatever order the *Big Matrix o' Numbers* thinks will maximize engagement.

For this reason, I exclusively used third-party clients like [Tweetbot](https://tapbots.com/tweetbot/) since, due to not needing to push views on promoted posts or serve ads, posts *are* delivered in reverse-chronological order. For nearly a decade, this is how I interacted with Twitter, until they [killed third-party access](https://www.theverge.com/2023/1/13/23553161/third-party-twitter-clients-apps-outage-twitterific-tweetbot) to the platform. Being forced to use the native client in its ad-ridden, algorithm-tainted form was just not worth it for me anymore, and so my Twitter habit evaporated.

To be fair, algorithmic content isn't inherently a bad thing. I'm a loyal Spotify user primarily because their curated playlists actually understand my eclectic taste in music (that I can't even define myself), allowing me to actually discover new music and artists. YouTube's algorithm is pretty good at helping me find new educational channels and quality video essays (as long as I intentionally stay away from YouTube Shorts).

Much to my delight, Bluesky has implemented content discovery in a very tasteful manner via [custom feeds](https://bsky.social/about/blog/7-27-2023-custom-feeds). These are effectively bite-sized "algorithms" that anyone can create. The core team themselves have built feeds such as [Quiet Posters](https://bsky.app/profile/did:plc:vpkhqolt662uhesyj6nxm7ys/feed/infreq), which signal boosts posts from people *you* follow that post infrequently. You can opt-in to have feed posts interleaved into your timeline, but the site doesn't force this upon you. I feel they've struck a nice balance between helping me discover new people & content without feeling like it's compromising my actual timeline.

## Open Software Attracts Cool Builders

Bluesky is built on top of the [AT Protocol](https://atproto.com/), which originally began as a research project within Twitter to investigate how the platform could be decentralized. As a developer, anything open-source like this is delightful — if I'm ever wondering how something works behind the scenes, it means there's an option to go spelunking into some specs or codebases to figure out what's really going on.

For example, someone on the dev team stated that even if you changed your handle, posts that linked to the old handle would "link" to the new account, even though the actual text in the post wouldn't change. Being curious how this works, I used [PDSls](https://pdsls.dev/) (a cool open-source tool) to look at the [metadata of a past post](https://pdsls.dev/at/did:plc:kewhcp362af66czceva4dhrl/app.bsky.feed.post/3lbzaygywv22x), and found a [`richtext.facet` type](https://docs.bsky.app/docs/advanced-guides/post-richtext#rich-text-facets) containing the DID (the unique identifier for ATProto blobs) of my profile. Using this, the frontend client can link out to the DID version of profile links, ensuring that old posts will always point to the correct account.

Building on top of these facets, [deck.blue](http://deck.bluehttps://deck.blue/) — a third-party client aiming to replicate [TweetDeck](https://www.wired.com/2012/03/hands-on-tweetdeck-wants-to-be-your-pro-twitter-client-again/) — lets you write Markdown-style inline links as a feature, using the same facets under the hood. I think this is particularly neat because it's a feature that's directly supported by the protocol, and it seems so obvious to implement and useful (given the character limit) that I'm sure the native app will eventually follow suit.

Speaking of third-party clients, [SkyBridge](https://github.com/videah/SkyBridge) bridges ATProto and [ActivityPub](https://activitypub.rocks/), which allows apps written for Mastodon like [Ivory](https://tapbots.com/ivory/) (Tweetbot's successor) to work with Bluesky, and it's surprisingly seamless. I'm hoping this means it's not too much work for Tapbots to fork Ivory and build a Bluesky-compatible app, as there's so many small features that I'm sorely missing from those apps, like draft posts, saved timeline position across devices, and custom gestures.

The openness of ATProto lends itself nicely to people building small things around the ecosystem, such as Emily Liu (a Bluesky dev) figuring out a way to [use Bluesky posts as blog comments](https://emilyliu.me/blog/comments). Cory Zue [extended her code](https://www.coryzue.com/writing/bluesky-comments/) to support Jekyll, and I liked the idea so much that I added it here. I've been wanting to add a lightweight comment system to my blog for a while but kept putting it off, and this fits the bill perfectly. If everything went right, there should be a comment section at the bottom of this post!

## Onwards and Upwards

By no means am I claiming Bluesky is the perfect microblogging platform. Already in the past week or so, I've noticed an uptick in the ever-obnoxious crypto and spam-bot accounts that made the Twitter notifications tab worthless. The Bluesky moderation team is going to be stretched thin as the platform becomes more widely adopted, and there are many other problems that need to be solved as networks like this scale.

One area where private, centralized platforms have a distinct advantage over decentralized ones is the ability to serve functionality like private accounts. Since all data on Bluesky is relayed between [PDSs](https://docs.bsky.app/docs/advanced-guides/federation-architecture#personal-data-server-pds), building an equivalent is going to be challenging. Maybe there's a clever way to "virtualize" private accounts by encrypting posts and requiring readers to call out to a centralized service (like how [Bluesky DMs](https://bsky.social/about/blog/05-22-2024-direct-messages) are implemented) for authorization before decrypted content is served, but I'll leave this for smart protocol devs to grapple with.

Compared to Mastodon (which suffers from being an "engineer's solution" to the foibles of Twitter), Bluesky feels like the perfect balance between extensibility and usability. I'm enjoying the site a lot at the moment — it feels fun and whimsical, with people posting a lot and actually interacting with each other, much like the early days of Twitter. I'm optimistic that Bluesky will [adhere to its ideals](https://www.wired.com/story/bluesky-ceo-jay-graber-wont-enshittify-ads/) with Jay Graber as CEO, and I'm looking forward to seeing all the neat things the community continues to build on top of it.