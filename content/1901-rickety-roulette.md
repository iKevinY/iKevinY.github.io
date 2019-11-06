Title: Rickety Roulette (picoCTF Writeup)
Date: 2019-03-25

Recently, I've taken an interest in [CTFs](https://en.wikipedia.org/wiki/Capture_the_flag#Computer_security): computer security competitions with tasks that have been specifically designed to have a specific weakness. The goal is to exploit these weaknesses through various methods -- such as reverse engineering, binary exploitation, or cryptanalysis -- in order to recover a "flag": a password that follows a specific format, like `flag{s3cret_c0de}`.

My university started a [CTF club](https://ubcctf.github.io) last month, and since I'm quite new to this field, I've been working my way through [picoCTF](https://picoctf.com), which is an oft-recommended beginner resource. Since I haven't written any technical articles in a while, I thought it would be interesting to provide write-ups for some of the more interesting problems, starting with one called `roulette`. (The source code as provided by picoCTF can be found [here]({static}/files/roulette.c), in case you'd like to try the challenge yourself first.)

If we connect to the service, we see the following:

```text
Welcome to ONLINE ROULETTE!
Here, have $3249 to start on the house! You'll lose it all anyways >:)

How much will you wager?
Current Balance: $3249    Current Wins: 0
```

If you enter an amount greater than your current balance, the program will reject your wager. Choosing a valid amount allows you to guess which number will come up:

```text
> 5000
You can't bet more than you have!
How much will you wager?
Current Balance: $3249   Current Wins: 0
> 100
Choose a number (1-36)
> 1

Spinning the Roulette for a chance to win $200!

Roulette  :  2

WRONG
You're never gonna win
```

On the off chance that you manage to guess the correct value, the program will fairly reward you with twice your wagered amount. We've been told that the goal is to accrue $1 billion, and upon doing so, we'll be rewarded with the flag. With only a 1-in-36 chance of doubling our money, it's simply not possible to get anywhere close by pure chance. Therefore, we'll have to find a way to beat the system.

Let's analyze the program piece-by-piece to see if we can identify any weaknesses (the code snippets I've included in this post are slightly reformatted from the original source provided above, for space efficiency). For starters, here's the `main` function:

```c
#define HOTSTREAK 3
#define MAX_WINS 16
#define ONE_BILLION 1000000000

long cash = 0;
long wins = 0;

int main(int argc, char* argv[]) {
  cash = get_rand();

  while (cash > 0) {
    long bet = get_bet();
    cash -= bet;
    long choice = get_choice();

    play_roulette(choice, bet);

    if (wins >= MAX_WINS) {
      printf("Wow you won %lu times? Looks like its time for you cash you out.\n", wins);
      exit(-1);
    }

    if (cash > ONE_BILLION) {
      printf("*** Current Balance: $%lu ***\n", cash);
      if (wins >= HOTSTREAK) {
        puts("Wow, I can't believe you did it.. You deserve this flag!");
        print_flag();
        exit(0);
      } else {
        puts("Wait a second... You're not even on a hotstreak! Get out of here cheater!");
        exit(-1);
      }
    }
  }
  puts("Haha, lost all the money I gave you already? See ya later!");
  return 0;
}
```

The program gives us a random amount of money to start with, and as long as we still have money, allows us to keep play roulette. Of note is the call to `print_flag()` -- getting the program to execute this function will give us our flag.

If we have more than $1 billion dollars, we enter the part of the program that checks whether the flag should be printed or not. However, take note of the `wins >= HOTSTREAK` check; if the current number of wins is less than 3, the system detects that we somehow tampered with our cash balance _without_ going through the hassle of actually winning multiple rounds in a row, accuses us of cheating, and kicks us out.

Let's take a look at `get_bet()` and see if there's anything we can exploit there.

```c
long get_bet() {
  while (1) {
    puts("How much will you wager?");
    long bet = get_long();
    if (bet <= cash) {
      return bet;
    } else {
      puts("You can't bet more than you have!");
    }
  }
}
```

This looks pretty standard: continuously ask the player for their wager until they provide a valid bet, and then return that amount. One common bug in programs like this is the possibility of [integer overflow](https://en.wikipedia.org/wiki/Integer_overflow), so let's investigate `get_long()` for bugs.

```c
int is_digit(char c) {
  return '0' <= c && c <= '9';
}

long get_long() {
  printf("> ");
  uint64_t l = 0;
  char c = 0;

  while (!is_digit(c))
    c = getchar();

  while (is_digit(c)) {
    if (l >= LONG_MAX) {
      l = LONG_MAX;
      break;
    }
    l *= 10; l += c - '0';
    c = getchar();
  }

  while (c != '\n')
    c = getchar();

  return l;
}
```

`get_long()` iterates over the given input character-by-character, ignoring anything that isn't a digit, and gradually accumulates the value in `l`. If it ever exceeds the value of `LONG_MAX` (a constant provided by `limits.h`), the balance is set to `LONG_MAX`, presumably as an attempt to guard against interflow overflow bugs.

However, it turns out this function is still exploitable. Since a `long` is a signed value, exceeding `LONG_MAX` will cause the value to "wrap around" to a negative number. We find that the program is compiled for 32-bit CPUs, so we simply need a value greater than 2³¹ − 1 = 2147483647:

```text
How much will you wager?
Current Balance: $4962   Current Wins: 0
> 2500000000
Choose a number (1-36)
> 1

Spinning the Roulette for a chance to win $705032704!
```

Great, we've found a way to effectively win as much money as we want, which means it's trivial to achieve a balance of $1 billion. However, there's still the issue of having to win at least 3 times _before_ reaching that amount (otherwise the cheat-detection will kick in).

Of course, one approach we can take is to simply bet $0 over and over until we get lucky on the 1/36 dice roll three times, then trigger the overflow on our balance. However, the roulette program plays a "fun" animation when spinning the wheel that takes around 10 seconds, and the time we're allowed to stay connected to the service is limited to a few minutes, so it's still astronomically unlikely that we'd be able to win enough times before being kicked out. We'll have to find a way to beat the odds.

Recall that we get a random amount of money every time we connect to the roulette service. Let's take a closer look at the implementation of `get_rand()`, the function that dictates our starting balance:

```c
long get_rand() {
  long seed;
  FILE* f = fopen("/dev/urandom", "r");
  fread(&seed, sizeof(seed), 1, f);
  fclose(f);
  seed = seed % 5000;
  if (seed < 0) seed *= -1;
  srand(seed);
  return seed;
}
```

It reads in some bytes from [`/dev/urandom`](https://en.wikipedia.org/wiki//dev/random), truncates the result to the interval `[0, 5000)`, and returns that as our starting balance.

The bug here lies in one somewhat innocuous-looking call: `srand(seed)`. This seeds the random number generation for the program, which by itself isn't a huge deal. However, remember that the value of `seed` becomes our starting balance -- the program reveals the seed to us!

`play_roulette()` uses `rand()` to choose which number the wheel lands on, and since we know the seed, the sequence of spins is actually deterministic! Let's write up a quick program to generate what values we should guess by taking the seed (our initial balance) as a command line argument, and then emulating the roulette logic to print the next few results:

```c
#include <stdio.h>
#include <stdlib.h>

#define ROULETTE_SIZE 36

int main(int argc, char* argv[]) {
  long seed = strtol(argv[1], NULL, 10);
  srand(seed);

  for (int i = 0; i < 5; i++) {
    printf("%i\n", (rand() % ROULETTE_SIZE) + 1);
  }

  return 0;
}
```

However, if we use this program to choose our guesses, we find that we get the first one right, but after that it fails. Did we misunderstand the behaviour of the roulette program and just get lucky? Let's take a closer look at the `play_roulette` function to see if we can figure out what went wrong:

```c
void play_roulette(long choice, long bet) {
  printf("Spinning the Roulette for a chance to win $%lu!\n", 2 * bet);
  long spin = (rand() % ROULETTE_SIZE) + 1;
  spin_roulette(spin);

  if (spin == choice) {
    cash += 2 * bet; wins += 1;
    puts(win_msgs[rand() % NUM_WIN_MSGS]);
  } else {
    puts(lose_msgs1[rand() % NUM_LOSE_MSGS]);
    puts(lose_msgs2[rand() % NUM_LOSE_MSGS]);
  }
}
```

It turns out that the program calls `rand()` to pick random winning/losing messages to display to the player, and this advances the PRNG. Therefore, we should account for this by choosing every _other_ number produced by the program we wrote (assuming we always hit the winning branch; we would have to skip two RNG results if we ever lose).

With this new insight, let's beat roulette for good:

```text
$ nc 2018shell.picoctf.com 26662
Welcome to ONLINE ROULETTE!
Here, have $3249 to start on the house! You'll lose it all anyways >:)
```

We pass the seed to the program we wrote to figure out which numbers to bet on.

```sh
$ ./rand 3249
9
29
6
29
1
```

This tells us that the roulette will land on 9, 6, then 1, so let's guess those!

```text
How much will you wager?
Current Balance: $3249   Current Wins: 0
> 0
Choose a number (1-36)
> 9

Spinning the Roulette for a chance to win $0!

Roulette  :  9

Wow.. Nice One!

How much will you wager?
Current Balance: $3249   Current Wins: 1
> 0
Choose a number (1-36)
> 6

Spinning the Roulette for a chance to win $0!

Roulette  :  6

Alright, now you're cooking!

How much will you wager?
Current Balance: $3249   Current Wins: 2
> 0
Choose a number (1-36)
> 1

Spinning the Roulette for a chance to win $0!

Roulette  :  1

You're not cheating are you?
```

Now that we've won three times, we just need to underflow our balance like we did earlier on (we guess a losing number so that our bet doesn't get re-added upon winning):

```text
How much will you wager?
Current Balance: $3249   Current Wins: 3
> 2500000000
Choose a number (1-36)
> 1

Spinning the Roulette for a chance to win $705032704!

Roulette  :  12

WRONG
Just give up!

*** Current Balance: $1794970545 ***
Wow, I can't believe you did it.. You deserve this flag!
picoCTF{redacted}
```

Success! This was an interesting problem because all it took to find the vulnerabilities was a careful pass through the source code. In addition, both the bugs are things that could easily sneak their way into an actual codebase if not careful. For my next writeup, I'm planning on tackling a problem that requires more sophisticated tooling and background knowledge.
