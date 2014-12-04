   /*********************************
                *     FACTOID INFO BOXES         *
                *********************************/
                    var infowindow = new google.maps.InfoWindow({
                        });
                    window.infomarkers = new Array();

                    function addInfoMarkers(){
                                var locations = [
                              ['{% include "includes/info_wildfire.html"%}',40.6,238],
                              ['{% include "includes/info_agriculture.html"%}',37.2,238.6],
                              ['{% include "includes/info_livestock.html"%}', 37.5,238.4],
                              ['{% include "includes/info_snowpack.html"%}', 37.35,237.7],
                            ];

                            // Setup the different icons and shadows
                            var iconURLPrefix = 'images/';

                            var icons = [
                              iconURLPrefix + 'fire.gif',
                              iconURLPrefix + 'agriculture.gif',
                              iconURLPrefix + 'livestock.gif',
                              iconURLPrefix + 'snow.jpg',
                            ]
                            var icons_length = icons.length;
                            var iconCounter = 0;
                            for (var i = 0; i < locations.length; i++) {
                                infomarker = new google.maps.Marker({
                                position: new google.maps.LatLng(locations[i][1], locations[i][2]),
                                map: map,
                                icon : icons[iconCounter],
                              });
                              window.infomarkers.push(infomarker);
                       }
                addInfoMarkers();

                   function setInfoMarkersMap(map) {
                          for (var i = 0; i < markers.length; i++) {
                            infomarkers[i].setMap(map);
                          }
                        }
                   // Removes the markers from the map, but keeps them in the array.
                   function clearMarkers() {
                          setInfoMarkersMap(null);
                        }

                 google.maps.event.addListener(infomarker, 'click', (function(infomarker, i) {
                        return function() {
                          infowindow.setContent(locations[i][0]);
                          infowindow.open(map, infomarker);
                          infowindow.style.width = "400px";
                          infowindow.style.height = "400px";
                        }
                      })(infomarker, i));

                      iconCounter++;
                      // We only have a limited number of possible icon colors, so we may have to restart the counter
                      if(iconCounter >= icons_length){
                        iconCounter = 0;
                      }
                    }

                    //function AutoCenter() {
                      //  Create a new viewpoint bound
                      //var bounds = new google.maps.LatLngBounds();
                      //  Go through each...
                      //$.each(markers, function (index, marker) {
                //      bounds.extend(marker.position);
                    //  });
                      //  Fit these bounds to the map
                   //   map.fitBounds(bounds);
                    //}
                    //AutoCenter();


