import json
import os
import datetime

from django.conf import settings

from wizer.tools.utils import sanitize, timestamp_format
from django.utils.duration import duration_microseconds


gpx_header = """<?xml version="1.0" encoding="UTF-8"?>
<gpx creator="Fabian Gebhart" version="1.1" xmlns="http://www.topografix.com/GPX/1/1"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd"
xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1"
xmlns:gpxtrkx="http://www.garmin.com/xmlschemas/TrackStatsExtension/v1"
xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"
xmlns:locus="http://www.locusmap.eu">"""


def _gpx_file(time, name, track_points, sport):
    return f"""{gpx_header}
    <metadata>
        <time>{time.strftime(timestamp_format)}</time>
        <link href="https://gitlab.com/fgebhart/workoutizer">
            <text>Workoutizer</text>
        </link>
    </metadata>
    <trk>
        <name>{name}</name>
        <extensions>
            <locus:activity>{sport}</locus:activity>
        </extensions>
        <trkseg>
            {track_points}
        </trkseg>
    </trk>
</gpx>
"""


def _track_points(coordinates: list, timestamps: list):
    track_points = ""
    for c, ts in zip(coordinates, timestamps):
        point = f"""<trkpt lat="{c[1]}" lon="{c[0]}">
                <time>{ts}</time>
            </trkpt>
            """
        track_points += point
    return track_points


def _build_gpx(time, file_name, coordinates: list, timestamps: list, sport: str):
    return _gpx_file(time=time, name=file_name, track_points=_track_points(coordinates, timestamps), sport=sport)


def _fill_list_of_timestamps(start: datetime.date, duration, length: int):
    list_of_timestamps = []
    duration = datetime.timedelta(microseconds=duration_microseconds(duration))
    one_step_of_time = duration / length
    start = datetime.datetime.combine(start, datetime.time(12, 00))
    for i in range(length):
        interval = (start + one_step_of_time * i)
        strftime = interval.strftime(timestamp_format)
        list_of_timestamps.append(strftime)
    return list_of_timestamps


def save_activity_to_gpx_file(activity):
    file_name = f"{activity.date}_{sanitize(activity.name)}.gpx"
    path = os.path.join(settings.MEDIA_ROOT, file_name)
    coordinates = json.loads(activity.trace_file.coordinates)
    file_content = _build_gpx(
        time=activity.date,
        file_name=activity.name,
        coordinates=coordinates,
        timestamps=_fill_list_of_timestamps(start=activity.date, duration=activity.duration, length=len(coordinates)),
        sport=activity.sport.name
    )
    with open(path, "w+") as f:
        f.write(file_content)

    return path
