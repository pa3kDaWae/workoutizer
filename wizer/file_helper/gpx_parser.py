import logging

import gpxpy
import gpxpy.gpx

from wizer.gis.gis import calc_distance_of_points
from .lib.parser import Parser

log = logging.getLogger(__name__)


class GPXParser(Parser):
    def __init__(self, path_to_file):
        super(GPXParser, self).__init__(path_to_file)
        self.gpx = None

    def _parse_metadata(self):
        gpx_file = open(self.path_to_file, 'r')
        self.file_name = self.get_file_name_from_path(self.path_to_file)
        self.gpx = gpxpy.parse(gpx_file)
        self._get_sport_from_gpx_file()
        self._get_duration_from_gpx_file()

    def _get_sport_from_gpx_file(self):
        if self.gpx.tracks[0].type:
            self.sport = self.gpx.tracks[0].type
        else:
            for e in self.gpx.tracks[0].extensions:
                if e.tag.split("}")[1] == "activity":
                    self.sport = e.text
                    log.debug(f"found sport: {self.sport}")

    def _get_duration_from_gpx_file(self):
        all_points_time = []
        for s in self.gpx.tracks[0].segments:
            for p in s.points:
                all_points_time.append(p.time)
        start = False
        end = False
        if all_points_time:
            start = all_points_time[0]
            end = all_points_time[-1]
        if start and end:
            self.duration = end - start
            log.debug(f"found duration: {self.duration}")
        else:
            log.debug(f"could not find duration")
        if self.gpx.time:
            self.date = self.gpx.time
            log.debug(f"found date: {self.date}")
        else:
            self.date = start
            log.debug(f"found date: {self.date}")

        if not self.date:
            log.debug(f"could not find date in GPX file, will use OS file created date")
            self.get_file_created_datetime()

    def _parse_records(self):
        for track in self.gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if point.elevation:
                        self.altitude_list.append(point.elevation)
                    self.coordinates_list.append([point.longitude, point.latitude])
        log.debug(f"found number of coordinates: {len(self.coordinates_list)}")
        log.debug(f"found number of elevation points: {len(self.altitude_list)}")
        self.distance = calc_distance_of_points(self.coordinates_list)
        log.debug(f"found distance: {self.distance}")
