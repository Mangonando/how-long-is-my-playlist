from project import (
    calculate_adjusted_duration,
    calculate_crossfade_loss,
    calculate_total_seconds,
    format_duration,
)


def test_calculate_total_seconds():
    assert calculate_total_seconds(0, 48, 17) == 2897


def test_calculate_crossfade_loss():
    assert calculate_crossfade_loss(1, 12) == 0


def test_calculate_adjusted_duration():
    assert calculate_adjusted_duration(2897, 13, 12) == 2753


def test_format_duration():
    assert format_duration(3600) == "1:00:00"
