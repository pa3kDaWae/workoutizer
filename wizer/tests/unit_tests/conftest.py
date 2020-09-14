import pytest


@pytest.fixture
def dummy_parser():
    return Parser


class Parser:
    def __init__(self):
        self.coordinates_list = [[8.710218, 49.414196], [8.710011, 49.414439], [8.710013, 49.414460]]
        self.distance_list = [0.261, 0.913, 56.981]
        self.altitude_list = [1.234, 4.89, 6.0]
        self.heart_rate_list = [89, 92, 102.9]  # should be ensured to be a list of ints
        self.cadence_list = [0, 4, 5]  # should be ensured to be a list of ints
        self.speed_list = [1.234, 4.89, 6.0, 8.38]  # also have a list with different length, will be trimmed
        self.temperature_list = [24.6, 26., 28]  # should be rounded and casted to ints
        self.timestamps_list = [1568470500.0, 1568470501.0, 1568470502.0]  # should be left untouched


@pytest.fixture
def dummy_list():
    def get_list(length):
        return [i for i in range(0, length)]
    return get_list
