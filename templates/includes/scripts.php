	<!-- for date picker calendar -->
	<link rel="stylesheet" href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css">
	<script type="text/javascript" src="//code.jquery.com/ui/1.11.1/jquery-ui.js"></script>

 	<!------------------------------------>
        <!--	LISTENERS           -->
        <!------------------------------------>
	<script type="text/javascript" src="media/myjs/formListener.js"></script> 
	<script type="text/javascript" src="media/myjs/formListener_points.js"></script> 
	<script type="text/javascript" src="media/myjs/formListener_colorbar.js"></script> 
	<script type="text/javascript" src="media/myjs/formListener_layers.js"></script> 

 	<!------------------------------------>
        <!--		MY SCRIPTS           -->
        <!------------------------------------>
	<script type="text/javascript" src="media/myjs/get_colorbar.js"></script> <!-- COLORBAR --> 
	<script type="text/javascript" src="media/myjs/progressWindow.js"></script> <!-- PROGRESS BAR -->
	<script type="text/javascript" src="media/myjs/zoomStates.js"></script> <!-- ZOOM TO STATE -->
	<script type="text/javascript" src="/media/myjs/colorbar.js"></script><!--DYNAMIC COLORBAR-->
	<script type="text/javascript" src="/media/myjs/colorbrewer.js"></script><!--DYNAMIC COLORBAR-->
	<script type="text/javascript" src="/media/myjs/gmaps_styles.js"></script><!--GMAPS STYLES-->
	{% include 'includes/js_datepicker.html'%}<!--DATE PICKER-->

	<!--<script type="text/javascript" src="/media/myjs/bootstrap-slider.js"></script>-->
	<!--<script type="text/javascript">
  		var slider = new Slider("#ex8", {
			tooltip: 'always'
		});
	</script>-->
 	<!------------------------------------>
        <!-	GOOGLE EARTH MAP SCRIPTS    -->
        <!------------------------------------>
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
		/*********************************
		*    CLIMO YEARS		*
		*********************************/
        	$('.landsat5').css('display','none');
        	$('.landsat8').css('display','none');
        	$('.modis').css('display','none');
        	$('.gridmet').css('display','none');
        	{% if product=='G'%}
            		$('.gridmet').css('display','inline');
		{% elif product=='5' %}
            		$('.landsat5').css('display','inline');
		{% elif product=='8' %}
            		$('.landsat8').css('display','inline');
		{% elif product=='M' %}
            		$('.modis').css('display','inline');
		{% endif %}

		/*********************************
		*    MAP INITIALIZE  		*
		*********************************/
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
			var dS = new Date($('#dateStart').val()).getTime();
			var dE = new Date($('#dateEnd').val()).getTime();
			var dSClim = $('#yearStartClim').val();
			var dEClim = $('#yearEndClim').val();
			var calc = $('#calculation').val();
			var p_message = 'Processing Request';
			var largeData = dE - dS >= 1 * 365 * 24 * 60 * 60 * 1000;
			var largeClimCalc = dEClim - dSClim >= 10;
			if (calc == 'value'){
			   if (largeData){ 
			       p_message = 'This computation requires a large amount of daily data. ' +
			       'Please be patient while we process your request.';
			   }
			}
			else {
			   if (largeData && largeClimCalc ){
			       p_message = 'This computation requires a large amount of daily data'+
				' and a large climatology calculation. ' +
			       'Please be patient while we process your request.';
			   }else if(largeData){
			       p_message = 'This computation requires a large amount of daily data. ' +
			       'Please be patient while we process your request.';
			   }else if (largeClimCalc){
			       p_message = 'Your request requires a large climatology calculation. ' +
			       'Please be patient while we process your request.';
			   }
			}
			// Show progress bar.
			waitingDialog.show(p_message, {dialogSize: 'sm', progressType: 'warning'});
			// Show the map layer.
			window.map.overlayMapTypes.push(mapType);
			// Once the tiles load, hide the progress bar.
			google.maps.event.addListenerOnce(mapType, 'tilesloaded', function() {
			   waitingDialog.hide();
			});
			// In case it takes more than 30 seconds for the tiles
			// to load, hide the dialog after 30 seconds anyway.
			setTimeout(function () {
			   waitingDialog.hide();
			}, 30000);
		{% endif %}
/*
        //This is for the potential mouseover event on the google map layer executing a POST call to get value
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
		  var newCenter = window.map.getCenter();
          myCenterLat = newCenter.lat().toFixed(4);
          myCenterLong = newCenter.lng().toFixed(4);
          var LongLat = String(myCenterLong)+','+String(myCenterLat);
          var latlong = new google.maps.LatLng(myCenterLat,myCenterLong);
          if(map.getZoom()!= myZoom) {
			document.getElementById('mapzoom').value =map.getZoom();
			myZoom = map.getZoom();
		  }
          //Update default points location to show at new center
          document.getElementById('mapCenterLongLat').value = LongLat;
          $('.point').each(function() {
            point_id = parseFloat($(this).attr('id').split('point')[1]);
            //First point is special
            if (point_id == 1 && $('#tabtimeseriesoptions').css('display') == 'none'){
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
          //Update sharelink
          var sL = document.getElementById('sL').value;
          var sL_new = sL.replace(/mapzoom=\d+/m,'mapzoom=' + String(myZoom));
          sL_new = sL_new.replace(/mapCenterLongLat=([\-\d.]+),([\d.]+)/m,'mapCenterLongLat=' + LongLat);
          document.getElementById('shareLink').value = sL_new;
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
                if (point_id == 1 && $('#tabtimeseriesoptions').css('display') == 'none'){
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
            //Update sharelink
            var sL = document.getElementById('sL').value;
            var sL_new = sL.replace(/mapCenterLongLat=([\-\d.]+),([\d.]+)/m,'mapCenterLongLat=' + LongLat);
            document.getElementById('shareLink').value = sL_new;
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
		*      LAYERS                    *
		*********************************/
		{% include 'includes/js_points.html'%}    //points
		{% include 'includes/js_rectangle.html'%} //rectangle
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
		{% include 'includes/js_overlays.html'%} //kml
		/*********************************/
	      }
	      //google.maps.event.addDomListener(window, 'load', initialize);

	      //window.onload = initialize;
	      jQuery(document).ready(initialize);

	</script>
