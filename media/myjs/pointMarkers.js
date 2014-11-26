/******************************************
 *   getMarkerUniqueId
 * Concatenates given lat and lng with an underscore and returns it.
 * This id will be used as a key of marker to cache the marker in markers object.
 * @param {!number} lat Latitude.
 * @param {!number} lng Longitude.
 * @return {string} Concatenated marker id.
 *****************************************/
var getMarkerUniqueId = function (lat, lng) {
    return lat + '_' + lng;
}
/******************************************
 *   getLatLng 
 * Creates an instance of google.maps.LatLng by given lat and lng values and returns it.
 * This function can be useful for getting new coordinates quickly.
 * @param {!number} lat Latitude.
 * @param {!number} lng Longitude.
 * @return {google.maps.LatLng} An instance of google.maps.LatLng object
 *****************************************/
var getLatLng = function (lat, lng) {
    return new google.maps.LatLng(lat, lng);
};
/******************************************
 *    addMarker
 * Binds click event to given map and invokesvar lat_lng;
    a callback that appends a new marker to clicked location.
*****************************************/
var lat,lng,lat_lng_string,v,v_list,lat_lng,new_lat_lng_string;
var addMarker = google.maps.event.addListener(map, 'click', function (e) {
    lat = e.latLng.lat(); // lat of clicked point
    lng = e.latLng.lng(); // lng of clicked point
    lat_lng_string = (Math.round(lat*1000) / 1000).toString() + ',' + (Math.round(lng*1000) / 1000).toString();
    //Set lat_lng_string hidden var
    v = document.getElementById('lat_lng_string').value;
    if (v != ''){v+=','}
    v+= lat_lng_string;
    document.getElementById('lat_lng_string').value = v;
    var markerId = getMarkerUniqueId(lat, lng); // an that will be used to cache this marker in markers object.
    var marker = new google.maps.Marker({
	position: getLatLng(lat, lng),
	map: map,
	id: 'marker_' + markerId,
	lat_lon_string:lat_lng_string
    });
    //marker.lat_lon_str = lat + ',' + lng;
    markers[markerId] = marker; // cache marker in markers object
    bindMarkerEvents(marker); // bind right click event to marker
    console.log(markers);

});
/******************************************
 *    bindMarkerEvents
 * Binds right click event to given marker and invokes a callback function that will remove the marker from map.
 * @param {!google.maps.Marker} marker A google.maps.Marker instance that the handler will binded.
*****************************************/
var bindMarkerEvents = function (marker) {
    google.maps.event.addListener(marker, "click", function (point) {
	var markerId = getMarkerUniqueId(point.latLng.lat(), point.latLng.lng()); // get marker id by using clicked point's coordinate
	var marker = markers[markerId]; // find marker
	//Remove lat lng from lat_lng_str
	v = document.getElementById('lat_lng_string').value;
	v_list = v.split(',');
	new_lat_lng_string ='';
	for (idx=0;idx< v_list.length - 1;idx+=2){
	    lat_lng = v_list[idx] + ',' + v_list[idx+1];
	    if (marker.lat_lon_string != lat_lng){
		new_lat_lng_string+=lat_lng + ',';
	    }
	}
	//Remove trailing comma
	new_lat_lng_string = new_lat_lng_string.substring(0,new_lat_lng_string.length - 1);
	document.getElementById('lat_lng_string').value = new_lat_lng_string;
	removeMarker(marker, markerId); // remove it
	console.log(markers);
    });
};
/******************************************
 *    removeMarker
 * Removes given marker from map.
 * @param {!google.maps.Marker} marker A google.maps.Marker instance that will be removed.
 * @param {!string} markerId Id of marker.
*****************************************/
var removeMarker = function (marker, markerId) {
    marker.setMap(null); // set markers setMap to null to remove it from map
    delete markers[markerId]; // delete marker instance from markers object
};
