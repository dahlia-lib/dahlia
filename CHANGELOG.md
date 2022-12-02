# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

### Remoevd
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