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
	<script type="text/javascript" src="media/myjs/showLoadingImage.js"></script> <!-- PROGRESS BAR -->
	<script type="text/javascript" src="media/myjs/zoomStates.js"></script> <!-- ZOOM TO STATE -->
	<script type="text/javascript" src="/media/myjs/colorbar.js"></script><!--DYNAMIC COLORBAR-->
	<script type="text/javascript" src="/media/myjs/colorbrewer.js"></script><!--DYNAMIC COLORBAR-->
	<script type="text/javascript" src="/media/myjs/gmaps_styles.js"></script><!--GMAPS STYLES-->
	{% include 'includes/js_datepicker.html'%}<!--DATE PICKER-->
	
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
	      /*********************************
	      *    INITIALIZE CALL
	      *********************************/
	      function initialize() {

       		geocoder = new google.maps.Geocoder();
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
			  mapTypeId: google.maps.MapTypeId.ROADMAP,
			  mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
			  clickable:true,
			  backgroundColor: '#FFFFFF',
			  //disableDefaultUI: true,
		};
        	map = new google.maps.Map(document.getElementById("map"),mapOptions);

		/*********************************
		*    WHITE GOOGLE MAP            *
		*********************************/
		{% include 'includes/light-political.html'%}
		map.setOptions({styles: lightPoliticalStyles});
		{% if mapid %}
               		window.map.overlayMapTypes.push(mapType);
		{% endif %}

		/*********************************
		*     ZOOM/CENTER CHANGED                   *
		*********************************/
		google.maps.event.addListener(map,'zoom_changed',function(){
		  if(map.getZoom()!= myZoom) {
			document.getElementById('mapzoom').value =map.getZoom();
			myZoom = map.getZoom();
		  }
		});
		google.maps.event.addListener(map,'center_changed',function(){
			newCenter = window.map.getCenter();
			myCenterLat = newCenter.lat().toFixed(4);
			myCenterLong = newCenter.lng().toFixed(4);
			document.getElementById('mapCenterLongLat').value =String(myCenterLat)+','+String(myCenterLong);
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
	      window.onload = initialize;

	</script>
