#bateria de pruebas unitarias para portus_data.py

import pandas as pd

from src.portus_data import URL_PORTUS, get_portus_current_data


def test_get_portus_current_data_returns_current_data_as_dataframe(monkeypatch):
	payload = {
		"fecha": "2026-09-03 15:00:00.0",
		"datos": [
			{
				"id": 38,
				"nombreParametro": "Temperatura del Agua",
				"nombreColumna": "ts2",
				"paramEseoo": "WaterTemp",
				"valor": "2914",
				"factor": 100.0,
				"unidad": "ºC",
				"paramQC": False,
				"variable": "WATER_TEMP",
				"averia": False,
			},
			{
				"id": 18,
				"nombreParametro": "Latitud",
				"nombreColumna": "lat",
				"paramEseoo": "Latitude",
				"valor": "39.563354",
				"factor": 1.0,
				"unidad": "º",
				"paramQC": False,
				"variable": "",
				"averia": False,
			},
		],
	}

	class DummyResponse:
		def raise_for_status(self):
			return None

		def json(self):
			return payload

	post_arguments = {}

	def fake_post(url, headers, params, json):
		post_arguments.update(
			url=url,
			headers=headers,
			params=params,
			json=json,
		)
		return DummyResponse()

	monkeypatch.setattr("src.portus_data.requests.post", fake_post)

	result = get_portus_current_data(station=2820)

	expected = pd.DataFrame(payload["datos"])
	expected.insert(0, "fecha", payload["fecha"])
	expected.insert(1, "station", 2820)

	assert post_arguments == {
		"url": f"{URL_PORTUS}/2820",
		"headers": {
			"Accept": "application/json",
			"Content-Type": "application/json",
		},
		"params": {"locale": "es"},
		"json": ["WATER_TEMP"],
	}
	pd.testing.assert_frame_equal(result, expected)
