# str2col

Map any value to a color. The same input always produces the same color.

```python
from str2col import Str2Col, str2col

# one-off
str2col("hello")              # "#a3c9f1"
str2col("hello", fmt="rgb")   # (163, 201, 241)

# reusable converter with constraints
conv = Str2Col(seed="myapp", hue_range=(180, 300), sat_range=(0.5, 0.8))
conv.to_hex("label A")        # "#..."
conv.to_rgb("label A")        # (R, G, B)
conv.to_hsl("label A")        # (hue, sat, light)
conv.to_ansi_fg("label A")    # "\033[38;2;...m"
conv.to_ansi_bg("label A")    # "\033[48;2;...m"
```

Any type works: strings, ints, floats, `None`.

## Install

```bash
pip install str2col
```

No runtime dependencies.

## CLI

```bash
str2col hello
str2col hello --format rgb
str2col hello --format ansi_fg --text "hello world"
echo "hello" | str2col
```

Options:

| Flag | Default | Description |
|------|---------|-------------|
| `--format` / `-f` | `hex` | `hex`, `rgb`, `rgb_float`, `hsl`, `ansi_fg`, `ansi_bg` |
| `--seed` | none | shift the color mapping |
| `--hue-range MIN MAX` | `0 360` | restrict hue (degrees) |
| `--sat-range MIN MAX` | `0.4 0.9` | restrict saturation |
| `--light-range MIN MAX` | `0.35 0.65` | restrict lightness |
| `--text TEXT` | none | print TEXT in the computed color |

## How it works

The input is coerced to a string and hashed with MD5. Three independent 4-byte chunks of the digest are mapped into the configured HSL ranges, then converted to the requested output format via Python's `colorsys` module.
