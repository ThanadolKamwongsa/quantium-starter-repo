from dash.testing.application_runners import import_app


def test_header_is_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1", timeout=10)
    header = dash_duo.find_element("h1")
    assert "Soul Foods" in header.text
    assert "Pink Morsel" in header.text


def test_visualisation_is_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    assert dash_duo.find_element("#sales-line-chart") is not None


def test_region_picker_is_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    radio = dash_duo.find_element("#region-filter")
    assert radio is not None
    for region in ("north", "east", "south", "west", "all"):
        assert region in radio.text.lower()
