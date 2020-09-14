import os
import datetime
import json

import pytz

from wizer import models
from wizer.apps import map_sport_name, sport_naming_map, _was_runserver_triggered, parse_and_save_to_model
from wizer.file_helper.initial_data_handler import insert_settings_and_sports_to_model


def test_map_sport_name():
    assert map_sport_name('running', sport_naming_map) == "Jogging"
    assert map_sport_name('Running', sport_naming_map) == "Jogging"
    assert map_sport_name('swim', sport_naming_map) == "Swimming"
    assert map_sport_name('SUP', sport_naming_map) == "unknown"


def test__was_runserver_triggered():
    args = ['runserver']
    assert _was_runserver_triggered(args) is True
    args = ['runserver', 'help']
    assert _was_runserver_triggered(args) is False
    args = ['manage', 'runserver 0.0.0.0:8000 --noreload']
    assert _was_runserver_triggered(args) is True


def test_parse_and_save_to_model(db, md5sum):
    # insert initial sports
    insert_settings_and_sports_to_model(settings_model=models.Settings, sport_model=models.Sport)
    assert len(list(models.Sport.objects.all())) > 0
    assert len(list(models.Settings.objects.all())) > 0

    trace_file_instance = parse_and_save_to_model(
        models=models,
        md5sum=md5sum,
        trace_file=os.path.join(os.path.dirname(__file__), "data/example.fit"),
        importing_demo_data=False,
    )
    # assert activity attributes
    assert models.Activity.objects.get().pk == 1
    assert models.Activity.objects.get().name == 'example'
    assert models.Activity.objects.get().distance == 5.84
    assert models.Activity.objects.get().aerobic_training_effect == 2.7
    assert models.Activity.objects.get().anaerobic_training_effect == 0.3
    assert models.Activity.objects.get().calories == 432
    assert models.Activity.objects.get().description is None
    assert models.Activity.objects.get().duration == datetime.timedelta(seconds=3164)
    assert models.Activity.objects.get().sport.name == 'Jogging'
    assert models.Activity.objects.get().date == datetime.datetime(2019, 9, 14, 15, 22, tzinfo=pytz.UTC)
    assert models.Activity.objects.get().is_demo_activity is False
    # assert trace file attributes
    assert models.Traces.objects.get().pk == 1
    assert models.Traces.objects.get().path_to_file.endswith("wizer/tests/integration_tests/data/example.fit")
    assert models.Traces.objects.get().file_name == "example.fit"
    assert models.Traces.objects.get().md5sum == "a64847629ea151cb1270b98d22ce6bb6"
    assert models.Traces.objects.get().coordinates_list.endswith(", [8.695240924134852, 49.40735740587116]]")
    assert models.Traces.objects.get().distance_list.endswith(", 5836.31, 5839.77]")
    assert models.Traces.objects.get().altitude_list.endswith(", 238.3, 238.3, 238.3]")
    assert models.Traces.objects.get().max_altitude == 353.3
    assert models.Traces.objects.get().min_altitude == 238.2
    assert models.Traces.objects.get().heart_rate_list.endswith(", 101, 99, 102, 99, 98]")
    assert models.Traces.objects.get().avg_heart_rate == 130
    assert models.Traces.objects.get().max_heart_rate == 160
    assert models.Traces.objects.get().min_heart_rate == 95
    assert models.Traces.objects.get().cadence_list.endswith(", 53, 53, 53, 52, 52, 52]")
    assert models.Traces.objects.get().avg_cadence == 64
    assert models.Traces.objects.get().max_cadence == 116
    assert models.Traces.objects.get().min_cadence == 0
    assert models.Traces.objects.get().speed_list.endswith(", 1.344, 1.344, 1.353, 1.344, 1.325]")
    assert models.Traces.objects.get().avg_speed == 1.845
    assert models.Traces.objects.get().max_speed == 3.57
    assert models.Traces.objects.get().min_speed == 0.0
    assert models.Traces.objects.get().temperature_list.endswith(", 26, 26, 26, 26, 26, 26]")
    assert models.Traces.objects.get().avg_temperature == 27
    assert models.Traces.objects.get().max_temperature == 31
    assert models.Traces.objects.get().min_temperature == 26
    assert models.Traces.objects.get().timestamps_list.endswith(", 1568470500.0, 1568470500.0]")
    # assert ui cache attributes
    assert models.UICacheActivityData.objects.get().pk == 1
    assert models.UICacheActivityData.objects.get().coordinates_list.endswith(", [8.6952, 49.4074]]")
    assert models.UICacheActivityData.objects.get().distance_list.endswith(", 5836.31, 5839.77]")
    assert models.UICacheActivityData.objects.get().altitude_list.endswith(", 238.3, 238.3, 238.3]")
    assert models.UICacheActivityData.objects.get().heart_rate_list.endswith(", 101, 99, 102, 99, 98]")
    assert models.UICacheActivityData.objects.get().cadence_list.endswith(", 53, 53, 53, 52, 52, 52]")
    assert models.UICacheActivityData.objects.get().speed_list.endswith(", 1.3, 1.3, 1.4, 1.3, 1.3]")
    assert models.UICacheActivityData.objects.get().temperature_list.endswith(", 26, 26, 26, 26, 26]")
    assert models.UICacheActivityData.objects.get().timestamps_list.endswith(", 1568470500.0, 1568470500.0]")
    # assert for correct foreign keys
    assert models.Activity.objects.get().trace_file.pk == 1
    assert models.Activity.objects.get().ui_cache_activity_data.pk == 1
    # ensure loading list attributes from string to list works
    assert type(json.loads(models.UICacheActivityData.objects.get().coordinates_list)) == list
    assert type(json.loads(models.Traces.objects.get().heart_rate_list)) == list
