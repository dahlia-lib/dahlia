<style>
  .dh2 { color: #0a0; }
  .dh4 { color: #a00; }
  .dh9 { color: #55f; }
  .dha { color: #5f5; }
  .dhb { color: #5ff; }
  .dhc { color: #f55; }
  .dhd { color: #f5f; }
  .dhe { color: #ff5; }
  .dhl { font-weight: bold; }
  .dhm { text-decoration: line-through; }
  .dhn { text-decoration: underline; }
  .dho { font-style: italic; }
  .dimmed { color: #919199; }
</style>

## The basics

All Dahlia formatting is done through instances of the `Dahlia` class. Different
instances transform[^1] strings through their `convert` method—so that each
instance can have its own settings.

```py
from dahlia import Dahlia

dahlia = Dahlia()
print(dahlia.convert("&4hello &lthere"))
```
<div class="highlight"><pre><code><span class="dh4">hello <span class="dhl">there</span></span></code></pre></div>

> See the [Syntax] section of the [Dahlia specification] for a list of all Dahlia
codes.

The `Dahlia` class also exposes `print` and `input` methods that wrap their
built-in counterparts, transforming[^1] the provided arguments:
```py
from dahlia import Dahlia

dahlia = Dahlia()
dahlia.print("&e&nunderlined&rn yellow")
```
<div class="highlight"><pre><code><span class="dhe"><span class="dhn">underlined</span> yellow</span></code></pre></div>

[^1]: See "transformation" in the specification's [glossary].

---

```py
from dahlia import Dahlia

dahlia = Dahlia()
name = dahlia.input("&cWhat is your name? ")
print(f"Oh, hi {name}!")
```
<div class="highlight"><pre><code><span class="dhc">What is your name? </span>Mark
Oh, hi Mark!</code></pre></div>

The `Dahlia` class accepts three optional arguments:

* the color depth[^2],
* the marker, a character that marks the beginning of a Dahlia code,
* the `auto_reset` flag, which specifies whether to automatically reset the
  formatting at the end of a string.

When not specified, Dahlia will try to detect the color depth[^2] of the current
terminal emulator. The detected depth can be accessed through the `depth`
property. If it can't be detected, Dahlia will fall back to `Depth.LOW`. If
colors are disabled (either through `NO_COLOR=1` or `TERM=dumb`), the depth will
stay `None`. You can run the Dahlia package with `python -m dahlia` to see your
current terminal's capabilities.

[^2]: See "color depth" in the specification's [glossary].

The default marker is `&`, and the default value for `auto_reset` is `True`.
Disabling `auto_reset` can be useful, for example, when you want to apply the
formatting to the user's input:
```py
from dahlia import Dahlia

dahlia = Dahlia(marker="§", auto_reset=False)
ans = dahlia.input("§9What's §l9+10§rl? ")
if ans == "21":
    dahlia.print("§2Correct!")
```
<div class="highlight"><pre><code><span class="dh9">What's <span class="dhl">9+10</span>? 21</span>
<span class="dh2">Correct!</span></code></pre></div>

---

```py
from dahlia import Dahlia

Dahlia().print("&ehi", "&othere")
Dahlia(auto_reset=False).print("&ehi", "&othere")
```
<div class="highlight"><pre><code><span class="dhe">hi</span> <span class="dho">there</span>
<span class="dhe">hi <span class="dho">there</span></span></code></pre></div>



## Cleaning utilities
Dahlia provides three utility functions:

* `clean` for removing Dahlia codes from strings
* `clean_ansi` for removing ANSI codes from strings
* `escape` for escaping Dahlia codes in strings

```py
from dahlia import Dahlia, clean, clean_ansi, escape

dahlia = Dahlia()
a = "&aa &b&lbunch &c&nof &d&ostyles &e&mhere"
b = dahlia.convert(a)

print(a)
print(clean(a))
print()
print(repr(b))
print(b)
print(clean_ansi(b))
print(escape(a))
print(dahlia.convert(escape(a)))
```
<div class="highlight"><pre><code>&aa &b&lbunch &c&nof &d&ostyles &e&mhere
a bunch of styles here

'\x1b[38;2;85;255;85ma \x1b[38;2;85;255;255m\x1b[1mbunch \x1b[38;2;255;85;85m\x1b[4mof \x1b[38;2;255;85;255m\x1b[3mstyles \x1b[38;2;255;255;85m\x1b[9mhere\x1b[0m'
<span class="dha">a </span><span class="dhl"><span class="dhb">bunch </span><span class="dhc"><span class="dhn">of </span></span><span class="dho"><span class="dhd"><span class="dhn">styles </span></span><span class="dhe"><span class="dhm"><span class="dhn">here</span></span></span></span></span>
a bunch of styles here
&_aa &_b&_lbunch &_c&_nof &_d&_ostyles &_e&_mhere
&aa &b&lbunch &c&nof &d&ostyles &e&mhere
</code></pre></div>

[glossary]: https://github.com/dahlia-lib/spec/blob/main/SPECIFICATION.md#glossary
[Syntax]: https://github.com/dahlia-lib/spec/blob/main/SPECIFICATION.md#syntax
[Dahlia specification]: https://github.com/dahlia-lib/spec/