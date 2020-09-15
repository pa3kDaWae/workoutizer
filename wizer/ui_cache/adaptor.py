import logging
from wizer.ui_cache.compressor import compress_data_for_ui_cache, ensure_list_attributes_have_same_length


log = logging.getLogger(__name__)


def save_ui_cache_to_model(ui_cache_model, parser):
    if parser.coordinates_list and parser.distance_list and parser.altitude_list and parser.heart_rate_list and \
            parser.cadence_list and parser.speed_list and parser.temperature_list and parser.timestamps_list:
        log.debug(f"saving activity data to ui_cache model")
        parser = ensure_list_attributes_have_same_length(parser=parser)
        parser = compress_data_for_ui_cache(parser=parser)
        ui_cache_object = ui_cache_model(
            coordinates_list=parser.coordinates_list,
            distance_list=parser.distance_list,
            altitude_list=parser.altitude_list,
            heart_rate_list=parser.heart_rate_list,
            cadence_list=parser.cadence_list,
            speed_list=parser.speed_list,
            temperature_list=parser.temperature_list,
            timestamps_list=parser.timestamps_list,
        )
        ui_cache_object.save()
        return ui_cache_object
    else:
        return None
