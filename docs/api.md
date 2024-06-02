## `clean`
```py
def clean(string: str, marker: str = "&") -> str
```
Removes all Dahlia codes from a string.

## `clean_ansi`
```py
def clean_ansi(string: str, marker: str = "&") -> str
```
Removes all ANSI codes from a string.

## `Dahlia`
```py
DepthInt = Literal[3, 4, 8, 24]

class Dahlia(
    *,
    depth: Depth | DepthInt | str | None = None,
    marker: str = "&",
    auto_reset: bool = True,
)
```
The core `Dahlia` class. Accepts the following arguments:

* `depth`: the color depth[^1] to use for styling; when `None`, Dahlia will try
  to detect the color depth of the current terminal emulator (`Depth.LOW` will
  be used as a fallback). The detected depth can be accessed through the `depth`
  property (will stay `None` if `NO_COLOR=1` or `TERM=dumb`); defaults to `None`
* `marker`: the character used to mark the beginning of a Dahlia formatting
  code; must be a single character; defaults to `&`
* `auto_reset`: whether to automatically reset the formatting at the end of a
  string; defaults to `True`

Dahlia instances are comparable and hashable.

### `Dahlia.convert`
```py
def convert(self, string: str) -> str
```
Transforms[^2] a Dahlia string.

### `Dahlia.input`
```py
def input(self, prompt: str) -> str
```
Wraps the built-in `input` by transforming[^2] the prompt.

### `Dahlia.print`
```py
def print(self, *args: object, **kwargs: Any) -> None
```
Wraps the built-in `print` by transforming[^2] all positional arguments and
passing through all keyword arguments.

## `Depth`
```py
class Depth(Enum):
    TTY = 3
    LOW = 4
    MEDIUM = 8
    HIGH = 24
```
Specifies usable color depth[^1] levels.

[^1]: See "color depth" in the specification's [glossary].
[^2]: See "transformation" in the specification's [glossary].
[glossary]: https://github.com/dahlia-lib/spec/blob/main/SPECIFICATION.md#glossary