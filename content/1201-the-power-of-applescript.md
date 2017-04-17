Title: The Power of AppleScript
Date: 2012-11-28

One of my favourite genres of music is video game music. Because of this, it was no surprise that I was ecstatic when OverClocked ReMix announced that ReMixes 1-2500 were available to download via torrent, and that every file contained "complete and consistent ID3 tags". While the tags for most fields are great, I wasn't particularly fond of the format of the track titles. Instead of *TrackName (GameName)* like I would have preferred, the format was *GameName 'TrackName' OC ReMix*. There are a few reasons why I don't like the provided format (namely that the "OC ReMix" suffix feels redundant to me and it feels more appropriate to not see the songs grouped by their source game), but that's besides the point.

Obviously, manually renaming nearly 2500 tracks in iTunes would be a ridiculous undertaking. Luckily, AppleScript happens to be the perfect tool to automate this task. While I had never used AppleScript previous to this, the syntax was easy enough to learn quickly. [Doug's AppleScripts for iTunes](http://dougscripts.com/itunes/) proved itself to be a useful resource for learning (and happens to be where I downloaded other scripts from in the past). It is also where I derived the skeleton of this script from. At first, I attempted to figured out how to handle regular expressions within strings in AppleScript, but I soon realized that a crude piece of code would work just as well; it just wouldn't be useful for any other situation. I set off in search of AppleScript documentation to learn to to manipulate the track name string in the way that I wanted.

The easiest part of the track title to manipulate was removing the *OC ReMix* text at the end of every track. The way I did it was by setting the track name track to itself after removing 9 characters from the end of the string (as it includes the leading space character). With AppleScript, this was very easy to do: `set trackName to text 1 thru -10 of trackName` (`-1` represents the last character in the string, so `-2` would remove the last character, and so on).

After that, to search for the part of the string that contained the song name, I initially tried looking for the first apostrophe in the track title and used the next character as the beginning of the song name string, and ended the string one character before the end of the track title. In most cases, this would (as expected) take the text between the apostrophes -- the song name -- and store it in a dedicated song name string. Great! Fortunately, I tested this script in batches of 10 tracks or so at a time and manually vetted the result, as this definitely did not work. The flaw with this method may already be obvious; if the game name itself contained an apostrophe (for example, Legend of Zelda: Link's Awakening), the script would use all the characters after this apostrophe until the final apostrophe as the song name, which is incorrect.

The fix for this was simple enough. Instead of searching for the first apostrophe within the track title, I searched for the first space followed directly by an apostrophe, and altered the values that affect the length of the strings accordingly.

All in all, the script was certainly not pretty, but it did the job. I didn't notice any incorrectly reformatted names at first glance, but it is possible that a few oddly named songs were incorrectly renamed. I guess my point is that AppleScript was easy enough to work with (given rudimentary knowledge of how other programming languages function) that I was able to hack this very specifically-purposed script together in a short amount of time. Most of the code is based on words in English making it accessible to people who have never programmed before, and the AppleScript Editor gives an alert when saving or running the code if it is invalid.

If you want to use the script to rename to your own tracks (or just to examine my shoddily thrown together code), here is the source code; to use the script, copy it into AppleScript Editor, select the tracks in iTunes, and run it.

```
#!applescript
tell application "iTunes"
	set sel to selection
	if sel is not {} then
		repeat with track in sel
			-- Set trackName variable to name of track (track)
			set trackName to (get name of track)
			-- Strip " OC ReMix" characters from end of track title
			set trackName to text 1 thru -10 of trackName
			-- Find the location in the string where the song name begins (-2)
			set songTitleBegins to (offset of " '" in trackName)
			-- Store name of song in songName string
			set songName to text ((songTitleBegins) + 2) thru -2 of trackName
			-- Find name of game
			set gameTitle to text 1 thru (songTitleBegins - 1) of trackName
			-- Format new track name
			set newTrackName to songName & " " & "(" & gameTitle & ")"
			-- Set name of track to newly formatted track name
			set name of track to newTrackName
		end repeat
	end if
end tell
```
