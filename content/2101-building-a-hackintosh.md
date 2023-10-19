Title: Building a Hackintosh
Date: 2021-01-23

2020 was an exciting year for Mac users because Apple finally released computers powered by their own custom silicon. Despite this, for some reason, it was the year that I finally caved and decided to build a Hackintosh. For about 7 years, I only ever owned laptops, and the 15" MacBook Pro was what I used as a "desktop substitute". I liked the idea of using a portable as my primary machine, as it meant that whether I was at home, at school, or traveling, I would have access to all of my files. In addition, the most intensive activities that I used my computer for were compiling code and playing League — both workloads that MacBook Pro can easily handle.

However, when Riot released VALORANT, that was the first PC game that pushed the performance of the machine. To Riot's credit, the game is impressively well-optimized for lower-spec devices, and I was used to playing on minimal graphical settings from my Team Fortress 2 days (loading custom ultra-low spec configs to gain every last frame), but once I started streaming gameplay for archival purposes, that really started to push the limits of the laptop.

Perhaps the straw that finally broke the camel's back is that one day I noticed that my laptop kind of… rocked back and forth on a flat surface, and it turns out that was because the battery was starting to bulge. Feeling guilty that this was probably a result of me stressing it whilst in clamshell mode for several hours at a time, I decided it was time to build a real desktop PC to play the games that I wanted to play. Since one of my other friends who feels equally strongly about macOS built a dual-booting Hackintosh earlier this year without much trouble (allegedly), I was convinced. Also, Apple's move to ditch Intel and move to native silicon suggests that macOS compatibility will only become worse as time goes on, meaning I might as well get in on the action now.


## Onto the Build

In terms of hardware, I decided to choose a part list nearly identical to [another one](https://infinitediaries.net/my-2020-hackintosh-hardware-spec/) that I found online that reportedly had good compatibility with macOS. My only non-negotiable was having Thunderbolt 3 support; without it, running my UltraWide monitor at native resolution would be a huge hassle. As nice as it would have been use an AMD CPU or an NVIDIA GPU, the benefits did not outweigh the lack of easy compatibility in my mind, so an i9-9900K and the RX 5700 XT was the best I could do. Since every build needs a spec list, here we go:

* *Motherboard*: Gigabyte Z390 Aorus Ultra
* *CPU*: Intel Core i9-9900K
* *GPU*: Gigabyte Aorus Radeon RX 5700 XT
* *RAM*: 4×16GB 3600MHz DDR4 HyperX Fury
* *Storage*: Samsung 970 EVO 2TB (macOS), 500GB (Windows)
* *Case*: Fractal Design Meshify C
* *PSU*: Seasonic Prime 850 Titanium
* *TB3 Card*: Gigabyte Titan Ridge 2.0
* *CPU Cooler*: Noctua NH-D15
* *Case Fans*: 3× Noctua NF-A14, 1× Noctua NF-S12A

Building a PC feels like a rite of passage of sorts for the types of people who spend the majority of their waking hours using a computer, so I was very excited to finally get to partake in it. Having not ever built a computer before, I prepared by watching far too many build videos (primarily from Vancouver-based [Linus Tech Tips](https://www.youtube.com/user/LinusTechTips)).

The build itself went fairly smoothly, with the exception of the fact that the Noctua CPU cooler I went with is so incredibly massive that once it's installed, it's very tough to access a lot of other parts of the motherboard, including the PCIe release tab. This was an issue when I first booted the system and the GPU fan was spinning at 100% and I thought I might have had a faulty card, but somehow after installing some drivers on the Windows side, it thankfully fixed itself.

Rather miraculously, Thunderbolt worked without having to do anything special, and was able to drive my monitor at full resolution. For some reason, though, USB doesn't work over Thunderbolt, and I figure it has something to do with the USB cable connected to the Titan Ridge card. However, I didn't want to fiddle with the internal cabling anymore, so I decided to just connect all my peripherals over USB like normal.

I couldn't get OpenCore (the macOS bootloader) to work the first few times I tried, despite my friend telling me nothing special was required other than "following [the guide](https://dortania.github.io/OpenCore-Install-Guide/)", so I gave up on it for a couple weeks, as I was mostly focused on preparing for [Clash tournaments](https://na.leagueoflegends.com/en-us/news/game-updates/worlds-2020-clash-details/) in League, which Windows was perfectly capable of running.

After reading through the guide more carefully, it turns out I had everything right except for missing a boot argument that was required for Navi GPUs (which the RX 5700 XT is). Making that fix allowed macOS to install, and to my delight, basically everything worked perfectly out of the box, including things like iMessage and iCloud — even native Screen Sharing — which apparently takes extra fiddling for some people's builds.

My delight quickly turned into panic when I tried booting back into Windows, though, and found that choosing that boot option from the BIOS would just infinitely loop me back to the BIOS. This was compounded by the fact that I was doing this on a Friday evening, and was due to play in the next round of Clash tournaments the next day, and while I _could_ have played on macOS, I had grown used to my Windows setup for League.

After half an hour of frantic Googling, I was pretty confident that the OpenCore installation process had somehow destroyed Windows' EFI bootloader, and that was why I was hitting a boot loop. I took the USB drive that I had stuck OpenCore on and reformatted it with a fresh copy of the Windows 10 installation media, which was funny because that drive _already had_ Windows 10 on it before I replaced _that_ with OpenCore (I only had one USB drive in my apartment). After booting from the installation media, I was able to restore things back to normal.


## My Debugging Experiences

This is the part of the blog post where I describe the problems I ran into, and hope that Google picks up on keywords so that other people can find the fixes.


### Unable to boot Windows after installing macOS

This was the issue that I talked about a bit earlier, where after successfully booting macOS for the first time, I was unable to actually boot back into Windows. I think what caused this was me deleting the `MICROSOFT` folder from the EFI, though I can't remember if I actually did this, or if it was a side effect of the installation process. Either way, it wasn't present, and I needed to boot from Windows installation media to properly reinstate the boot info.

[This Reddit post](https://www.reddit.com/r/hackintosh/comments/hn3gwr/accidentally_deleted_microsoft_folder_from_efi/) is what I referenced, which boils down to entering Command Prompt from the installation media and using `diskpart` to find the system and Windows partitions, then running `bcdboot` against the system partition to set up the boot files properly.


### Clamped Audio in macOS

This one was a bit weirder; when I thought everything was working properly, I noticed that I couldn't raise the volume past ~5 "ticks" of the macOS volume picker; any louder and the meter would go up, but the volume would stay the same. In addition, when watching YouTube, louder moments would create a sort of "audio rubberbanding" where the volume would adjust itself below this imaginary threshold, but at slightly different times in each audio channel, making it very annoying.

The solution to this ended up being a bad layout ID, and the OpenCore post-install guide actually [explains how to solve this](https://dortania.github.io/OpenCore-Post-Install/universal/audio.html#finding-your-layout-id). However, their proposal to try all valid layout IDs for your audio codec was off-putting, since that would've meant trial-and-erroring over 10 different options, so I put off making this fix initially. However, another Reddit thread suggested just trying layout 7 (ie. adding `alcid=7` as one of the `boot-args`), and it turns out that did the trick.


### Mounting macOS EFI partition from Windows

Later on, I was attempting to mess with my OpenCore configuration to get OpenCanopy working for a more visually appealing boot screen, but OpenCore wasn't happy with the new configuration and fatal error'd immediately when trying to start up, meaning it was impossible to boot macOS at all.

Fortunately, it's still possible to boot directly into Windows from the BIOS' boot selector, and then from Windows you can mount macOS' EFI partition and undo bad configuration changes from Windows. I followed the instructions on [this page](https://manjaro.site/how-to-mount-macos-efi-partition-from-windows-10/) to do so: essentially, using `diskpart` to find and mount the Hackintosh disk and then the EFI partition, then doing normal Windows file operations to restore the configuration files back to a bootable state.


### Cursed Audio Crash

The one rather severe issue that I started to notice a couple of months in was that sometimes when attempting to stream Advent of Code, my computer would lock up, but not in the way that I'm used to. The screen would freeze, and audio that was playing began to stutter slightly before completely cutting out. However, the OS would never fully get to a kernel panic, so a hard power cycle was the only way to recover. Rather obnoxiously, this happened very infrequently (only twice out of the 25 days that I streamed Advent of Code), so it was difficult to root cause or debug. In addition, since it never actually panicked, there wasn't any useful information in Console.app to make heads or tails of.

There were a couple of clues that helped narrow down the cause; namely, the fact that the freeze only seemed to happen while I had Twitch Studio (the broadcasting software I use on macOS) open suggested it was somehow related to a more intensive system process, and the strange audio behaviour made me suggest that the audio stack was to blame.

After some searching, I stumbled upon [this Reddit post](https://www.reddit.com/r/hackintosh/comments/dmn84u/rx_vega_64_freezes_system_during_hw_accel_encode/) in which someone with an RX Vega 64 (a similar graphics card to my own) had system freezes when performing hardware-accelerated audio encoding. They recommended running a `log` command to stream kernel-related logs to a file, such that when the crash occurred, it would dump the logs before the system failed, meaning information would be captured even though no kernel panic was actually produced.

Fortunately, the crash _did_ happen during a day where I happened to remember to run the command at startup, and much like the discussion that went on in the comments of that Reddit post, the logs right before the crash seemed to be audio-related, and `AppleGFXHDA.kext` was the culprit. I disabled the extension by renaming it (which meant I had to first disable SIP, something I didn't initially intend to do on my Hackintosh), and I haven't witnessed the crash since, so I'm guessing that solved it.

----

All in all, building a Hackintosh was a really fun experience, and I realized just how sheltered I was from the whole world of "how modern PCs really work". I always just nodded my head and pretended to understand when people at work or friends would talk about their _BIOS_ and stuff like that, but now I can at least sort of join in on those discussions. Of course, now I'm a bit sad that I won't be able to justify buying an M1 Mac anytime soon.
