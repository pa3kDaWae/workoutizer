import pytest

from wizer.file_helper.gpx_exporter import gpx_header


@pytest.fixture(scope='session')
def trace_coordinates():
    return [[8.476648433133962, 49.48468884453178], [8.476595375686886, 49.48457719758154],
            [8.47659705206752, 49.48453864082695], [8.47659654915333, 49.48450796306134]]


@pytest.fixture(scope='session')
def trace_coordinates_with_elevation():
    return [[8.476648433133962, 49.48468884453178, 200], [8.476595375686886, 49.48457719758154, 201],
            [8.47659705206752, 49.48453864082695, 202], [8.47659654915333, 49.48450796306134, 203]]


@pytest.fixture(scope='session')
def gpx_string():
    return f"""{gpx_header}
    <metadata>
        <time>2019-07-12T00:00:00Z</time>
        <link href="https://gitlab.com/fgebhart/workoutizer">
            <text>Workoutizer</text>
        </link>
    </metadata>
    <trk>
        <name>test</name>
            <type>Running</type>
        <trkseg>
            <trkpt lat="49.48468884453178" lon="8.476648433133962">
                <time>2019-07-12T12:00:00Z</time>
            </trkpt>
            <trkpt lat="49.48457719758154" lon="8.476595375686886">
                <time>2019-07-12T12:01:00Z</time>
            </trkpt>
            <trkpt lat="49.48453864082695" lon="8.47659705206752">
                <time>2019-07-12T12:02:00Z</time>
            </trkpt>
            <trkpt lat="49.48450796306134" lon="8.47659654915333">
                <time>2019-07-12T12:03:00Z</time>
            </trkpt>
            
        </trkseg>
    </trk>
</gpx>
"""


@pytest.fixture(scope='session')
def gpx_string_with_elevation():
    return f"""{gpx_header}
    <metadata>
        <time>2019-07-12T00:00:00Z</time>
        <link href="https://gitlab.com/fgebhart/workoutizer">
            <text>Workoutizer</text>
        </link>
    </metadata>
    <trk>
        <name>test</name>
            <type>Running</type>
        <trkseg>
            <trkpt lat="49.48468884453178" lon="8.476648433133962">
                <time>2019-07-12T12:00:00Z</time>
                <ele>200</ele>
            </trkpt>
            <trkpt lat="49.48457719758154" lon="8.476595375686886">
                <time>2019-07-12T12:01:00Z</time>
                <ele>201</ele>
            </trkpt>
            <trkpt lat="49.48453864082695" lon="8.47659705206752">
                <time>2019-07-12T12:02:00Z</time>
                <ele>202</ele>
            </trkpt>
            <trkpt lat="49.48450796306134" lon="8.47659654915333">
                <time>2019-07-12T12:03:00Z</time>
                <ele>203</ele>
            </trkpt>
            
        </trkseg>
    </trk>
</gpx>
"""
