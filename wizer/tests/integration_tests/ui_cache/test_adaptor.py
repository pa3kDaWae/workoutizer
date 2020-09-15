from wizer.ui_cache.adaptor import save_ui_cache_to_model
from wizer import models


def test_save_ui_cache_to_model(db, fit_parser):
    parser = fit_parser()
    ui_cache_object = save_ui_cache_to_model(
        ui_cache_model=models.UICacheActivityData,
        parser=parser,
    )
    ui_cache_instance = models.UICacheActivityData.objects.get(pk=ui_cache_object.pk)
    # sanity checks
    assert ui_cache_instance.pk == 1
    assert ui_cache_instance.heart_rate_list.endswith(", 101, 99, 102, 99, 98]")


def test_save_ui_cache_to_model__all_attributes_empty(db, fit_parser):
    parser = fit_parser()

    # test code path where all attributes are empty lists
    parser.coordinates_list = []
    parser.distance_list = []
    parser.altitude_list = []
    parser.heart_rate_list = []
    parser.cadence_list = []
    parser.speed_list = []
    parser.temperature_list = []
    parser.timestamps_list = []

    ui_cache_object = save_ui_cache_to_model(
        ui_cache_model=models.UICacheActivityData,
        parser=parser,
    )

    assert ui_cache_object is None
