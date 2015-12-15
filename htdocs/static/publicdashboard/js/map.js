    var country='Ethiopia';
    var country_lat='9.0300';
    var country_long='38.7400';

    var cities = new L.LayerGroup();

		L.marker([9.1300, 38.7400]).bindPopup('Something').addTo(cities),
		L.marker([9.6300, 38.8400]).bindPopup('Something Else').addTo(cities),
		L.marker([9.6400, 38.7500]).bindPopup('A place').addTo(cities),
		L.marker([9.3300, 38.200]).bindPopup('Another Place').addTo(cities);


	    var mbAttr = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
				'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
				'Imagery © <a href="http://mapbox.com">Mapbox</a>',
			mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6IjZjNmRjNzk3ZmE2MTcwOTEwMGY0MzU3YjUzOWFmNWZhIn0.Y8bhBaUMqFiPrDRW9hieoQ';

	    var grayscale   = L.tileLayer(mbUrl, {id: 'mapbox.light', attribution: mbAttr}),
		    streets  = L.tileLayer(mbUrl, {id: 'mapbox.streets',   attribution: mbAttr});

		var map = L.map('map', {
			center: [country_lat, country_long],
			zoom: 7,
			layers: [grayscale, cities]
		});

		var baseLayers = {
			"Grayscale": grayscale,
			"Streets": streets
		};

		var overlays = {
			"Cities": cities
		};

		L.control.layers(baseLayers, overlays).addTo(map);
