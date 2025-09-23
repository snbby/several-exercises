import pytest

from license_plate_problem import code6_seq


def test_license_plate_problem():
    assert code6_seq(0) == "000000"
    assert code6_seq(999_999) == "999999"

    # After 999999:
    assert code6_seq(1_000_000) == "00000A"
    assert code6_seq(1_000_001) == "00001A"
    assert code6_seq(1_000_000 + 99_999) == "99999A"
    assert code6_seq(1_000_000 + 100_000) == "00000B"

    assert code6_seq(1_000_000 + 26*100_000 - 1) == "99999Z"
    assert code6_seq(1_000_000 + 26*100_000) == "0000AA"
    assert code6_seq(1_000_000 + 26*100_000 + 1) == "0001AA"

    assert code6_seq(501_363_135) == "ZZZZZZ"

    with pytest.raises(ValueError):
        code6_seq(501_363_135 + 1)

    with pytest.raises(ValueError):
        code6_seq(-1)

