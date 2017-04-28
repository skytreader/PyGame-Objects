from mock import MagicMock

def make_mock_clock():
    mock_clock = MagicMock()
    mock_clock.tick.return_value = None

    return mock_clock
