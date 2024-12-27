# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2024-12-28

### Added
- Python 3.13 support
- An `escape` utility function
- Running `python -m dahlia` now displays the lib version

### Changed
- Improved error message for an invalid marker type
  (by [@cadaniel02][cadaniel02])

### Fixed
- Corrected edge case behavior when trying to use a regex character (e.g. `?` or
  `$`) as a marker
- Fixed custom color processing

### Removed
- Python 3.8 support

[cadaniel02]: https://github.com/cadaniel02/

## [3.0.0] - 2024-06-02

This release follows the [Dahlia Specification v1.0.0][spec].

### Added
- Automatic color depth detection (as a consequence, `Dahlia`'s `depth`
  parameter can now be `None`)
- [Style-specific reset codes][spec-reset]
- [The `&_` escape code][spec-esc]
- The `clean_ansi` function should now handle way more ANSI escape codes
- The package can now be executed with `python -m dahlia` to show the current
  terminal emulator's capabilities
- Various performance improvements:
  - String conversions are now approximately ~70% faster
  - A comprehensive benchmark showed an overall library speedup of 20%

### Changed
- The "Blink" style code was changed from `&p` to `&k`
- The custom color syntax was changed from `&[#ffaff3]` to `&#ffaff3;` and now
  supports shorthand 3-digit codes
- The `Dahlia.depth` property now returns a `Depth | None` instead of an `int`
- The full reset code is now `&R` instead of `&r`
- The "Hide" style code was changed from `&k` to `&h`
- The `no_reset` parameter and property was renamed to `auto_reset` and now
  defaults to `True`

### Fixed
- Type checkers no longer complain about non-lowercase depth strings

### Removed
- `Dahlia.reset`
- `Dahlia.test`
- Dahlia's `no_color` parameter
- The CLI tool
- The `&g` code
- The legacy `dahlia`, `dprint`, and `dinput` functions
- The `quantize_ansi` utility function

[spec]: https://github.com/dahlia-lib/spec/
[spec-reset]: https://github.com/dahlia-lib/spec/blob/main/SPECIFICATION.md#resetting
[spec-esc]: https://github.com/dahlia-lib/spec/blob/main/SPECIFICATION.md#escaping

## [2.3.2] - 2023-04-19

### Fixed
- Dahlia objects with different markers are no longer considered equal

## [2.3.1] - 2023-02-20

### Fixed
- Python 3.8 compatibility

## [2.3.0] - 2023-02-16

### Added
- `quantize_ansi` by [@Lunarmagpie](https://github.com/Lunarmagpie)

## [2.2.2] - 2023-01-03

### Added
- Legacy `dinput` function

### Fixed
- Corrected legacy `dahlia` and `dinput` function typehints

## [2.2.1] - 2022-12-27

### Changed
- Minor CLI improvements

### Fixed
- Changed the default depth in the Dahlia CLI to 4

## [2.2.0] - 2022-12-21

### Added
- New format codes:
  - `i` - invert
  - `j` - dim
  - `k` - hide
  - `p` - blink
- String and integer literals can now be used to specify the depth, e.g. `dprint("&3hi", depth="tty")` or `Dahlia(depth=24)`
- `no_color` kwarg (has priority over the `NO_COLOR` environment variable)

### Changed
- Changed the default depth to LOW (4-bit)

### Fixed
- Fixed encoding background colors for lower color depths

## [2.1.3] - 2022-12-02

### Fixed
- Added depth 4 as a valid option in the Dahlia CLI
- Fixed Python 3.8 compatibility
- Fixed non-HIGH depths failing during conversion

## [2.1.2] - 2022-12-01

### Added
- `py.typed` file by [@Lunarmagpie](https://github.com/Lunarmagpie)

### Changed
- `__main__.py:main` now uses `sys.exit` instead of `exit`
- Improved project structure

### Fixed
- Fixed 4-bit colors being entirely unused by the `__get_ansi` function

Also thanks to [@Sigmanificient](https://github.com/Sigmanificient) for minor improvements!

## [2.1.1] - 2022-11-01

### Fixed
- Included `dahlia` and `dprint` functions in the module's `__all__`

## [2.1.0] - 2022-11-01

### Added
- 4-bit colors
- Custom marker support
- Legacy `dahlia` and `dprint` functions
- `black` and `isort` as dev dependencies

## [2.0.0] - 2022-09-24

### Added
- Support for the NO_COLOR environment variable
- `Depth` enum for `Dahlia` construction

### Changed
- Functions `dahlia`, `dprint`, and `dinput` have been replaced by the `Dahlia` class with methods `convert`, `print`, and `input`, respectively

### Removed
- Global `config` variable

## [1.1.0] - 2022-08-12

### Added
- `dinput` function
- `reset` function
- `no_reset` parameter for `dahlia`, `dprint`, `dinput`.

## [1.0.0] - 2022-07-12

Initial release 🎉

[1.0.0]: https://github.com/trag1c/Dahlia/releases/tag/1.0.0
[1.1.0]: https://github.com/trag1c/Dahlia/compare/1.0.0...1.1.0
[2.0.0]: https://github.com/trag1c/Dahlia/compare/1.1.0...2.0.0
[2.1.0]: https://github.com/trag1c/Dahlia/compare/2.0.0...2.1.0
[2.1.1]: https://github.com/trag1c/Dahlia/compare/2.1.0...2.1.1
[2.1.2]: https://github.com/trag1c/Dahlia/compare/2.1.1...2.1.2
[2.1.3]: https://github.com/trag1c/Dahlia/compare/2.1.2...2.1.3
[2.2.0]: https://github.com/trag1c/Dahlia/compare/2.1.3...2.2.0
[2.2.1]: https://github.com/trag1c/Dahlia/compare/2.2.0...2.2.1
[2.2.2]: https://github.com/trag1c/Dahlia/compare/2.2.1...2.2.2
[2.3.0]: https://github.com/trag1c/Dahlia/compare/2.2.2...2.3.0
[2.3.1]: https://github.com/trag1c/Dahlia/compare/2.3.0...2.3.1
[2.3.2]: https://github.com/trag1c/Dahlia/compare/2.3.1...2.3.2
[3.0.0]: https://github.com/trag1c/Dahlia/compare/2.3.2...3.0.0
