# str2col Design Spec

**Date:** 2026-07-16

## Overview

`str2col` is a small Python utility that deterministically maps any value (string, float, int, or other type coercible to `str`) to a color. It ships as both a Python library and a CLI tool. The same input always produces the same color; an optional seed shifts the mapping while preserving determinism.

## Core Pipeline

```
input → str() → hash (hashlib.md5) → 3 independent byte-chunks → HSL (constrained) → output format
```

1. Any input is coerced to string via `str()`.
2. If a seed is provided, it is appended before hashing: `f"{value}{seed}"`.
3. `hashlib.md5` produces a 16-byte digest. The digest is split into three 4-byte chunks, each interpreted as a big-endian unsigned int and normalized to [0, 1].
4. Each normalized float is linearly remapped into a user-specified range:
   - `hue_range` — degrees, default `(0, 360)`
   - `sat_range` — 0–1, default `(0.4, 0.9)`
   - `light_range` — 0–1, default `(0.35, 0.65)`
5. HSL → RGB via `colorsys.hls_to_rgb` (stdlib).
6. RGB triple is converted to the requested output format.

## Library API

### `Str2Col` class

```python
from str2col import Str2Col

conv = Str2Col(
    seed=None,
    hue_range=(0, 360),
    sat_range=(0.4, 0.9),
    light_range=(0.35, 0.65),
)

conv.to_hex("label")        # → "#a3f2c1"
conv.to_rgb("label")        # → (163, 242, 193)       integers 0–255
conv.to_rgb_float("label")  # → (0.639, 0.949, 0.757) floats 0–1
conv.to_hsl("label")        # → (150.2, 0.65, 0.50)   (hue°, sat, light)
conv.to_ansi_fg("label")    # → "\033[38;2;163;242;193m"  (no reset appended)
conv.to_ansi_bg("label")    # → "\033[48;2;163;242;193m"  (no reset appended)
```

All `to_*` methods accept any value and coerce it internally.

### Lightweight function

```python
from str2col import str2col

str2col("label")             # → "#a3f2c1"  (default: hex, default ranges, no seed)
str2col("label", fmt="rgb")  # → (163, 242, 193)
str2col("label", seed="myapp", hue_range=(180, 300))
```

`str2col()` is equivalent to `Str2Col(**kwargs).to_<fmt>(value)`.

## CLI

```
str2col [value] [options]
```

`value` may be a positional argument or piped via stdin. Both work simultaneously if needed.

| Option | Description |
|--------|-------------|
| `--format hex\|rgb\|rgb_float\|hsl\|ansi_fg\|ansi_bg` | Output format (default: `hex`) |
| `--seed SEED` | Salt for hashing |
| `--hue-range MIN MAX` | Hue range in degrees |
| `--sat-range MIN MAX` | Saturation range 0–1 |
| `--light-range MIN MAX` | Lightness range 0–1 |
| `--text TEXT` | Print TEXT colored with the result (wraps in ANSI escapes + reset) |

Examples:

```bash
str2col "my label"
str2col "my label" --format rgb --seed myapp
str2col "my label" --format ansi_fg --text "hello"
echo "my label" | str2col --format hex
```

## Project Structure

```
str2col/
├── str2col/
│   ├── __init__.py    # exports Str2Col, str2col
│   ├── core.py        # Str2Col class: hash → HSL → to_* methods
│   └── cli.py         # argparse entry point
├── tests/
│   └── test_core.py
└── pyproject.toml
```

## Dependencies

None beyond the Python standard library (`hashlib`, `colorsys`, `argparse`).

## Packaging

Distributed as a pip-installable package. The CLI is registered as a `console_scripts` entry point in `pyproject.toml` so `str2col` is available on `PATH` after install.
