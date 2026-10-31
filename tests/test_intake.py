import pytest
from app.core import parse, confirm


@pytest.mark.parametrize(
    "text", ["next Friday", "2030-02-31 at 10:00", "2030-06-17 at 25:00", "2030-06-17 or 2030-06-18 at 10:00"]
)
def test_ambiguous_or_invalid_clarifies(text):
    assert parse(text)["status"] == "clarify"


def test_confirmation_is_not_booking():
    p = parse("2030-06-17 at 09:00")
    assert p["requires_confirmation"] and not p["booked"]
    with pytest.raises(PermissionError):
        confirm(p, "2030-06-17", "09:00")
    assert not confirm(p, "2030-06-17", "09:00", True)["booked"]
