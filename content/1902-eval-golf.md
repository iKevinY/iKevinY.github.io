Title: Eval Golf (PlaidCTF Writeup)
Date: 2019-04-15
Slug: eval-golf-plaidctf-writeup

Sticking with the theme of CTF writeups, here's one of a fairly simple challenge from [PlaidCTF 2019](http://plaidctf.com). Given that Python is my programming language of choice, it was fun to work on a Python-based challenge (rather than the low-level exploits that are more common in CTFs).

The service that we're trying to retrieve the flag from executes this script:

```python
#!/usr/bin/env python3

from sys import exit
from secret import secret_value_for_password, flag, exec

try:
    val = 0
    inp = input("Input value: ")
    count_digits = len(set(inp))
    if count_digits <= 10:          # Make sure it is a number
        val = eval(inp)
    else:
        raise

    if val == secret_value_for_password:
        print(flag)
    else:
        print("Nope. Better luck next time.")
except:
    print("Nope. No hacking.")
    exit(1)
```

The obvious thing to exploit here is the line containing `eval()`, which of course is extremely dangerous to use when paired with user-input. However, there are are a couple of safeguards in place that make our job a little more difficult.

The easiest thing to do here is just pass in the string `secret_value_for_password` as the input value. When that string is `eval`'d, it will set `val` to whatever the value of that imported constant is, causing the following `if` condition check to succeed and giving us the flag.

Unfortunately, the code that's supposed to "make sure [the input] is a number" is not actually doing that. What it's actually doing is restricting the length of the input to 10 characters. Interestingly though, since `count_digits` is actually set to the length of `set(inp)`, the actual restriction is only that our input consists of 10 or fewer _distinct characters_ (ie. reusing the same character more than once doesn't contribute to our "limit").

The string `secret_value_for_password` contains 15 characters, which means it will be rejected. Somehow we need to find a way to [golf down](https://en.wikipedia.org/wiki/Code_golf) the unique characters in our payload.

The first that comes to mind is to build up each character of our secret value one-by-one using [`chr()`](https://docs.python.org/3/library/functions.html#chr), which takes in a number and returns the character corresponding to that ASCII value. Of course, we can represent any number we want by summing `1` with itself a bunch of times, which helps us not use up precious unique characters.

```python
>>> target = 'secret_value_for_password'
>>> codepoints = ['+'.join('1' for _ in range(ord(c))) for c in target]
>>> payload = '+'.join('chr({})'.format(c) for c in codepoints)
>>> eval(payload)
'secret_value_for_password'
>>> len(set(payload))
7
```

Excellent, we've managed to put together `secret_value_for_password` using only seven different characters! The problem here is that this payload will set `val` to the string literal `secret_value_for_password`, rather than than the value of that variable itself. We could fix this by wrapping the entire payload in `eval()`, but since we haven't used any of the characters in `eval` yet, this would bump us up to 11 characters -- just above our limit.

Somehow we need to trim one character, but it feels like everything is necessary. We definitely need our parentheses to make any sort of function calls, and the `+` serves the dual purpose of accumulating our ASCII values and also performing the string concatenation.

Rather tantalizingly, the script gives us a variable named `val` which is set to `0`. If this was instead initialized to `1`, we could replace `1` in our payload with `val`, and be at 10 characters exactly (since we have `eval` in our payload anyways).

The trick here is figuring out a way to represent `1` in Python with the following pool of characters: `()+chreval`. Having worked with Python enough, I suspected the solution was something to do with truthiness. If we could somehow get an expression to evaluate to something `True`, we could sum up _that expression_ as a replacement for using the character 1 (because in Python, `True + True = 2`).

The magic bullet here was the built-in [`all()`](https://docs.python.org/3/library/functions.html#all), which returns `True` if all elements of the input iterable are truthy (or if the iterable itself is empty). We already have the characters `a` and `l` from our call to `eval`, and we can simply pass in `()` (the empty tuple). That is, `all(())` serves as our substitute for the character `1`.

With this change, our payload contains exactly 10 unique characters. Putting this all together, we arrive at our final exploit (using [`pwntools`](https://github.com/Gallopsled/pwntools) to execute it):

```python
from pwn import *

target = "secret_value_for_password"

codepoints = ['+'.join('all(())' for _ in range(ord(c))) for c in target]
payload = '+'.join('chr({})'.format(c) for c in codepoints)
payload = 'eval(' + payload + ')'

conn = remote('canyouguessme.pwni.ng', 12349)
conn.sendline(payload)
conn.interactive()
```

This 22KB payload is accepted by the service and gives us our flag!
