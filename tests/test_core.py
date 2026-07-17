import re
import pytest
from str2col import Str2Col, str2col

HEX_RE = re.compile(r"^#[0-9a-f]{6}$")


def test_to_hex_returns_hex_string():
    assert HEX_RE.match(Str2Col().to_hex("hello"))


def test_to_hex_is_deterministic():
    conv = Str2Col()
    assert conv.to_hex("hello") == conv.to_hex("hello")


def test_different_inputs_give_different_colors():
    conv = Str2Col()
    assert conv.to_hex("hello") != conv.to_hex("world")


def test_seed_shifts_color():
    assert Str2Col(seed="a").to_hex("hello") != Str2Col(seed="b").to_hex("hello")


def test_seed_is_deterministic():
    assert Str2Col(seed="x").to_hex("hello") == Str2Col(seed="x").to_hex("hello")


def test_to_rgb_returns_int_tuple_in_range():
    r, g, b = Str2Col().to_rgb("hello")
    assert all(isinstance(v, int) for v in (r, g, b))
    assert all(0 <= v <= 255 for v in (r, g, b))


def test_to_rgb_float_returns_float_tuple_in_range():
    r, g, b = Str2Col().to_rgb_float("hello")
    assert all(isinstance(v, float) for v in (r, g, b))
    assert all(0.0 <= v <= 1.0 for v in (r, g, b))


def test_to_hsl_respects_custom_ranges():
    conv = Str2Col(hue_range=(180, 240), sat_range=(0.5, 0.7), light_range=(0.4, 0.6))
    hue, sat, light = conv.to_hsl("hello")
    assert 180 <= hue <= 240
    assert 0.5 <= sat <= 0.7
    assert 0.4 <= light <= 0.6


def test_to_hsl_default_ranges():
    hue, sat, light = Str2Col().to_hsl("hello")
    assert 0 <= hue <= 360
    assert 0.4 <= sat <= 0.9
    assert 0.35 <= light <= 0.65


def test_to_ansi_fg_format():
    result = Str2Col().to_ansi_fg("hello")
    assert result.startswith("\033[38;2;")
    assert result.endswith("m")


def test_to_ansi_bg_format():
    result = Str2Col().to_ansi_bg("hello")
    assert result.startswith("\033[48;2;")
    assert result.endswith("m")


def test_ansi_fg_no_reset():
    assert "\033[0m" not in Str2Col().to_ansi_fg("hello")


def test_ansi_bg_no_reset():
    assert "\033[0m" not in Str2Col().to_ansi_bg("hello")


def test_non_string_inputs():
    conv = Str2Col()
    assert HEX_RE.match(conv.to_hex(42))
    assert HEX_RE.match(conv.to_hex(3.14))
    assert HEX_RE.match(conv.to_hex(None))


def test_str2col_default_returns_hex():
    assert HEX_RE.match(str2col("hello"))


def test_str2col_matches_class():
    assert str2col("hello") == Str2Col().to_hex("hello")


def test_str2col_fmt_rgb():
    result = str2col("hello", fmt="rgb")
    assert isinstance(result, tuple) and len(result) == 3


def test_str2col_fmt_hsl():
    hue, sat, light = str2col("hello", fmt="hsl")
    assert 0 <= hue <= 360


def test_str2col_with_seed():
    assert str2col("hello", seed="x") != str2col("hello", seed="y")


def test_str2col_invalid_fmt():
    with pytest.raises(KeyError):
        str2col("hello", fmt="invalid")
