	<!-- JQUERY/JQUERY UI/AJAX -->
	<!--<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>-->

	<!-- for date picker calendar -->
	<link rel="stylesheet" href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css">
	<script type="text/javascript" src="//code.jquery.com/ui/1.11.1/jquery-ui.js"></script>

 	<!------------------------------------>
        <!--		MY SCRIPTS           -->
        <!------------------------------------>
	<script type="text/javascript" src="media/myjs/get_colorbar.js"></script> <!-- COLORBAR --> 
	<script type="text/javascript" src="media/myjs/formListener.js"></script> <!-- FORM LISTENER -->
	<script type="text/javascript" src="media/myjs/progressWindow.js"></script> <!-- PROGRESS BAR -->
	<script type="text/javascript" src="media/myjs/zoomStates.js"></script> <!-- ZOOM TO STATE -->
	<script type="text/javascript" src="/media/myjs/colorbar.js"></script><!--DYNAMIC COLORBAR-->
	<script type="text/javascript" src="/media/myjs/colorbrewer.js"></script><!--DYNAMIC COLORBAR-->
	<script type="text/javascript" src="/media/myjs/gmaps_styles.js"></script><!--GMAPS STYLES-->
	{% include 'includes/js_datepicker.html'%}<!--DATE PICKER-->
 	<!------------------------------------>
        <!-	GOOGLE EARTH MAP SCRIPTS    -->
        <!------------------------------------>
	<!- for layer control on map -->
	<!--<script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>-->

	<script src="https://maps.googleapis.com/maps/api/js?sensor=true"></script>

	<script type="text/javascript">
	     var MAPID = "{{ mapid }}";
	     var TOKEN = "{{ token }}";
 	     {% if mapid %}
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
	     {% endif %}

	      var map=null;
	      var statemarkerLayer = null;
	      var statemarkerOverLayer = null;
	      var countymarkerOverLayer = null;
	      var climatedivmarkerOverLayer = null;
	      var hucsmarkerOverLayer = null;
	      var psasmarkerOverLayer = null;
	      var kmlmarkerOverLayer = null;
	      var myZoom;	
	      var infomarkers;  
	      var timeoutID;


	      /*********************************
	      *    INITIALIZE CALL
	      *********************************/
	      function initialize() {

       		//geocoder = new google.maps.Geocoder();
                var mapCenterLongLat = "{{ mapCenterLongLat}}";
                var mapCenterLat = parseFloat(mapCenterLongLat.split(',')[1]).toFixed(4);
                var mapCenterLong = parseFloat(mapCenterLongLat.split(',')[0]).toFixed(4);

		var myCenter = new google.maps.LatLng(mapCenterLat, mapCenterLong);
		var myZoom ={{ mapzoom }}
		var mapOptions = {
			  center: myCenter,
			  zoom: myZoom,
			  maxZoom: 18,
			  streetViewControl: false,
			  mapTypeControl: true,
			  navigationControl: true, 
			  mapTypeId: google.maps.MapTypeId.TERRAIN,
			  mapTypeControlOptions: {
				style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
				position: google.maps.ControlPosition.TOP_RIGHT
			    },
			  clickable:true,
			  backgroundColor: '#FFFFFF',
			  disableDefaultUI: false,
			  zoomControl: true,
				    zoomControlOptions: {
					style: google.maps.ZoomControlStyle.LARGE,
					position: google.maps.ControlPosition.TOP_LEFT
				    },
			 panControl: false,
				    panControlOptions: {
					position: google.maps.ControlPosition.TOP_RIGHT
				    },
		};
        	map = new google.maps.Map(document.getElementById("map"),mapOptions);

		/*********************************
		*    WHITE GOOGLE MAP            *
		*********************************/
		{% include 'includes/light-political.html'%}
		map.setOptions({styles: lightPoliticalStyles});
		{% if mapid %}
               		window.map.overlayMapTypes.push(mapType);
			window.infomarkers = new Array();
			google.maps.event.addListenerOnce(mapType, 'tilesloaded', function() {
			 //this part runs when the mapobject is created and rendered			
				google.maps.event.addListenerOnce(map, 'idle', function() {
				  //this part runs when the mapobject shown for the first time
					window.clearTimeout(timeoutID);
				});
			});
		{% endif %}
/*
		// Set mouseover event for each feature.
                 google.maps.event.addListener(map,'click', function(event) {
			var lat = event.latLng.lat().toFixed(4);
			var long = event.latLng.lng().toFixed(4);

			function getPointData(lat,long){
                    	//alert("Get Point Value Function ");
                        $.ajax({
                            type: 'POST',
                            url: '/',
			    data:{
				'lat': lat, 
				'long': long, 
				},
                            success: function(){alert('DONE!');},
                            error:function(){alert('ERROR!');},
                    });

                    var pointValue=parseFloat(lat)+parseFloat(long);

                    return pointValue;
                }


			var value=getPointData(lat,long);

			 var infowindow = new google.maps.InfoWindow({});
			 window.infomarkers = new Array();
			 messageString='<b>Value</b>    : '+value+' {{ varUnits }}'+
				'<br><b>Latitude</b>   : '+lat+
				'<br><b>Longitude</b> : '+long+'<br>';
			 var locations = [messageString,lat,long];
			 infomarker = new google.maps.Marker({
                                position: new google.maps.LatLng(locations[1], locations[2]),
                                map: map,
                              });
			 //window.infomarkers.push(infomarker);
			 infowindow.setContent(locations[0]);
			 infowindow.open(map, infomarker);
			 google.maps.event.addListener(infowindow,'closeclick',function(){
			  	infomarker.setMap(null); //removes the marker
			});
                 });
*/
		/*********************************
		*     ZOOM/CENTER CHANGED                   *
		*********************************/
		google.maps.event.addListener(map,'zoom_changed',function(){
		  if(map.getZoom()!= myZoom) {
			document.getElementById('mapzoom').value =map.getZoom();
			myZoom = map.getZoom();
		  }
          //Update default points location to show at new center
          var newCenter = window.map.getCenter();
          myCenterLat = newCenter.lat().toFixed(4);
          myCenterLong = newCenter.lng().toFixed(4);
          var LongLat = String(myCenterLong)+','+String(myCenterLat);
          var latlong = new google.maps.LatLng(myCenterLat,myCenterLong);
          document.getElementById('mapCenterLongLat').value = LongLat;
          $('.point').each(function() {
            point_id = parseFloat($(this).attr('id').split('point')[1]);
            //First point is special
            if (point_id == 1 && $('#p' + String(point_id)).val() == '-112,42'){
                $('#p' + String(point_id)).val(LongLat);
                window.markers[point_id - 1].position = latlong;
            }
            else{ 
                if ($(this).css('display') != 'block'){
                    $('#p' + String(point_id)).val(LongLat);
                    window.markers[point_id - 1].position = latlong;
                }
            }
          });  
		});
		google.maps.event.addListener(map,'center_changed',function(){
			var newCenter = window.map.getCenter();
			myCenterLat = newCenter.lat().toFixed(4);
			myCenterLong = newCenter.lng().toFixed(4);
            var LongLat = String(myCenterLong)+','+String(myCenterLat);
            var latlong = new google.maps.LatLng(myCenterLat,myCenterLong);
			document.getElementById('mapCenterLongLat').value = LongLat;
            //Update default points location to show at new center
            $('.point').each(function() {
                point_id = parseFloat($(this).attr('id').split('point')[1]);
                //First point is special
                if (point_id == 1 && $('#p' + String(point_id)).val() == '-112,42'){
                    $('#p' + String(point_id)).val(LongLat);
                    window.markers[point_id - 1].position = latlong;
                }
                else{ 
                    if ($(this).css('display') != 'block'){
                        $('#p' + String(point_id)).val(LongLat);
                        window.markers[point_id - 1].position = latlong;
                    }
                }
            });    
		});

		/*********************************
		*     COLORBAR                   *
		*********************************/
		colorbarsize = parseInt(document.getElementById('colorbarsize').value);
                colorbarmap = document.getElementById('colorbarmap').value;
                myPalette=colorbrewer[colorbarmap][colorbarsize];
                minColorbar = document.getElementById('minColorbar').value
                maxColorbar = document.getElementById('maxColorbar').value
                myScale = d3.scale.quantile().range(myPalette).domain([minColorbar,maxColorbar]);
                colorbar1 = Colorbar()
                    .thickness(30)
                    .barlength(300)
                    .orient("horizontal")
                    .scale(myScale)
                colorbarObject1 = d3.select("#colorbar1").call(colorbar1)

		var palette = new String();
		palette=myPalette[0].replace(/#/g, '');
		for (var i=1;i<myPalette.length;i++){
			palette = palette+','+myPalette[i].replace(/#/g, '');
		} 
		jQuery('#palette').val(palette);
	
		palette_list = palette.split(",");
                var myPalette = new Array();
                for (var i = 0; i < palette_list.length; i++) {
                        myPalette[i]="#"+palette_list[i];
                }
                myScale = d3.scale.quantile().range(myPalette).domain([{{ minColorbar }},{{ maxColorbar}}])
                colorbar = Colorbar()
                   .thickness(30)
                    .barlength(400)
                    .orient("horizontal")
                    .scale(myScale)
                colorbarObject = d3.select("#colorbar").call(colorbar)
	
		/*********************************
		*      POINTS                    *
		*********************************/
		{% include 'includes/js_points.html'%}

		/*********************************
		*      RECTANGLE                    *
		*********************************/
		{% include 'includes/js_rectangle.html'%}

		/*********************************
		*      STATES                    *
		*********************************/
		window.statemarkerLayer = new google.maps.KmlLayer('http://www.wrcc.dri.edu/monitor/WWDT/KML/states.kmz', {
                map:map,
                    preserveViewport: true,
                    suppressInfoWindows: false
                 }); //end KmlLayer
		 google.maps.event.addListener(statemarkerLayer, 'click', function(kmlEvent) {
                        $('#state').val(kmlEvent.featureData.name);
                	findAddress();
          	}); //end listener
		window.statemarkerLayer.setMap(null);

		/*********************************
		*      OVERLAYS                   *
		*********************************/
		{% include 'includes/js_overlays.html'%}
		/*********************************/
	      }
	      //google.maps.event.addDomListener(window, 'load', initialize);

	      //window.onload = initialize;
	      jQuery(document).ready(initialize);

	</script>
