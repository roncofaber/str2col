import hashlib
import colorsys


def _hash_value(value, seed):
    key = str(value) if seed is None else f"{value}{seed}"
    digest = hashlib.md5(key.encode()).digest()
    c = [int.from_bytes(digest[i*4:(i+1)*4], "big") for i in range(4)]
    mask = 0xFFFFFFFF
    h = ((c[0] + c[3]) & mask) / mask
    s = ((c[1] + c[3]) & mask) / mask
    l = ((c[2] + c[3]) & mask) / mask
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


_FMT_MAP = {
    "hex": "to_hex",
    "rgb": "to_rgb",
    "rgb_float": "to_rgb_float",
    "hsl": "to_hsl",
    "ansi_fg": "to_ansi_fg",
    "ansi_bg": "to_ansi_bg",
}


def str2col(value, fmt="hex", seed=None, hue_range=(0, 360), sat_range=(0.4, 0.9), light_range=(0.35, 0.65)):
    conv = Str2Col(seed=seed, hue_range=hue_range, sat_range=sat_range, light_range=light_range)
    return getattr(conv, _FMT_MAP[fmt])(value)
