#bateria de pruebas unitarias para portus_data.py

from unittest.mock import Mock, patch

import pandas as pd

from src.portus_data import URL_PORTUS, get_portus_current_data


def test_get_portus_current_data_returns_current_data_as_dataframe():
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
	response = Mock()
	response.json.return_value = payload

	with patch("src.portus_data.requests.get", return_value=response) as get:
		result = get_portus_current_data()

	expected = pd.DataFrame(payload["datos"])
	expected.insert(0, "fecha", payload["fecha"])

	get.assert_called_once_with(URL_PORTUS)
	response.raise_for_status.assert_called_once_with()
	pd.testing.assert_frame_equal(result, expected)
