Title: On Programming and Turtles
Date: 2013-12-17
Status: draft

Minecraft is one of my favourite games. At the time of writing, [over 13 million](https://minecraft.net/stats) copies have been sold for the PC alone -- an impressive statistic considering the game was in alpha merely three years ago. Minecraft's popularity is due primarily to its open-ended nature. The ever-growing variety of blocks appeals to those who enjoy the building aspect of the game, and survival mode only augments the gratification of building by having the player work for their building materials. As for combat, there are numerous community-created custom maps with their own unique rulesets. Expanding on this, through the use of elaborate server-side modding, Minecraft functions more as a game engine than a standalone game, enabling players with unmodded clients to instantly connect to servers and play game modes such as a Minecraft version of the Hunger Games. There is a niche for nearly every type of player.

Added in Minecraft Alpha 1.0.1, Redstone opened up an entirely new world in terms of gameplay. [Redstone Dust](http://minecraft.gamepedia.com/Redstone#Redstone_Dust) carries a Redstone current between various Redstone components while [Redstone Torches](http://minecraft.gamepedia.com/Redstone_Torch) function as a [signal inverter](http://en.wikipedia.org/wiki/Inverter_(logic_gate)). In conjunction with one another, it is possible to construct elementary logic gates, and therefore, fully functional [ALUs](http://en.wikipedia.org/wiki/Arithmetic_logic_unit) and other more complex circuits. This also means that Minecraft is Turing-complete, but I digress.

The concept of Redstone captivated me even though I had no experience with anything involving logic gates prior to playing Minecraft. At first, using Redstone involved searching up designs that had the functionality that was required. However, as I became more exposed to it, it became increasingly second nature to build complex circuits based on their constituent logic gates rather than needing to search for circuit schematics. With this learning process came realizations such as  the fact that an XOR gate is used to control circuits where two light switches are linked to a single light bulb, or that an AND gate can be reduced to an OR gate with its inputs and output inverted ([De Morgan's laws](http://en.wikipedia.org/wiki/De_Morgan%27s_laws)). On occasion, I would need to create a Redstone circuit that could fit within the constraints of an existing structure, and this resulted in innovative arrangements of each piece of circuitry. In other situations, the functionality I needed was very specific and circuit designs found online would not satisfy the requirements. In other words, I learned about logic gates by playing Minecraft -- a peculiar yet satisfying realization to come to. When picking up programming, utilizing boolean logic felt straightforward despite never having formally learned about it.

I think that one of the reasons that Redstone was so appealing was because situations arose where piecing together a circuit was necessary in order to overcome a problem in-game. The lack of tangibility of learning boolean logic in a different manner would have probably been discouraging, or at least uninteresting. By learning through Minecraft, it felt substantial, even though in reality, the product being created was only changes made within a video game world. I thought back to this while learning how to program. Most of the coding examples that novice programmers are to learn from simply output text to a terminal without any tangible product being produced. Many exercises attempt to teach the basics of writing a program, but to someone without much programming experience, it may prove difficult to bridge the cognitive gap between theory and practicality in terms of how lines of code can be applied to real-world scenarios.

For a while, I limited myself to playing only vanilla Minecraft, as I felt that playing the game with mods would tarnish my appreciation of the original game. Having followed various [Mindcrackers'](http://www.guudelp.com) [Feed the Beast](http://feed-the-beast.com) series on YouTube for quite some time, I finally caved and installed the mod pack. This added an immense -- perhaps even unnecessary -- amount of content to the game. The mod that I was most interested in was [ComputerCraft](http://www.computercraft.info), written by [Daniel Ratcliffe](http://www.computercraft.info/dan200/), which adds various blocks that can be programmed using [Lua](http://www.lua.org). Among these blocks are [Computers](http://computercraft.info/wiki/Computer), which are interactive terminals, but (arguably) more interestingly, [Turtles](http://computercraft.info/wiki/Turtle), robots that can be scripted with Lua.

One of the things that could disincentive learning to programming is that, at least during the learning stages, the only thing produced is pixels on a screen. In other fields, this is not the case; even the newest artists can produce visually interesting drawings or paintings, and a musician's first composition will probably sound decent, even if it only follows a rudimentary I-IV-V-I chord progression. On the other hand, programmers who are just beginning to learn their first programming language are typically are greeted with the string `Hello World` being printed in front of themselves. Barring the intrinsic reward of learning a new skill, this is fairly lacklustre, and I feel that ComputerCraft solves this in an elegant way. By introducing programming through Turtle scripts, the act of programming is repackaged as a task with a clear goal that can be worked towards. For example, if you notice that you're lacking iron and diamonds, you could write a script that will instruct a Turtle to mine in search of ores. This makes programming gratifying by adding an extrinsic reward.

The terminology used in ComputerCraft is an obvious allusion to the programming language [Logo](http://en.wikipedia.org/wiki/Logo_(programming_language)), which was separated from other programming languages existent at the time by its use of "turtle graphics". The language was largely designed for children and other people new to programming. In fact, its Wikipedia article states that "the design goals of Logo included accessible power and informative error messages" and that "virtual Turtles allowed for immediate visual feedback and debugging". With Turtles, ComputerCraft allows a novice programmer to use kinaesthetic reasoning to debug the actions of a Turtle in a similar manner as Logo was envisioned to do. Given these points, it can be concluded that ComputerCraft very closely follows the design philosophy of Logo, essentially making it a modern version of what Logo was back in the 60s and 70s.

----

The first major program that I wrote for Turtles was a branch mining script. My goal was to write a program that a swarm of Turtles could execute simultaneously to quickly mine an entire area for ores. I tend to be meticulous about following patterns when I mine, and when branch mining, this entails digging tunnels with torches every eight blocks. Here is a very basic Turtle script with this functionality.

```lua
function miningIteration()
  turtle.dig() -- digs the block in front
  turtle.forward() -- moves forward
  turtle.digUp() -- digs the block above
end

while true do
  for i = 1, 8 do miningIteration() end -- dig for eight blocks
  turtle.select(16) -- select inventory slot 16 for torches
  turtle.placeUp() -- place torch above the Turtle

  -- Assume miningComplete is controlled by external logic
  if miningComplete then break end
end
```

The function `miningIteration()` instructs the Turtle to dig the block in front of the Turtle, move forward a block, and then dig the block above. The function is repeated eight times, and following this, the Turtle will place a torch. While this is technically a functional mining script, there are a number of improvements that could be made. Here are a few that I implemented into my expanded branch mining script.

[Gravel] is, in my opinion at least, the one thing in the game that is more annoying than [Creepers] because it often unexpectedly falls while mining which is can at times be startling. Turtles have an interesting behaviour when mining gravel. Consider the manner in which `miningIteration()` has been coded. On first inspection, it may seem that there is no fault in how this would execute; if gravel fell and was obstructing the path of the Turtle, `turtle.forward()` would simply fail and the following iteration would dig, and this would repeat until all the gravel was gone. However, the loop that instructs the Turtle to place a torch after each `miningIteration()` would increment even though the Turtle did not actually move anywhere and the next torch would be placed less than eight blocks away.

There is a simple enough fix. The [Turtle API](http://computercraft.info/wiki/Turtle_(API)) contains a set of functions that allow a Turtle to detect if there is a block in front of, above, or below itself. An improvement to the Turtle would be to detect if there is a block in front of the Turtle and if so, continue digging in front until it there is no block in front. To deal with overhead gravel, the same approach can be taken but by detecting blocks above the Turtle rather than in front of it. Here is the function rewritten to use these detection functions instead of movement functions.

```lua
function miningIteration()
  while turtle.detect() do turtle.dig() end
  turtle.forward()
  while turtle.detectUp() do turtle.digUp() end
end
```

However, this function is still flawed, though the cause of the problem may not be obvious to someone unfamiliar with Minecraft. Although stationary blocks make up the crux of the game, there is another class of objects known as entities, which includes not only boats and minecarts but also falling sand and gravel. Entities have a position, velocity, and rotation, and are affected by the game's physics. When the game logic detects that there is no stationary block underneath a stationary sand or gravel block has became an air block, it is converted into an entity and begins to fall until it lands on another solid block (or falls through the [Void](http://minecraft.gamepedia.com/The_Void)).

If a Turtle were to execute the current version of `miningIteration()`, after a while, it would become apparent that the Turtle still has problems with gravel. When mining, if it encounters a column of gravel above itself, it will move forward during the time that the gravel block is still falling, leaving gravel lying in the middle of the branch mine. Directly after the Turtle finishes executing `turtle.digUp()`, the gravel block would still be falling, and therefore, `turtle.detectUp()` would return `false`. This would cause the Turtle to simply continue mining instead of stopping to mine the gravel above it.

This can be solved by pausing the script for just the right amount of time so that it would detect gravel after it had fallen. This timing turned out to be 0.2 seconds, so adding `sleep(0.2)` after the digging functions forces the Turtle to halt for a brief period of time, resulting in gravel being mined correctly.

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

In terms of torch placement, this directional behaviour means that mining in the northwards and southwards direction requires no special treatment. In the remaining two directions, the torch will be placed on the block in front of the Turtle, and in the next iteration of mining, it will get mined with the block it is attached to. On its own, ComputerCraft does not provide a way for Turtles to automatically determine what direction they are facing (additional mods can add additional types of Turtles to the game). Utilizing ComputerCraft's [GPS API](http://computercraft.info/wiki/Gps_(API)) to determine the axis along which a Turtle is travelling would be the only way to add this functionality. As I do not have any GPS infrastructure in my world, I opted to have the Turtle simply prompt the user for the direction that it is facing and store it in the variable `direction`.

```lua
while true do
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
  if miningComplete then break end
end
```

With this revision, if the Turtle is facing in one of the two problematic directions, it will simply complete an extra iteration of mining and then move backwards one block. When `turtle.placeUp()` is called, the torch can no longer attach to the block in front (because it has been mined), so it gets placed on either the left or right wall, circumventing the issue of the torch being destroyed in the next iteration of mining.

----

In an educational environment, ComputerCraft could be used to create coding assignments for students. An interesting result of this is that all of the students could simply connect to the same LAN world through pit their Turtle scripts against one another in order to determine whose algorithm is the most efficient; after all, friendly competition is always a good motivator. For a younger audience, this would be more engaging than nearly any other approach to teaching programming that I can think of, considering Minecraft's popularity with the younger demographic. Perhaps this style of teaching would be better suited for a club or co-curricular activity rather than a class, since all of its participants would need to have Minecraft accounts. That being said, Minecraft has already been used in academic settings, from teaching [logic gates to an electronics class](http://www.reddit.com/r/Minecraft/comments/1pk6zl/learning_logic_gates_in_electronics_class/) to [perspective in art](http://www.reddit.com/r/Minecraft/comments/1dvpnj/today_my_teacher_used_minecraft_to_teach/). Organizations such as [MinecraftEdu](http://minecraftedu.com) seek to bring Minecraft into the classroom by offering a discount on bulk sales and also providing a mod to the game that streamlines the teaching process.

If something unexpected were to happen to a Turtle on a long mining expedition, it could get stuck somewhere and time and resources would need to be spent in order to locate and retrieve it. To avoid this, it would be wise to debug the Turtle's movements in a low-risk environment before actually deploying it on a mining expedition. This might include, for example, checking to see how the Turtle would react if a mob wandered in front of the Turtle and obstructed its movement functions. These habits can be applied when the code being written is no longer a Turtle script but rather a more traditional program.

Another benefit of learning programming through ComputerCraft is that ideas for new features or added functionality arise simply by using the program. Perhaps the mining script discussed could be extended to automatically return to the start of the branch when its inventory is full, or the Turtle could automatically throw out junk materials and only keep ores. Maybe fuel could be a factor, and it could automatically consume any fuel sources that it mines in order to extend the mining expedition. This process of beginning with a basic program and expanding its functionality can be applied to programming independent of ComputerCraft.

In conclusion, I believe that ComputerCraft is a great way to teach people who are already interested in Minecraft the basics of programming. Lua is a very beginner friendly language as, much like Logo, it features a syntax similar to regular English. Turtles will almost certainly more engaging to a novice programmer than a Lua prompt. The mod is not only limited to working with Turtles, either; a more traditional approach can be taken to the programming involved. There are a wide variety of programs that various people have written, from basic APIs to [operating systems with GUIs](https://github.com/oeed/PearOS). In this age of computing, more unorthodox approaches to teaching and learning can and should be experimented with, and with ComputerCraft, <s>the sky</s> `Y = 255` is the limit.
