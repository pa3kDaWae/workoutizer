from itertools import combinations

import pytest

from wizer.ui_cache.compressor import _compress_coordinates, _compress_list_of_floats, _ensure_list_of_ints, \
    compress_data_for_ui_cache, ensure_list_attributes_have_same_length, _compress_list_length


def test__compress_coordinates():
    coordinates = [[8.710218, 49.414196], [8.710011, 49.414439]]
    expected = [[8.7102, 49.4142], [8.7100, 49.4144]]
    result = _compress_coordinates(coordinates=coordinates, decimals=4)
    assert expected == result


def test__compress_list_of_floats():
    list_of_floats = [0.261, 0.913, 56.981]

    expected = [0.3, 0.9, 57.0]
    result = _compress_list_of_floats(input_list=list_of_floats, decimals=1)
    assert expected == result

    expected = [0.26, 0.91, 56.98]
    result = _compress_list_of_floats(input_list=list_of_floats, decimals=2)
    assert expected == result


def test__ensure_list_of_ints():
    list_of_floats = [1.234, 4.89, 6.0]
    expected = [1, 4, 6]
    result = _ensure_list_of_ints(input_list=list_of_floats)
    assert expected == result


def test_compress_data_for_ui_cache(dummy_parser):
    parser = dummy_parser()
    parser = compress_data_for_ui_cache(parser=parser)

    assert parser.coordinates_list == [[8.7102, 49.4142], [8.7100, 49.4144], [8.7100, 49.4145]]
    assert parser.distance_list == [0.26, 0.91, 56.98]
    assert parser.altitude_list == [1.2, 4.9, 6.0]
    assert parser.heart_rate_list == [89, 92, 102]   # was ensured to be a list of ints
    assert parser.cadence_list == [0, 4, 5]     # was not changed
    assert parser.speed_list == [1.2, 4.9, 6.0, 8.4]
    assert parser.temperature_list == [25., 26., 28.]
    assert type(parser.temperature_list[0]) == int
    assert parser.timestamps_list == [1568470500.0, 1568470501.0, 1568470502.0]     # was not changed


def test_ensure_list_attributes_have_same_length(dummy_parser):
    parser = dummy_parser()
    result_parser = ensure_list_attributes_have_same_length(parser=parser)
    list_attributes = []
    for attribute, value_list in result_parser.__dict__.items():
        if attribute.endswith("_list"):
            list_attributes.append(value_list)

    for combination in combinations(list_attributes, 2):
        assert len(combination[0]) == len(combination[1])


def test_ensure_list_attributes_have_same_length__with_empty_lists(dummy_parser):
    parser = dummy_parser()
    parser.cadence_list = []
    parser.speed_list = []
    result_parser = ensure_list_attributes_have_same_length(parser=parser)
    list_attributes = []
    for attribute, value_list in result_parser.__dict__.items():
        if attribute.endswith("_list"):
            list_attributes.append(value_list)

    for combination in combinations(list_attributes, 2):
        if combination[0] and combination[1]:
            assert len(combination[0]) == len(combination[1])

    for value in list_attributes:
        if value:
            assert len(value) > 0
        else:
            assert value is None


def test__compress_list_length(dummy_list):
    list20 = dummy_list(length=20)
    assert len(_compress_list_length(input_list=list20, desired_length=0)) == 0
    assert len(_compress_list_length(input_list=list20, desired_length=10)) == 10
    assert len(_compress_list_length(input_list=list20, desired_length=20)) == 20
    with pytest.raises(ValueError):
        assert len(_compress_list_length(input_list=list20, desired_length=30))
    list30 = dummy_list(length=30)
    assert len(_compress_list_length(input_list=list30, desired_length=10)) == 10
    list40 = dummy_list(length=40)
    assert len(_compress_list_length(input_list=list40, desired_length=10)) == 10
    list50 = dummy_list(length=50)
    assert len(_compress_list_length(input_list=list50, desired_length=10)) == 10
    list500 = dummy_list(length=500)
    assert len(_compress_list_length(input_list=list500, desired_length=10)) == 10
    list50 = dummy_list(length=50)
    assert len(_compress_list_length(input_list=list50, desired_length=9)) == 9
    list18 = dummy_list(length=18)
    assert len(_compress_list_length(input_list=list18, desired_length=15)) == 15
    assert len(_compress_list_length(input_list=list20, desired_length=15)) == 15
    assert len(_compress_list_length(input_list=list30, desired_length=15)) == 15
    assert len(_compress_list_length(input_list=list500, desired_length=19)) == 19
    list4872 = dummy_list(length=4872)
    assert len(_compress_list_length(input_list=list4872, desired_length=547)) == 547
    custom_list = [1.234, 4.89, 6.0, 8.38]
    assert len(_compress_list_length(input_list=custom_list, desired_length=3)) == 3





