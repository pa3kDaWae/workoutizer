import logging
import json
import datetime

import numpy as np
import pytz
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool

from django.conf import settings
from wizer.tools.utils import ensure_lists_have_same_length, remove_nones_from_list
from wizer.models import Lap

log = logging.getLogger(__name__)

plot_matrix = {
    "temperature": {
        "color": "OrangeRed",
        "axis": "°C",
        "title": "Temperature",
    },
    "cadence": {
        "color": "MediumSlateBlue",
        "axis": "revolutions/min",
        "title": "Cadence",
    },
    "speed": {
        "color": "darkred",
        "axis": "m/s",
        "title": "Speed",
    },
    "heart_rate": {
        "color": "DarkOrange",
        "axis": "bpm",
        "title": "Heart Rate",
    },
}


def plot_time_series(activity):
    dict_containing_divs_and_scripts = {}
    attributes = activity.trace_file.__dict__
    del attributes["coordinates_list"]
    del attributes["altitude_list"]
    lap_data = Lap.objects.filter(trace=activity.trace_file)
    if lap_data:
        log.debug(f"found some Lap data for {activity}: {lap_data}")

    for attribute, values in attributes.items():
        if attribute.endswith("_list") and attribute != 'timestamps_list':
            values = json.loads(values)
            if values:
                attribute = attribute.replace("_list", "")
                if activity.distance:
                    x_axis = np.arange(0, activity.distance, activity.distance / len(values))
                    p = figure(plot_height=int(settings.PLOT_HEIGHT / 2),
                               sizing_mode='stretch_width', y_axis_label=plot_matrix[attribute]["axis"],
                               x_range=(0, x_axis[-1]))
                    p.xaxis[0].ticker.desired_num_ticks = 10
                    for lap in lap_data:
                        y_pos = lap.distance
                        print(f"y_pos: {y_pos}")
                        p.line([y_pos, y_pos], [min(values)-1, max(values)+1], line_width=10, color='grey')
                        y_pos += lap.distance
                else:
                    timestamps_list = json.loads(attributes["timestamps_list"])
                    x_axis = [datetime.datetime.fromtimestamp(t) for t in timestamps_list]
                    x_axis, values = ensure_lists_have_same_length(x_axis, values)
                    print(f"x_axis: {x_axis}")
                    p = figure(x_axis_type='datetime', plot_height=int(settings.PLOT_HEIGHT / 2),
                               sizing_mode='stretch_width', y_axis_label=plot_matrix[attribute]["axis"])
                    for lap in lap_data:
                        print(f"lap_end: {lap.end_time}")
                        p.line([lap.end_time, lap.end_time], [min(values)-1, max(values)+1], line_width=10, color='grey')
                p.tools = []
                p.toolbar.logo = None
                p.toolbar_location = None
                if attribute == 'cadence':
                    p.scatter(x_axis, values, radius=0.01, fill_alpha=1, color=plot_matrix[attribute]["color"])
                else:
                    p.line(x_axis, values, line_width=2, color=plot_matrix[attribute]["color"])
                hover = HoverTool(
                    tooltips=[(plot_matrix[attribute]['title'], f"@y {plot_matrix[attribute]['axis']}")],
                    mode='vline')
                p.add_tools(hover)
                p.toolbar.logo = None
                p.title.text = plot_matrix[attribute]["title"]

                script, div = components(p)
                name = attribute.replace("_", " ").title()
                dict_containing_divs_and_scripts[name] = {"script": script, "div": div}

    return dict_containing_divs_and_scripts