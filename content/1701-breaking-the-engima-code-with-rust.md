Title: Breaking the Enigma Code With Rust
Date: 2017-04-17

If I had to pick something from the humanities to study in university, I would probably go with history. Not only is history interesting in and of itself, but having a good grasp on history clarifies a lot of modern geopolitics. War is probably one of the more "exciting" aspects of history, and while it goes without saying that war is terrible, a lot of technologies and even new fields of research are the product of wartime conditions.

The Enigma machines are a series of electromechanical cipher machines that were famously used by Germany in World War II to encrypt military communications. Breaking the Enigma code had a huge impact on the Allies' ability to win the war. Most of what I could write about the history of cracking Enigma is already covered by [this Wikipedia article](https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma) (or if you prefer a more dramatized version, a [certain movie](https://en.wikipedia.org/wiki/The_Imitation_Game) starring Benedict Cumberbatch), so I won't go over it in detail.

Inspired by the [computers](https://en.wikipedia.org/wiki/Colossus_computer) that were born out of cryptanalysis, I decided to write my own Enigma-cracking program in Rust -- [ `ultra`](https://github.com/iKevinY/ultra). "Ultra secret" was the classification level used by the Allies to refer to intelligence obtained via deciphering German communications at [Bletchley Park](https://en.wikipedia.org/wiki/Bletchley_Park). If the Germany had discovered that the Allies could read their messages, they easily could have switched to a completely new encryption method, nullifying all the effort spent breaking Enigma in the first place.

To demonstrate how the Enigma cipher was employed, here is some example usage from `ultra`. First, we encrypt this plaintext message using some random machine settings:

```bash
$ ultra --randomize "\
A few miles south of Soledad, the Salinas River drops in close to the hillside bank and runs deep and green. The water is warm too, for it has slipped twinkling over the yellow sands in the sunlight before reaching the narrow pool."
S rkz yypvn dsory vc Xbjvauu, yos Tlkdcmx Qpwcd tpgsf zj euqpp op vvd iwuffxjz umes nmk yamh zkdq vwk vavwc. Nkh fmyzp gk rfhe sgx, qth ml psm qasmrkl npmhsxdou jqwx hba eiyeur qtoci kq lqb hxqczkqn mdodir scdmsprt ddm ywnbgz uemo.
(Rotors: 215, Key Setting: YFI, Ring Setting: UZW)
```

When this ciphertext is encrypted using the same settings, we recover the original message:

```bash
$ ultra --rotor=215 --key=YFI --ring=UZW "\
S rkz yypvn dsory vc Xbjvauu, yos Tlkdcmx Qpwcd tpgsf zj euqpp op vvd iwuffxjz umes nmk yamh zkdq vwk vavwc. Nkh fmyzp gk rfhe sgx, qth ml psm qasmrkl npmhsxdou jqwx hba eiyeur qtoci kq lqb hxqczkqn mdodir scdmsprt ddm ywnbgz uemo."
A few miles south of Soledad, the Salinas River drops in close to the hillside bank and runs deep and green. The water is warm too, for it has slipped twinkling over the yellow sands in the sunlight before reaching the narrow pool.
```

Now, let's attempt to decipher the message with no knowledge of the correct settings:

```bash
$ ultra --decrypt "\
S rkz yypvn dsory vc Xbjvauu, yos Tlkdcmx Qpwcd tpgsf zj euqpp op vvd iwuffxjz umes nmk yamh zkdq vwk vavwc. Nkh fmyzp gk rfhe sgx, qth ml psm qasmrkl npmhsxdou jqwx hba eiyeur qtoci kq lqb hxqczkqn mdodir scdmsprt ddm ywnbgz uemo."
A few miles south of Soledad, the Salinas River drops in close to the hillside bank and runs deep and green. The water is warm too, for it has slipped twinkling over the yellow sands in the sunlight before reaching the narrow pool.
(Rotors: 215, Key Setting: EZI, Ring Setting: ATW)
```

We managed to recover the plaintext from nothing but the ciphertext! The decryption algorithm used in `ultra` was largely inspired by some of James Lyon's articles on the Enigma machine on his website [Practical Cryptography](http://practicalcryptography.com/ciphers/mechanical-era/enigma/).

It is important to make a distinction between the algorithm used by `ultra` and the cryptanalysis that was performed at Bletchley Park. The methods that were actually used to crack Enigma during World War II involved intercepting messages where parts of the plaintext could be guessed, which mostly came in the form of weather reports and other routine communications.

On the other hand, the way that `ultra` deciphers messages is purely statistical. [This file](https://github.com/iKevinY/ultra/blob/master/src/data/quadgrams.txt) contains a list of quadgrams (four-letter sequences) from a fairly sizeable English corpus, and their number of occurrences. According to this, the top 5 most common English quadgrams are *TION*, *NTHE*, *THER*, *THAT*, and *OFTH*, which seems reasonable. At the bottom of the file, we find extremely uncommon quadgrams, such as *AAJZ*.

If we take a given piece of ciphertext and attempt to decrypt it with random Enigma settings, it will almost certainly look like gibberish. However, we know at least one configuration will produce something that seems like reasonable English: the one used to encrypt the message in the first place! Therefore, all we have to do is iterate through all possible machine settings, decrypt the ciphertext, compute a "fitness score" based on how similar it looks to English, and choose the setting that resulted in the best score.

To come up with a fitness score, we use a statistical [language model](https://en.wikipedia.org/wiki/Language_model), and define the probability of any given phrase as the product of its component quadgrams (ignoring things like word boundaries). For example, the probability of the message "APPLE" would be calculated by taking the product of the probabilities of _APPL_ and _PPLE_.

$$\Pr(\text{APPLE}) = \Pr(\text{APPL}) \times \Pr(\text{PPLE})$$

The probability of a single quadgram is given by $\Pr(q) = \frac{C(q)}{N}$, where $C(q)$ is the count of a given quadgram, and $N$ is the sum of all quadgram counts in our list. Because computers have finite floating-point precision, it is ill-advised to multiply several tiny floats together. Luckily, we can use logarithms to map these multiplications to additions, and because $\log(x) > \log(y)$ for all $x > y ≥ 0$, it is fine to use this log probability as our fitness function.

$$\log(\Pr(\text{APPLE})) = \log(\frac{C(\text{APPL})}{N}) + \log(\frac{C(\text{PPLE})}{N})$$

Using the identity $\log(\frac{a}{b}) = \log(a) - \log(b)$, this can be simplified even further:

$$\log(\Pr(\text{APPLE})) = \log(C(\text{APPL})) + \log(C(\text{PPLE})) - 2\log(N)$$

The final $\log(N)$ term will have a coefficient of the number of quadgrams in the input message. Because encrypting a message doesn't change its length, this term would only cause a constant difference in the fitness function, and can therefore be completely omitted. This leaves us with a simple fitness function: the sum of the log-counts of all quadgrams in the message.

Typical usage of the M3 Enigma machine involved choosing 3 of 5 possible rotors. Because the order of the rotors matters, this comes out to 60 possible permutations. Each rotor has 26 different "key settings" (sometimes referred to as "indicator settings") and 26 different "ring settings", leaving us with $60 \times 26^6$, or $18\,534\,946\,560$ possible rotor configurations.

When you take into account the [plugboard](https://en.wikipedia.org/wiki/Enigma_machine#Plugboard), the number of settings is [in the quintillions](http://crypto.stackexchange.com/questions/33628/how-many-possible-enigma-machine-settings), so we won't even consider trying to break this using our ciphertext-only attack. However, this still leaves approximately 18 billion permutations. Even if it only took 1 microsecond to try each one, it would still take 5 hours to work through the entire problem space. Fortunately, with some clever optimization, we can reduce the number of permutations to just over 1.5 million.

We can search for the optimal rotors and key settings separately from their ring settings. The ring settings determine offsets for the rotors' notches (the position at which the fast rotor advancing causes the middle rotor to advance, and likewise between the middle and the slow rotors). If we find the correct rotors and key settings with the wrong ring settings, the resulting plaintext will be somewhat correct, with errors where the rotors advanced in the wrong place.

First, we check all possible rotor and key permutations, fixing the ring settings as "AAA". We pick the best of those, and then try key and ring settings for the fast and middle rotors; the slow rotor doesn't "turn" any other rotors, so its ring setting doesn't influence the decryption, and therefore we can safely ignore it. This leaves us with a total of $60 \times 26^3 + 26^4$, or $1\,511\,536$ settings to check -- a reasonable number to brute-force on a modern computer.

----

Seeing as `ultra` was my first real Rust project, I figured I would also share some thoughts I have about it. Perhaps Rust's primary selling point is memory safety. My introductory computer systems course was essentially one extended lecture about everything that can go wrong with `malloc` and pointers. While being familiar with using Valgrind is neat, it's nice to not have to think about these things at all, and just focus on writing the implementation.

In addition, between closures and iterators, Rust makes it easy to write functional code. Because of my prior experience with Python, Haskell, and [Racket](https://racket-lang.org), I felt right at home using Rust. Chaining together iterator adapters and collecting the result rather than iteratively pushing values into a vector with a for-loop reminded me of using list comprehensions in Python.

The bulk of `ultra`'s decryption algorithm involves iterating over Enigma settings, running the ciphertext through it, and returning the one with the highest fitness score. This lends itself nicely to parallelization; by splitting up the work, each worker can compute the maximum of its subset of the work, and the final result is the max of _those_ maximums.

Using the amazing [Rayon](https://github.com/nikomatsakis/rayon) data parallelism library, many Rust iterators can be parallelized nearly effortlessly. With `ultra`, I essentially just needed to import Rayon's prelude and add a couple of calls to `into_par_iter()`. (I also had to collect into a vector because the result of `iproduct!` can't be directly transformed into a parallel iterator.)

```
#!rust
use rayon::prelude::*;

let (rotor, key) = iproduct!(rotors.iter(), keys.iter())
    .collect::<Vec<_>>()  // These two lines turn a normal
    .into_par_iter()      // iterator into a parallel one!
    .max_by_key(|&(rotor, key)| { ... })
    .unwrap();
```

What makes this feel magical is that I didn't even have to think about managing multi-threaded memory access; the parallelization just works, and all I had to do was add three lines of code. Languages with a rich library ecosystem tend to flourish, and the existence of cool libraries like Rayon gives me a lot of confidence in the future of Rust.

Since Rust advertises itself as being "blazingly fast", I decided to do some benchmarking by comparing James' [sample C code](http://practicalcryptography.com/cryptanalysis/breaking-machine-ciphers/cryptanalysis-enigma/#c-code-for-breaking-enigma) to sequential and parallel versions of `ultra`. These are the times that I got while testing on my quad-core MacBook Pro:

|                   | **real (s)** | **user (s)** |
|:----------------- |:------------:|:------------:|
| C (reference)     | 43.8         | 43.4         |
| Rust (sequential) | 19.2         | 19.0         |
| Rust (parallel)   | 4.5          | 28.4         |

The sequential version of `ultra` already runs about twice as fast as the C version, and after adding the parallelization described above, it jumps to nearly 10 times as fast!

When writing `ultra`, I didn't explicitly set out to implement a hyper-optimized version of James' code. Instead, I used the description of the algorithm described in his blog post and wrote what I felt was idiomatic Rust. I think this nicely demonstrates the fact that Rust makes it easy to write programs that are readable and also performant.

Cargo also plays a large role in making Rust nice work with. Nothing is more annoying than coming across an open source project that seems useful, but struggling to figure out how to even compile it. With a Rust project, however, you're essentially guaranteed that `cargo build` will work -- no Makefiles or manual dependency management required.

I really enjoyed learning about Rust while building [`ultra`](https://github.com/iKevinY/ultra), and will definitely be using it more in the future. Given the results of Stack Overflow's recent [developer survey](https://stackoverflow.com/insights/survey/2017), it seems like Rust is growing in popularity -- it will be very exciting if it becomes adopted by industry.
