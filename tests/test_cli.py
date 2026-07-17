import subprocess
import sys


def run(*args, stdin=None):
    return subprocess.run(
        [sys.executable, "-m", "str2col.cli"] + list(args),
        capture_output=True,
        text=True,
        input=stdin,
    )


def test_cli_hex_output():
    r = run("hello")
    assert r.returncode == 0
    out = r.stdout.strip()
    assert out.startswith("#") and len(out) == 7


def test_cli_rgb_format():
    r = run("hello", "--format", "rgb")
    assert r.returncode == 0
    assert "(" in r.stdout


def test_cli_stdin():
    r = run(stdin="hello\n")
    assert r.returncode == 0
    assert r.stdout.strip().startswith("#")


def test_cli_stdin_matches_arg():
    r_arg = run("hello")
    r_stdin = run(stdin="hello\n")
    assert r_arg.stdout.strip() == r_stdin.stdout.strip()


def test_cli_seed_shifts_color():
    r1 = run("hello", "--seed", "a")
    r2 = run("hello", "--seed", "b")
    assert r1.stdout.strip() != r2.stdout.strip()


def test_cli_hue_range():
    r = run("hello", "--format", "hsl", "--hue-range", "180", "240")
    assert r.returncode == 0


def test_cli_text_option():
    r = run("hello", "--text", "hi")
    assert r.returncode == 0
    assert "\033[38;2;" in r.stdout
    assert "\033[0m" in r.stdout


def test_cli_no_args_no_stdin():
    r = subprocess.run(
        [sys.executable, "-m", "str2col.cli"],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert r.returncode != 0
