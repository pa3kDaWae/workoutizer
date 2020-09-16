import os
import datetime

import pytest
import pytz

from wizer.models import Settings, Sport, Activity, Traces, UICacheActivityData
from wizer.file_helper.fit_parser import FITParser
from wizer.file_helper.gpx_parser import GPXParser


@pytest.fixture(scope="module")
def fit_parser():
    test_file_path = os.path.join(os.path.dirname(__file__), "data/example.fit")

    def _pass_path(path=test_file_path):
        return FITParser(path_to_file=path)

    return _pass_path


@pytest.fixture(scope="module")
def gpx_parser():
    test_file_path = os.path.join(os.path.dirname(__file__), "data/example.gpx")

    def _pass_path(path=test_file_path):
        return GPXParser(path_to_file=path)

    return _pass_path


@pytest.fixture
def md5sum():
    return "a64847629ea151cb1270b98d22ce6bb6"


@pytest.fixture
def settings(db):
    settings = Settings(
        path_to_trace_dir="/home/pi/traces/",
        path_to_garmin_device="/home/pi/traces/",
        file_checker_interval=90,
        number_of_days=30,
        reimporter_updates_all=False,
        delete_files_after_import=False,
    )
    settings.save()
    return settings


@pytest.fixture
def sport(db):
    sport = Sport(name='Some Crazy Stuff', color='red', icon='Bike')
    sport.save()
    return sport


@pytest.fixture
def trace_file(db):
    trace = Traces(
        path_to_file='some/path/to/file.gpx',
        file_name='file.gpx',
        md5sum='4c1185c55476269b442f424a9d80d964',
        coordinates_list='[[8.47357001155615, 49.47972273454071], [8.47357001155615, 49.47972273454071]]',
    )
    trace.save()
    return trace


@pytest.fixture
def ui_cache_data(db, dummy_parser):
    parser = dummy_parser()
    ui_data = UICacheActivityData(
        coordinates_list=parser.coordinates_list,
        distance_list=parser.distance_list,
        altitude_list=parser.altitude_list,
        heart_rate_list=parser.heart_rate_list,
        cadence_list=parser.cadence_list,
        speed_list=parser.speed_list,
        temperature_list=parser.temperature_list,
        timestamps_list=parser.timestamps_list,
    )
    ui_data.save()
    return ui_data


@pytest.fixture
def activity(db, sport, trace_file, ui_cache_data):
    activity = Activity(
        name='Running',
        sport=sport,
        date=datetime.datetime(2020, 7, 7, tzinfo=pytz.UTC),
        duration=datetime.timedelta(minutes=30),
        distance=5.2,
        description="some super sport",
        trace_file=trace_file,
        calories=123,
        ui_cache_activity_data=ui_cache_data,
    )
    activity.save()
    return activity


@pytest.fixture
def ip_port():
    return "192.168.0.108:8000"


@pytest.fixture
def wkz_service_path():
    return '/etc/systemd/system/wkz.service'


@pytest.fixture
def wkz_mount_service_path():
    return '/etc/systemd/system/wkz_mount.service'


@pytest.fixture
def udev_rule_dir():
    return '/etc/udev/rules.d'


@pytest.fixture
def udev_rule_path(udev_rule_dir):
    return f'{udev_rule_dir}/device_mount.rules'


@pytest.fixture
def vendor_id():
    return '091e'


@pytest.fixture
def product_id():
    return '4b48'
