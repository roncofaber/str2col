import hashlib
import colorsys


def _hash_value(value, seed):
    key = str(value) if seed is None else f"{value}{seed}"
    digest = hashlib.md5(key.encode()).digest()
    h = int.from_bytes(digest[0:4], "big") / 0xFFFFFFFF
    s = int.from_bytes(digest[4:8], "big") / 0xFFFFFFFF
    l = int.from_bytes(digest[8:12], "big") / 0xFFFFFFFF
    return h, s, l


def _remap(v, low, high):
    return low + v * (high - low)


class Str2Col:
    def __init__(self, seed=None, hue_range=(0, 360), sat_range=(0.4, 0.9), light_range=(0.35, 0.65)):
        self.seed = seed
        self.hue_range = hue_range
        self.sat_range = sat_range
        self.light_range = light_range

    def _to_rgb_float(self, value):
        h, s, l = _hash_value(value, self.seed)
        hue = _remap(h, self.hue_range[0], self.hue_range[1]) / 360.0
        sat = _remap(s, self.sat_range[0], self.sat_range[1])
        light = _remap(l, self.light_range[0], self.light_range[1])
        r, g, b = colorsys.hls_to_rgb(hue, light, sat)
        return r, g, b

    def to_rgb_float(self, value):
        return self._to_rgb_float(value)

    def to_rgb(self, value):
        r, g, b = self._to_rgb_float(value)
        return (round(r * 255), round(g * 255), round(b * 255))

    def to_hex(self, value):
        r, g, b = self.to_rgb(value)
        return f"#{r:02x}{g:02x}{b:02x}"

    def to_hsl(self, value):
        h, s, l = _hash_value(value, self.seed)
        hue = _remap(h, self.hue_range[0], self.hue_range[1])
        sat = _remap(s, self.sat_range[0], self.sat_range[1])
        light = _remap(l, self.light_range[0], self.light_range[1])
        return (hue, sat, light)

    def to_ansi_fg(self, value):
        r, g, b = self.to_rgb(value)
        return f"\033[38;2;{r};{g};{b}m"

    def to_ansi_bg(self, value):
        r, g, b = self.to_rgb(value)
        return f"\033[48;2;{r};{g};{b}m"


def str2col(value, seed=None, hue_range=(0, 360), sat_range=(0.4, 0.9), light_range=(0.35, 0.65), fmt="hex"):
    conv = Str2Col(seed=seed, hue_range=hue_range, sat_range=sat_range, light_range=light_range)
    if fmt == "hex":
        return conv.to_hex(value)
    elif fmt == "rgb":
        return conv.to_rgb(value)
    elif fmt == "rgb_float":
        return conv.to_rgb_float(value)
    elif fmt == "hsl":
        return conv.to_hsl(value)
    elif fmt == "ansi_fg":
        return conv.to_ansi_fg(value)
    elif fmt == "ansi_bg":
        return conv.to_ansi_bg(value)
    else:
        raise ValueError(f"Unknown format: {fmt}")
