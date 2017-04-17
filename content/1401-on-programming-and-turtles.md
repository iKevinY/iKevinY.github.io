Title: On Programming and Turtles
Date: 2014-01-05

Minecraft is one of my favourite games. [Over 13 million][1] copies have been sold for the PC alone -- an impressive statistic considering the game was in alpha merely three years ago. Minecraft's popularity is due primarily to its open-ended nature. The ever-growing variety of blocks appeals to those who enjoy the building aspect of the game, and survival mode only augments the gratification of building by having the player work for their building materials. As for PvP combat, there are numerous community-created custom maps with their own unique rulesets. Expanding on this, through the use of elaborate server-side modding, Minecraft functions more as a game engine than a standalone game, enabling players with unmodded clients to instantly connect to a server and play game modes such as a Minecraft version of the Hunger Games. There is a niche in the game for every type of player.

Added in Minecraft Alpha 1.0.1, Redstone opened up an entirely new world in terms of gameplay. [Redstone Dust][2] carries a Redstone current between various Redstone components while [Redstone Torches][3] function as a [signal inverter][4]. In conjunction with one another, it is possible to construct elementary logic gates, and therefore, fully functional [ALUs][5] and other more complex circuits. This means that Minecraft is Turing-complete, but I digress.

The concept of Redstone captivated me even though I had no experience with anything involving logic gates prior to playing Minecraft. At first, using Redstone involved searching for designs that had the functionality that was required. However, as I became more exposed to it, it became increasingly second nature to build circuits based on their constituent logic gates rather than needing to search for schematics. With this learning process came realizations such as the fact that an XOR gate is what controls circuits where two light switches are linked to a single light bulb, or that an AND gate can be constructed as an OR gate with its inputs and output inverted (which [De Morgan's laws][6] prove). In other words, I learned about logic gates by playing Minecraft -- a peculiar yet satisfying realization. Using boolean logic when programming felt very straightforward despite never having formally learned about it.

My theory of why Redstone was so appealing is that situations arose where building a circuit was necessary in order to overcome a problem in-game. The lack of tangibility of learning boolean logic in a different manner would have probably been discouraging, or at least uninteresting. By learning through Minecraft, it felt substantial, even though in reality, the product being created was only changes made within a video game world. I thought back to this while learning how to program. Most coding examples that novice programmers are supplied with output text to a terminal without producing a tangible product. Many exercises attempt to teach the basics of writing a program, but to someone without much programming experience, it may prove difficult to bridge the cognitive gap between theory and practicality in terms of how lines of code can be applied to real-world scenarios.

For a while, I limited myself to playing vanilla Minecraft, as I felt that playing the game with mods would tarnish my appreciation of the original game. Having followed various [Mindcrackers'][7] [Feed the Beast][8] series on YouTube for quite some time, I finally caved and installed the mod pack. This added an immense -- perhaps even unnecessary -- amount of content to the game. The mod that I was most interested in was [ComputerCraft][9], written by [Daniel Ratcliffe][10], which adds various blocks that can be programmed using [Lua][11]. Among these blocks are [Turtles][12]: robot-like blocks that can be scripted with Lua.

Something that could disincentive learning to programming is that, at least during the learning stages, the only thing produced is pixels on a screen. In other fields, this is not the case. Even amateur artists can produce visually interesting drawings or paintings, and a musician's first composition will probably sound decent, even if it only follows a I-IV-V-I chord progression. On the other hand, programmers who are just beginning to learn their first programming language are typically are greeted with the string `Hello World` being printed in front of themselves. Barring the intrinsic reward of having learnt a new skill, this is fairly lacklustre, and I feel that ComputerCraft solves this in an elegant way. By introducing programming through Turtle scripts, the act of programming is repackaged as a task with a clear goal that can be worked towards. For example, if you notice that you're lacking iron and diamonds, you could write a script that will instruct a Turtle to mine in search of ores. By adding an extrinsic reward, programming in ComputerCraft becomes more gratifying.

The terminology used in ComputerCraft is an obvious allusion to the programming language [Logo][13], which was separated from other programming languages existent at the time by its use of "turtle graphics". The language was largely designed for children and other people new to programming. In fact, its Wikipedia article states that "the design goals of Logo included accessible power and informative error messages" and that "virtual Turtles allowed for immediate visual feedback and debugging". With Turtles, ComputerCraft allows a novice programmer to use kinaesthetic reasoning to debug the actions of a Turtle in a similar manner as Logo was envisioned to do. Given these points, it can be concluded that ComputerCraft very closely follows the design philosophy of Logo, essentially making it a modern version of what Logo was in the past.

----

The first major Turtle program that I wrote was a branch mining script. My goal was to write a program that a swarm of Turtles could execute simultaneously to excavate an area for ores. I tend to be meticulous about following patterns when I mine, and when branch mining, this entails digging tunnels with torches every eight blocks. Here is a very basic Turtle script with this functionality.

```
#!lua
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

The function `miningIteration()` instructs the Turtle to dig the block in front of the Turtle, move forward, and then dig the block above itself. The function is repeated eight times and then the Turtle places a torch. While this is technically a functional mining script, there are a number of improvements that could be made. Here are a few that I implemented into my expanded branch mining script.

[Gravel][14] is, in my opinion at least, the one thing in the game that is more annoying than [Creepers][15], because it often unexpectedly falls while mining which is can at times be startling. Turtles have an interesting behaviour when mining gravel. Consider the manner in which `miningIteration()` has been coded. On first inspection, it may seem that there is no fault in how this would execute: if gravel fell and was obstructing the path of the Turtle, `turtle.forward()` would simply fail and the following iteration would dig, and this would repeat until all the gravel was gone. However, the loop that instructs the Turtle to place a torch after each `miningIteration()` would increment even though the Turtle did not actually move anywhere and the next torch would be placed less than eight blocks away.

There is a simple enough fix. The [Turtle API][16] contains functions that allow a Turtle to detect if there is a block in front of, above, or below itself. An improvement to the Turtle would be to detect if there is a block in front of the Turtle and if so, continue digging in front until it there is no block in front. To deal with overhead gravel, the same approach can be taken but by detecting blocks above the Turtle rather than in front of it. Here is the function rewritten to use these detection functions instead of movement functions.

```
#!lua
function miningIteration()
  while turtle.detect() do turtle.dig() end
  turtle.forward()
  while turtle.detectUp() do turtle.digUp() end
end
```

However, this function is still flawed, though the cause of the problem may not be obvious to someone unfamiliar with Minecraft. Although stationary blocks make up the crux of the game, there is another class of objects known as entities, which includes not only boats and minecarts but also falling sand and gravel. Entities have a position, velocity, and rotation, and are affected by the game's physics. When the game logic detects that there is no stationary block underneath a sand or gravel block, it is converted into an entity and falls until it lands on another solid block (or falls through the [Void][17]).

If a Turtle were to execute the current version of `miningIteration()`, it would quickly become apparent that the Turtle still has problems with gravel. If it encountered a column of gravel above itself, it would move forward during the time that the gravel block above itself is was still falling, leaving a pillar of gravel in the middle of the branch mine. The reason for this is that directly after the Turtle finishes executing `turtle.digUp()`, the gravel block is still falling; therefore, `turtle.detectUp()` returns `false`. This causes the Turtle to continue mining instead of properly stopping to mine the gravel above it. This can be solved by pausing the script for just the right amount of time so that it can detect gravel after it had fallen. This timing turned out to be 0.2 seconds, so adding `sleep(0.2)` after the digging functions forces the Turtle to halt for a brief period of time, mining gravel correctly.

```
#!lua
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

Another interesting behaviour that needed to be debugged was directional-based. Minecraft has many direction-specific quirks due to the way that the game logic was programmed in. This usually results in either south or west sides of blocks being prioritized in some manner. `turtle.placeUp()` instructs a Turtle to place whatever is in the selected block of its inventory above itself. For solid blocks, this is straightforward. However, in the case of non-solid blocks like torches, they will snap to an adjacent block face. The west face is prioritized, followed by the east, north, and south faces successively.

With regards to torch placement, this directional behaviour means that mining in the northwards and southwards direction requires no special treatment. In the remaining two directions, the torch will be placed on the block in front of the Turtle, and in the next iteration of mining, it will get mined along with the block it is attached to. On its own, ComputerCraft does not provide a way for Turtles to automatically determine what direction they are facing (additional mods can add additional types of Turtles to the game). Utilizing ComputerCraft's [GPS API][18] to determine the axis along which a Turtle is travelling would be the only way to add this functionality. As I do not have any GPS infrastructure in my world, I opted to have the Turtle simply prompt the user for the direction that it is facing and store it in the variable `direction`.

```
#!lua
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

In an educational environment, ComputerCraft could be used to create coding assignments for students. An interesting result of this is that all of the students could simply connect to the same LAN world through pit their Turtle scripts against one another in order to determine whose algorithm is the most efficient; after all, friendly competition is always a good motivator. For a younger audience, this would be more engaging than nearly any other approach to teaching programming that I can think of, considering Minecraft's popularity with the younger demographic. Perhaps this style of teaching would be better suited for a club or co-curricular activity rather than a class, since all of its participants would need to have Minecraft accounts. That being said, Minecraft has been used in academic settings to teach subjects from [logic gates to an electronics class][19] to [perspective in art][20]. Organizations such as [MinecraftEdu][21] seek to bring Minecraft into the classroom by offering a discount on bulk sales and also providing a mod to the game that improves the teaching process.

If something unexpected were to happen to a Turtle on a long mining expedition, it could get stuck, and time and resources would need to be spent in order to locate and retrieve it. To avoid this, it would be wise to debug the Turtle's movements in a low-risk environment before actually deploying it on a mining expedition. This might include checking to see how the Turtle would react if a mob wandered in front of the Turtle and obstructed its movement functions, for example. These debugging habits can be applied when the code being written is no longer a Turtle script but rather a more conventional computer program.

Another benefit of learning programming through ComputerCraft is that ideas for new features or added functionality arise simply by using the program. Perhaps the mining script could be extended to instruct the Turtle to automatically return to the start of the branch when its inventory fills up or throw out unwanted materials and only keep ores. Maybe fuel could be a factor, and it could automatically consume any fuel sources that it mines in order to extend the mining expedition. This process of beginning with a basic program and expanding its functionality can be applied when programming independently of ComputerCraft.

I believe that ComputerCraft is a great way to teach people who are already interested in Minecraft the basics of programming. Lua is a very beginner friendly language as, much like Logo, it features a syntax similar to normal English. Turtles will almost certainly more engaging to a novice programmer than a Lua prompt. The mod is not only limited to working with Turtles, either; a more traditional approach can be taken to the programming involved. There are a wide variety of programs that various people have written, from basic APIs to [operating systems with GUIs][22]. In this age of computing, more unorthodox approaches to teaching and learning can be experimented with, and with ComputerCraft, <s>the sky</s> `Y = 255` is the limit.

[1]:  https://minecraft.net/stats
[2]:  http://minecraft.gamepedia.com/Redstone#Redstone_Dust
[3]:  http://minecraft.gamepedia.com/Redstone_Torch
[4]:  http://en.wikipedia.org/wiki/Inverter_(logic_gate)
[5]:  http://en.wikipedia.org/wiki/Arithmetic_logic_unit
[6]:  http://en.wikipedia.org/wiki/De_Morgan%27s_laws)
[7]:  http://www.guudelp.com
[8]:  http://feed-the-beast.com
[9]:  http://www.computercraft.info
[10]: http://www.computercraft.info/dan200/
[11]: http://www.lua.org
[12]: http://computercraft.info/wiki/Turtle
[13]: http://en.wikipedia.org/wiki/Logo_(programming_language)
[14]: http://minecraft.gamepedia.com/Gravel
[15]: http://minecraft.gamepedia.com/Creeper
[16]: http://computercraft.info/wiki/Turtle_(API)
[17]: http://minecraft.gamepedia.com/The_Void
[18]: http://computercraft.info/wiki/Gps_(API)
[19]: http://www.reddit.com/r/Minecraft/comments/1pk6zl/learning_logic_gates_in_electronics_class/
[20]: http://www.reddit.com/r/Minecraft/comments/1dvpnj/today_my_teacher_used_minecraft_to_teach/
[21]: http://minecraftedu.com
[22]: https://github.com/oeed/PearOS
