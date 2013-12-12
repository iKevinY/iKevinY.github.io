Title: On Programming and Turtles
Date: 2013-12-11
Status: draft

Minecraft is one of my favourite games (the other being League of Legends). At the time of writing, [nearly 13 million](https://minecraft.net/stats) PC copies and over 33 million copies across all platforms have been sold -- an impressive statistic considering the game was in alpha merely three years ago. Minecraft's popularity is due mostly to its open-ended nature. The constantly increasing variety of blocks appeal to those who enjoy the building aspect of the game, and survival mode only augments the gratification of building by having the player work for their building materials. As for combat, there are numerous custom maps with their own unique rulesets, enabled by [Command Blocks](http://minecraft.gamepedia.com/Command_Block), that have been created by the community and can be played over multiplayer.

The addition of [Redstone](http://minecraft.gamepedia.com/Redstone) opened up an entirely new world in terms of gameplay. Minecraft Alpha 1.0.1 added [Redstone Dust](http://minecraft.gamepedia.com/Redstone#Redstone_Dust) and [Redstone Torches](http://minecraft.gamepedia.com/Redstone_Torch) to the game; the former carries the current between various Redstone components while the latter functions as a [signal inverter](http://en.wikipedia.org/wiki/Inverter_(logic_gate)). In conjunction with one another, it is possible to construct elementary logic gates, and therefore, fully functional [ALUs](http://en.wikipedia.org/wiki/Arithmetic_logic_unit) and other more complex circuits.

Upon learning about it, the concept of Redstone captivated me; I had no experience with anything involving logic circuits prior to playing Minecraft. At first, using Redstone involved searching up designs that had the functionality that was required. However, as I tinkered around with it more, it became increasingly second nature to build complex circuits based on their constituent logic gates rather than needing to search for circuit schematics. Sometimes, I would need to create a Redstone circuit that fits within the constraints of an existing structure, and this resulted in innovative ways to arrange each piece of circuitry. In other situations, the functionality I needed was very specific and a circuit template would not meet specifications. In other words, I learned about logic gates *by playing Minecraft*. When picking up programming, utilizing boolean logic felt straightforward despite never having formally learned about it.

I think that one of the reasons that Redstone was so appealing was because while playing Minecraft, situations arose where building a Redstone circuit would be the solution to a problem I had in-game. The lack of tangibility of learning about boolean logic in a different manner would have likely been discouraging. By learning through Minecraft instead, it felt substantial, even if the substance was within a video game. I thought back to this while learning how to program. Most of the coding examples that novice programmers are provided with simply output text to a terminal without any tangible product being produced. Many exercises teach how to write a program, but it may be difficult to bridge the cognitive gap between theory and practicality in terms of how lines of code can be applied to real-world scenarios.

## ComputerCraft and Turtles

For a while, I limited myself to playing only vanilla Minecraft, as I felt that playing the game with mods would tarnish my appreciation of the original game. Having followed various [Mindcrackers'](http://www.guudelp.com) [Feed the Beast](http://feed-the-beast.com) series on YouTube for quite some time, I finally caved and installed the expansive mod pack. This added an immense -- perhaps even unnecessary -- amount of content to the game. The mod that I was most interested in was [ComputerCraft](http://www.computercraft.info), written by [Daniel Ratcliffe](http://www.computercraft.info/dan200/), which adds various blocks that can be programmed using [Lua](http://www.lua.org). Among these blocks are [Computers](http://computercraft.info/wiki/Computer), which are interactive terminals, but more interestingly, [Turtles](http://computercraft.info/wiki/Turtle), robots that can be scripted with Lua.

One of the things that could disincentive someone trying to learn how to program is that, at least during the learning stages, the only thing produced is pixels on a screen. In other fields, this is not the case; even the newest artists can produce visually interesting drawings or paintings, and a musician's first composition will probably sound decent, even if it only follows a basic I-IV-V-I chord progression. On the other hand, programmers who are just starting out typically are greeted with the `Hello World` being printed in front of themselves. Barring the intrinsic reward of learning a new skill, this is fairly lacklustre, and I feel that ComputerCraft solves this in an elegant way. By introducing programming through Turtle scripts, programming is repackaged as a task with a clear goal that can be worked towards. For example, if you notice that you're lacking iron and diamonds, you could write a script that will instruct a Turtle to mine in search of ores. This makes programming gratifying by adding an extrinsic reward for writing scripts.

The terminology used in ComputerCraft is an obvious throwback to the programming language [Logo](http://en.wikipedia.org/wiki/Logo_(programming_language)), which featured so called "turtle graphics". The language was largely designed for children and other people new to programming. In fact, the linked Wikipedia article states that "the design goals of Logo included accessible power and informative error messages" and that the "virtual Turtles allowed for immediate visual feedback and debugging". With Turtles, ComputerCraft allows a novice programmer to use kinaesthetic reasoning to debug the actions of a Turtle in a similar manner as Logo was envisioned to do. Given all of these points, I feel that ComputerCraft very closely follows the design philosophy of Logo, essentially making it a modern version of what Logo was back in the 60s and 70s.

## Digging for Ores

The first major program that I wrote for Turtles was a branch mining script. My goal was to write a program that a swarm of Turtles could execute simultaneously to quickly mine an entire area for ores. I tend to be meticulous about following patterns when I mine, and when branch mining, this entails digging tunnels with torches every eight blocks. And yes, although ten-block spacing would prevent mob spawns while being more economic, but I prefer working in powers of two and would gladly trade that for a 20% increase in torch consumption; after all, torches are renewable through wood and charcoal. Here is a very basic way to code a Turtle script with this functionality.

```lua
function miningIteration()
  turtle.dig() -- digs the block in front
  turtle.forward() -- moves forward
  turtle.digUp() -- digs the block above
end

-- Assume external logic controls the value of isMining
while isMining do
  for i = 1, 8 do miningIteration() end -- dig for eight blocks
  turtle.select(16) -- select inventory slot 16 for torches
  turtle.placeUp() -- place torch above the Turtle
end
```

While this is technically a functional mining script, there are a number of improvements that could be made. Here are a few that I implemented into my expanded branch mining script.

The one thing in the game that is more annoying than [Creepers](http://minecraft.gamepedia.com/wiki/Creeper) is, at least in my opinion, [gravel](http://minecraft.gamepedia.com/Gravel), because it often unexpectedly begins to suffocates you. I soon figured out that Turtles have an interesting interaction with gravel. Consider the manner in which `miningIteration()` has been coded. On first inspection, it may seem that there is no fault in how this would execute; `turtle.forward()` would simply fail if gravel fell and was obstructing the path of the Turtle, but the following iteration would mine until all the gravel was gone. However, the loop that instructs the Turtle to place a torch after each `miningIteration()` would increment even though the Turtle did not actually move anywhere and the next torch would be placed less than eight blocks away.

There's a simple enough fix -- just detect if the Turtle is unable to move forward and if so, dig until it can move forward. Following this, continue through the rest of `miningIteration()`. Luckily enough, the [Turtle API](http://computercraft.info/wiki/Turtle_(API)) contains a set of functions that allow a Turtle to detect if there is a block in front of, above, or below itself. Here is the function rewritten to use these detection functions instead of movement functions.

```lua
function miningIteration()
  while turtle.detect() do turtle.dig() end
  turtle.forward()
  while turtle.detectUp() do turtle.digUp() end
end
```

However, this function is still flawed, though the cause of the problem may not be obvious to someone unfamiliar with Minecraft. Though stationary blocks are what make up the core of the game, there is another class of objects known as entities, which includes not only boats and minecarts but also sand and gravel while they are falling. These entities have a position, velocity, and rotation, and are affected by the game's physics. When the game logic detects that the block underneath a stationary sand or gravel block becomes an air block, the stationary block is converted into an entity and begins to fall until it lands on another solid block (or falls through the [Void](http://minecraft.gamepedia.com/The_Void)).

If you were to let a Turtle run the current version of `miningIteration()`, after a while, you would notice that the Turtle still has problems with gravel. When mining, if it encounters a column of gravel above itself, it will move forward during the time that the gravel block is still falling, leaving gravel lying in the middle of the branch mine. Directly after the Turtle had finished executing `turtle.digUp()`, the gravel block was still in mid-fall, and therefore, `turtle.detectUp()` returned `false`. This caused the Turtle to simply continued mining and not stop to mine the gravel above it.

My solution to this was to halt the program for just the right amount of time so that it would detect gravel after it had fallen. This timing turned out to be 0.2 seconds, so adding `sleep(0.2)` directly after `turtle.dig()` and `turtle.digUp()` forces the Turtle to halt for a brief period of time and mine columns of gravel correctly without sacrificing too much efficiency.

```lua
function miningIteration()
  while turtle.detect() do
    turtle.dig()
    sleep(0.2)
  end
  turtle.forward()
  while turtle.detectUp() do
    turtle.digUp()
    sleep(0.2)
  end
end
```

Another interesting behaviour that needed to be debugged was directional-based. Minecraft has many direction-specific quirks due to the way that the game logic was programmed in. This usually results in either south or west sides of blocks being prioritized in some manner. `turtle.placeUp()` instructs a Turtle to place whatever is in the selected block of its inventory above itself. For solid blocks, this is no problem. However, in the case of non-solid blocks like torches, they will snap to an adjacent block face. The west face is prioritized, followed by the east, north, and south faces successively.

In terms of torch placement, this directional behaviour means that mining in the northwards and southwards direction requires no special treatment. In the remaining two directions, the torch will be placed on the block in front of the Turtle, and in the next iteration of mining, it will get mined with the block it is attached to. On its own, ComputerCraft does not provide a way for Turtles to automatically determine what direction they are facing (additional mods can add additional types of Turtles to the game). Utilizing the [GPS API](http://computercraft.info/wiki/Gps_(API)) to determine the axis along which a Turtle is travelling would be the only way to add this functionality, and as I do not yet have GPS infrastructure set up in my world, I opted to have the Turtle simply prompt the user for the direction that it is facing and store it in the variable `direction`.

```lua
while isMining do
  for i = 1, 8 do miningIteration() end
  if direction == 1 or direction == 3 then
    miningIteration() -- complete an extra mining iteration
    turtle.back() -- go back one block and place torch
    turtle.select(16)
    turtle.placeUp()
  else
    turtle.select(16)
    turtle.placeUp()
  end
end
```

With this revision to the mining logic, if the Turtle is facing in one of the two problematic directions, the Turtle will simply complete an extra iteration of mining and then move backwards one block. When `turtle.placeUp()` is called, there is no longer a block in front that that torch could attach to, so it gets placed on either the left or right wall, circumventing the issue of the torch being destroyed in the next iteration of mining.

If something unexpected were to happen to the Turtle on a long mining expedition, it might get stuck underground with its haul of resources and many resources would have to spent (time and materials) to locate and retrieve it. To avoid this, it would be wise to debug the Turtle's movements in a low-risk environment before actually deploying it on a mining expedition. This might include, for example, checking to see how the Turtle would react if a mob wandered in front of the Turtle and obstructed its movement functions. Through this, ComputerCraft teaches error handling and debugging even if it may not be thought of in this manner.

Another benefit of learning programming through ComputerCraft is that ideas for new features or added functionality arise simply by using the program. Perhaps the mining script could be extended to automatically return to the start of the branch when its inventory is full, or the Turtle could automatically throw out junk materials and only keep ores. Maybe fuel could be taken into account, having the Turtle return when low on fuel or automatically consume any fuel sources that it mines in order to keep mine further. This process of taking a basic program and expanding it could be applied to many different types of ComputerCraft scripts, and not just mining scripts.

## ComputerCraft in the Classroom

In an teaching environment, ComputerCraft could be used to create coding assignments for students. An interesting result of this is that all of the students could simply connect to the same LAN world through pit their Turtle scripts against one another in order to determine whose algorithm is the most efficient; after all, friendly competition is always a good motivator. For a younger audience, this would be more engaging than nearly any other approach to teaching programming that I can think of, considering Minecraft's popularity with the younger demographic. Of course, the new problem would be to make sure that they are focused on the programming aspect of the lesson and not the Minecraft-playing. Perhaps this style of teaching would be better suited for a club or co-curricular activity rather than a class, since all of its participants would need to have Minecraft accounts. That being said, Minecraft has already been used in various academic settings, such as teaching [logic gates to an electronics class](http://www.reddit.com/r/Minecraft/comments/1pk6zl/learning_logic_gates_in_electronics_class/) or [perspective in art](http://www.reddit.com/r/Minecraft/comments/1dvpnj/today_my_teacher_used_minecraft_to_teach/).

The mod is not just limited to controlling Turtles; a more traditional approach can be taken to the programming involved. On the [ComputerCraft Forums](http://www.computercraft.info/forums2/), there are numerous examples of various APIs or even [operating systems with GUIs](https://github.com/oeed/PearOS) that have been written for the Computers that the mod adds. I am currently working on a Turtle-based OS, but more on that in a later post.

ComputerCraft is a great way to teach people who are already interested in Minecraft the basics of programming. Lua is a very beginner friendly programming language, as, much like Logo, it features a syntax similar to regular English. Turtles will almost certainly prove to be more engaging to a novice programmer than an interactive Lua prompt. In today's era of technology, unorthodox approaches to teaching can be taken, and with ComputerCraft, <s>the sky</s> `Y = 255` is the limit.
