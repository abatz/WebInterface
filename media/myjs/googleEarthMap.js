var MAPID = "{{ mapid }}";
var TOKEN = "{{ token }}";
var eeMapOptions = {
	getTileUrl: function(tile, zoom) {
		  var url = ['https://earthengine.googleapis.com/map',
			     MAPID, zoom, tile.x, tile.y].join("/");
		  url += '?token=' + TOKEN
		  return url;
	},
	tileSize: new google.maps.Size(256, 256)
};
var mapType = new google.maps.ImageMapType(eeMapOptions);
/*********************************
*    INITIALIZE CALL
********************************* /
function initialize() {
	var center = new google.maps.LatLng(39.5272, -119.8219);
	var mapOptions = {
		  center: center,
		  zoom: 8,
		  maxZoom: 10,
		  streetViewControl: false,
		  mapTypeControl:true,
		  mapTypeId: google.maps.MapTypeId.ROADMAP,
		  clickable:true,
	};

	var map = new google.maps.Map(document.getElementById("map"),
				      mapOptions);
	map.overlayMapTypes.push(mapType);

	//These may not be necessary
	//map = new google.maps.Map($('#map').get(0), mapOptions)
	//map.overlayMapTypes.push(null);
	//map.overlayMapTypes.setAt("0",mapType);

	var marker = new google.maps.Marker({position:new google.maps.LatLng(39.5272,-119.8219),
		     map: map, draggable: true});
	/*********************************
	*     LISTENER
	*********************************/
	google.maps.event.addListener(marker, 'dragend', function(a) {
		  var div = document.createElement('div');
		  var longitude=a.latLng.lng().toFixed(4)
		  var latitude=a.latLng.lat().toFixed(4)
		  document.getElementById('UserLatLong').value = longitude+','+latitude;
	});
}
/*********************************
*    INITIALIZE CALL
*********************************/
google.maps.event.addDomListener(window, 'load', initialize);
window.onload = initialize;
