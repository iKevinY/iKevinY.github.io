Title: Sandbox
Latex:

This page is a sandbox page for testing how the Markdown engine will render certain elements.

# First Paragraph
Cupcake ipsum dolor sit amet applicake. Chocolate pudding caramels tootsie roll dragee cake wafer brownie halvah. Oat cake sesame snaps donut tootsie roll. Candy sugar plum biscuit. Donut chocolate cake icing marshmallow sweet chupa chups. Icing jelly pastry chocolate bar sweet roll souffle gummi bears applicake brownie. Donut muffin icing cookie applicake. Powder cotton candy croissant toffee topping.

## Second Paragraph
Lollipop pudding bear claw tootsie roll danish sweet. Caramels tootsie roll wafer toffee cupcake toffee gingerbread pudding carrot cake. Donut pastry carrot cake halvah croissant. Gingerbread chocolate tiramisu liquorice sesame snaps macaroon. Liquorice brownie candy canes. Icing tiramisu gummi bears. Carrot cake wafer pastry jelly beans tart dessert chocolate bar souffle souffle. Oat cake marshmallow jelly beans caramels. Gummies brownie brownie bear claw biscuit bear claw marzipan. Fruitcake lollipop pastry gingerbread gummies pastry.

### Third Paragraph
Pudding donut bonbon sweet jelly sesame snaps croissant. Bonbon applicake donut muffin cupcake brownie souffle. Chocolate bar jelly wafer chocolate cake chocolate cake. Brownie apple pie lemon drops dragee. Muffin dragee marzipan. Dragee pastry sweet roll chocolate cake lollipop pudding macaroon oat cake. Bear claw cotton candy dessert chupa chups pudding macaroon applicake fruitcake. Fruitcake danish pastry halvah chocolate cake.

> This quote is quite nice.
> <cite>Kevin Yap</cite>

## Code

The following is `inline code`.

```lua
for index, word in ipairs(wordTable) do
  if word == [[\n]] then -- checks if the "word" is a newline character
    n = n + 1
    lineTable[n] = ""
    n = n + 1
    lineTable[n] = ""
  -- Checks to see if adding the next word (first element of wordTable) will fit within the terminal
  elseif string.len(lineTable[n]) + string.len(tostring(word)) + 1 <= lineSpacing then
    if lineTable[n] ~= "" then
      lineTable[n] = lineTable[n] .. " " .. word
    else -- if the word would be the first of the string, don't add a leading space to the line (because it would be incorrect)
      lineTable[n] = tostring(word)
    end
  -- Otherwise make a new line and add the word to it
  else
    n = n + 1 -- move to next line in lineTable
    lineTable[n] = tostring(word)
  end
end
```

```
This time we have a code block with no syntax highlighting.
It spans a couple of lines.
```

## Unordered Lists

* List item
* List item

## Ordered Lists

1. Ordered lists
2. Have numbers

## Tables

<table>
<tr> <td></td> <td>Hunt</td> <td>Slack</td> </tr>
<tr> <td style="font-weight:bold">Hunt</td> <td>0</td> <td>-3</td> </tr>
<tr> <td style="font-weight:bold">Slack</td> <td>+1</td> <td>-2</td> </tr>
</table>

## LaTeX

An important aspect of the challenge to keep in account is the `m` variable, which is set to a random integer value every round such that $0 &#8804; m &#8804; P(P-1)$. Assuming that this value is truly random, in order to calculate this value, I wrote code to track the average cooperation value of the tribe over time to determine the probability that `m` would be met for any given round. As the graph $y = P(P-1)$ (which can be rewritten as $y = P^2 - P$) is a quadratic equation, assuming each player has a reputation of 0.5, the probability that `m` will be reached increases when fewer players are remaining. The following math will be displayed on its own.

$$J_\alpha(x) = \sum\limits_{m=0}^\infty \frac{(-1)^m}{m! \, \Gamma(m + \alpha + 1)}{\left({\frac{x}{2}}\right)}^{2 m + \alpha}$$

However, the game is not quite that simple. In every round, a variable is set to a random value such that $\{ x \in \mathbb{Z} \wedge 0 \leq x \leq P(P-1) \}$ where $P = \text{number of players}$. The value $P(P-1)$ or $P^2-P$ comes up often; it is equal to twice the number of hunts that will take place in the current round. The total hunts in a a round is equal to $\binom{P}{2}$ (each player hunts with every other player).

$$ \frac{P(P-1)}{2} = \binom{P}{2} $$

Math is fun.
