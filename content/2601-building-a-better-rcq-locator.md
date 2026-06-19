Title: Building a Better RCQ Locator
Date: 2026-06-19
Summary: I built a website for finding Regional Championship Qualifiers for Magic: The Gathering that you can check out at https://surveil.land.
Bluesky: https://bsky.app/profile/kevinyap.ca/post/3monwf77f4k2q

!!! note ""
    **TLDR**: I built a website for finding Regional Championship Qualifiers for Magic: The Gathering that you can check out at [**surveil.land**](https://surveil.land/).

Over the last few years, I've gotten into Magic: The Gathering. While there are many different ways to play Magic, from being a collector to showing up to Commander nights play with new people, what I primarily get out of Magic is scratching the competitive itch that I used to satisfy through a truly mind-numbing amount of hours playing League of Legends trying to climb that ranked ladder (which, incidentally, [led to the side project](https://kevinyap.ca/2020/03/architecting-zeal-gg/) that has been sitting at the bottom of my resume ever since).

The dream of every competitive Magic player is to make it onto the [Pro Tour](https://magic.gg/pro-tour), an international, invite-only tournament that happens approximately three times per year in different locations around the world. It's a 3-day event that tests its invitees' skill to the max by having them play in dozens of rounds of both of Magic's primary 60-card formats: Constructed and Limited.

The primary way to qualify for the Pro Tour (other than already being on the tour and getting a good enough result to justify staying on the tour) is by getting a top placement at a Regional Championship, or "RC", which are held once or twice per "season" in each country or region. This is *also* an invite-only tournament that you must qualify for by playing in *Regional Championship Qualifiers* that are held at the local level at "LGSes" (local game stores), the same shops that sell cards and host more casual weekly events.

Alas, while I was fortunate enough to qualify for the [Canadian RC](https://magic.gg/news/f2f-tour-championship-calgary-november-2025-final-standings) last year in the first season I decided to take competing seriously, I ended Day 1 with a 4-4-1 record and didn't make the cut for Day 2 (which requires 6 wins out of 9 matches). This year, I'm back on the grind again.

One of the frustrating parts of this system is earning your qualification to the RC in the first place. By its very nature, there is some inherent variance in every game of Magic: The Gathering; even amongst top players, the better player is not going to win 100% of their games -- sometimes they'll get unlucky with their card draws (this isn't even taking into account the possibilities for misplays or not seeing certain winning lines 7+ hours into a grueling tournament day). Then there's the concept of the "event metagame": the deck that you chose to bring to the event will have good and bad matchups into other decks, and it's entirely possible that by the graces of the tournament pairing software, you luck into all of your good or all of your bad matchups on any given day.

Each event only hands out invites to the top 1 to 4 players, depending on the region and the attendance count, so it's truly a numbers game. As a result, qualifying tends to require attending multiple RCQs until you get the right alignment of a) having the proper preparation, b) playing well on the day, and c) getting somewhat fortunate with your matchups.

---

To their credit, Wizards of the Coast (the company that runs Magic: The Gathering) has an [event locator app](https://locator.wizards.com/) that lets you punch in your address and receive a list of of nearby events. You can then filter by format, event type, etc. This is a great tool for, say, if you move to a new city or are visiting and want to look up what LGSes are near you and what days they hold Commander nights or other weeklies on. This is a nice service, but there are a couple of problems with it when it comes to finding RCQs.

Firstly, the maximum distance you can search is a radius of 100 miles (160 km). Living in Toronto, I'm fortunate enough that there's a wealth of stores close to me that all host RCQs, but people who live in sparser geographical regions like the US will often drive hours to stores in other cities to attend these events, and a 100 mile search isn't big enough to catch all potential destinations.

Secondly, and this is mostly personal commentary: it's a little bloated to use if all you care about is having access to a list of upcoming RCQs near you. The set of data doesn't really change all that much, especially if you only care about RCQs which are scheduled weeks to months out in advance, so a simpler and more straightforward site would do the trick just as well.

A couple of years ago, a website called Spicerack.gg popped up that solved all of these issues, for me at least. It searched through the same dataset of events that Wizards' locator site did, with similar filters for format and event type, but presented the list of events in a much cleaner way. Of relevance to this topic, it also had a quick "Drivable RCQs" shortcut at the top which would automatically configure the set of filters to RCQs only (perhaps most importantly) a very large search radius -- larger than 100 miles. I referenced this site *a lot* last year to find RCQs at stores that I didn't frequent to give myself the best chance of qualification.

The reason I didn't hyperlink it is because approximately a month ago, Spicerack shut down unexpectedly. The circumstances around the shutdown are still a bit unclear to me, but the gist of it is that on top of having an event locator, Spicerack was also trying to expand into being a tournament organization platform too, where stores could sign up to run events, sell entries, and manage attendees and decklists on the day of. This part of the site was seemingly strongly coupled to the (unrelated) event locator part of the site, and when the decision was made to shut down the former, the latter came down with it. (More context can be found by searching through Reddit/Twitter.)

I grumbled to myself about this for a while and went back to using Wizards' event locator to catalog which RCQs I should attend for a couple weeks, all the while thinking to myself that it would be pretty straightforward to replicate Spicerack's approach (but not actioning on it out of laziness). It wasn't until having a back and forth with another software developer in one of the MTG Discord servers I'm a part of that I had the motivation to just go ahead and build the darn thing.

---

In another bout of "domain name driven development" (wherein I think of a great domain name that isn't taken, register it, *then* actually work on a project), I realized that `.land` was a valid TLD and thought of registering `fetch.land`, a reference to a very iconic cycle of cards known as [fetchlands](https://mtg.wiki/page/Fetch_land) (because they "fetch" other lands from your deck). That, of course, was already taken, and so I went down the list of other land cycles until landing (no pun intended) on `surveil.land`, a nice name as it references the [surveil lands](https://mtg.wiki/page/Scry_land#Surveil_lands) and nice because it also evokes some imagery of monitoring or finding events. (I didn't want to go with `scry.land` because it was a little too close to [Scryfall](https://scryfall.com/), the most valuable Magic resource on the web.)

Some thoughts I had in mind while building it:

As I mentioned earlier, the list of events is virtually static, especially when only considering things like RCQs. At the time of writing, there are 1260 RCQs returned by the event locator and that's *worldwide*, not just in North America or something like that. This means that, realistically, an RCQ locator doesn't *truly* need a backend server at all; you could just serve a single static page with every known RCQ embedded in the payload and let frontend JS do any nice filtering and other presentation of the data.

The lower the maintenance overhead of a project is (both in terms of time and money), the more confident I can be about it not becoming vaporware. In this new era of LLM-driven development, there are orders of magnitudes more hobby projects appearing, but I anticipate they will just as quickly rot and disappear once tech debt and/or hosting fees begin to rack up. I take a lot of pride in developing long-lasting projects ([zeal.gg](https://zeal.gg/) has been up and running for almost a decade now).

I wanted it to be as simple and easy-to-use as possible for finding RCQs, à la the "Drivable RCQs" shortcut that Spicerack had. While whatever infrastructure supports serving only RCQs could easily serve all the events that are in Wizards' event locator, I figured people who are interested in non-competitive events can use their site directly (I'm not trying to completely invalidate its existence).

Any good side project also affords the opportunity to play around with new technology, and since I wrote zeal.gg, lots of things have changed. The above constraints led me to building on top of Cloudflare's infrastructure because I hadn't tried out Cloudflare Pages, Workers, or R2 before.

The idea behind it was for the frontend to just be a single static page. This page would read in JSON blobs from R2 buckets that contained all the event information. These blobs would be periodically updated by some workers that would poll the event locator API to see if any new events needed to be added to the payload (or removed since they had happened in the past). This also makes it trivial to support an arbitrarily large search radius, since every result is available to the client and just needs to be filtered.

I also decided to get a bit fancy and chop up the globe into different "tiles" keyed by latitude/longitude. Then, based on the location and radius that the user inputs, the frontend will request the "correct" JSON blobs that span the search region: in the best case, only a single file (because the entire area is encompassed by a single tile), and in the worst case, four files (if the center of the circle is near the vertex where 4 tiles meet). This is overkill for a couple thousand events, which could comfortably fit in a single JSON file, but this design adds some flexibility in case the number of events shoots up dramatically, if for example new regions are added, Wizards decides to run more RCQs, or I decide to index more types of events in the future.

---

Anyways, the site is live now at [**surveil.land**](https://surveil.land/). It remembers your last-inputted location and filters so it's a zero-click experience on repeat visits. The event blobs are aggressively cached so the longest you ever have to wait is the first time the events in your region is loaded into memory. Even when nothing is cached, it's generally a sub-second load (the longest delay is waiting for the location lookup to resolve to a latitude/longitude pair). It also has some nice-to-have features like "Add to Home Screen" on mobile, a lightweight starring feature, and being able to quickly create Apple/Google Calendar events.

Hopefully my fellow RCQ grinders and Pro Tour aspirants find it useful!
