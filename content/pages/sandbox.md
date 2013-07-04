Title: Sandbox

This page is a sandbox page for testing how the Markdown engine will render certain elements.

# H1
## H2
### H3

# Code

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

## Unordered Lists

* List item
* List item

# Ordered Lists

1. Ordered lists
2. Have numbers

## Abbreviations

The HTML specification 
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium

## Definitions

Apple
:   Pomaceous fruit of plants of the genus Malus in 
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

## Footnotes

Footnotes[^1] have a label[^label] and a definition[^!DEF].

## Tables

First Header  | Second Header | Third Header
------------- | ------------- | ------------
Content Cell  | Content       | Lots of content here
Content Cell  | Content       | Not so much

[^1]: This is a footnote
[^label]: A footnote on "label"
[^!DEF]: The definition of a footnote.


///Footnotes Go Here///