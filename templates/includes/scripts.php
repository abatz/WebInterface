	<!-- JQUERY/JQUERY UI/AJAX -->
	<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

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
	<!--<script type="text/javascript" src="/media/myjs/bootstrap-slider.js"></script>--><!--TRANSPARENCY SLIDER-->
	<script type="text/javascript">
		function setCenter(){
			var newCenter = window.map.getCenter();
			var newLat = newCenter.lat().toFixed(4);
			var newLong = newCenter.lng().toFixed(4);
                       document.getElementById('mapCenterLongLat').value =String(newLong)+','+String(newLat);
		};
	</script>
	
	<script type="text/javascript"> 
		$(function(){
		    $( "#dateStartTS" ).datepicker({
		      changeMonth: true,
		      changeYear: true,
		      numberOfMonths: 3,
		      minDate: "1979-01-01",
		      //minDate: {{ minDate }}, #need to fix.. to be dependent on dataset selected
		      maxDate: "-1d",
		      dateFormat: "yy-mm-dd",
		      onClose: function( selectedDate ) {
			$( ".dateEnd" ).datepicker( "option", "minDate", selectedDate );
			document.getElementById('dateStart').value =document.getElementById('dateStartTS').value;
		      }
		  }).datepicker('setDate', "{{ dateStart }}");
		 $( "#dateEndTS" ).datepicker({
		      changeMonth: true,
		      changeYear: true,
		      numberOfMonths: 3,
		      minDate: "1979-01-01",
		      //minDate: {{ minDate }}, #need to fix.. to be dependent on dataset selected
		      maxDate: "-1d",
		      dateFormat: "yy-mm-dd",
		      onClose: function( selectedDate ) {
			$( ".dateStart" ).datepicker( "option", "maxDate", selectedDate );
			document.getElementById('dateEnd').value =document.getElementById('dateEndTS').value;
			}
		}).datepicker('setDate', '{{ dateEnd }}');
	});
 		$(function(){
                    $( "#dateStart" ).datepicker({
                      changeMonth: true,
                      changeYear: true,
                      numberOfMonths: 3,
                      minDate: "1979-01-01",
                      //minDate: {{ minDate }}, #need to fix.. to be dependent on dataset selected
                      maxDate: "-1d",
                      dateFormat: "yy-mm-dd",
                      onClose: function( selectedDate ) {
                        $( ".dateEnd" ).datepicker( "option", "minDate", selectedDate );
                        document.getElementById('dateStartTS').value =document.getElementById('dateStart').value;
                      }
                  }).datepicker('setDate', "{{ dateStart }}");
                 $( "#dateEnd" ).datepicker({
                      changeMonth: true,
                      changeYear: true,
                      numberOfMonths: 3,
                      minDate: "1979-01-01",
                      //minDate: {{ minDate }}, #need to fix.. to be dependent on dataset selected
                      maxDate: "-1d",
                      dateFormat: "yy-mm-dd",
                      onClose: function( selectedDate ) {
                        $( ".dateStart" ).datepicker( "option", "maxDate", selectedDate );
                        document.getElementById('dateEndTS').value =document.getElementById('dateEnd').value;
                        }
                }).datepicker('setDate', '{{ dateEnd }}');
        });

	</script>
	
 	<!------------------------------------>
        <!-	GOOGLE EARTH MAP SCRIPTS    -->
        <!------------------------------------>
	<script src="https://maps.googleapis.com/maps/api/js?sensor=true"></script>

<script type="text/javascript">
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

	      var map=null;
	      var statemarkerLayer = null;
	      var statemarkerOverLayer = null;
	      var countymarkerOverLayer = null;
	      var climatedivmarkerOverLayer = null;
	      var hucsmarkerOverLayer = null;
	      var psasmarkerOverLayer = null;
	      var kmlmarkerLayer = null;
	      var myZoom;	
	      var infomarkers;
	      var mapOnStyles;
	      var mapOffStyles;
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
		var mapOffStyles = [
		  {
		    featureType: "all",
		    stylers: [
		      { visibility: "off" }]
		    }];
		 var mapOnStyles = [
                  {
                    featureType: "all",
                    stylers: [
                      { visibility: "on" }]
                    }];
        	map = new google.maps.Map(document.getElementById("map"),mapOptions);
		{% if background =="whitebackground" %}
		map.setOptions({styles: mapOffStyles});
		{% endif %}
		//map.setOptions({styles: mapOnStyles});

 		function showNewRect(event) {
                    var ne = rectangle.getBounds().getNorthEast();
                    var sw = rectangle.getBounds().getSouthWest();
                    document.getElementById('NELat').value = ne.lat().toFixed(4);
                    document.getElementById('NELong').value = ne.lng().toFixed(4);
                    document.getElementById('SWLat').value = sw.lat().toFixed(4);
                    document.getElementById('SWLong').value = sw.lng().toFixed(4);
                }

		/*********************************
		*     ZOOM/CENTER CHANGED                   *
		*********************************/
		google.maps.event.addListener(map,'zoom_changed',function(){
		  if(map.getZoom()!= myZoom) {
			document.getElementById('mapzoom').value =map.getZoom();
			myZoom = map.getZoom();
		  }
		});
		/* does not work... too often updates 
		google.maps.event.addListener(map,'center_changed',function(){
			var mapCenterLongLat = "{{ mapCenterLongLat}}";
                	var mapCenterLat = parseFloat(mapCenterLongLat.split(',')[1]).toFixed(4);
                	var mapCenterLong = parseFloat(mapCenterLongLat.split(',')[0]).toFixed(4);
			newCenter = window.map.getCenter();
			myCenterLat = newCenter.lat().toFixed(4);
			myCenterLong = newCenter.lon().toFixed(4);
			document.getElementById('mapCenterLongLat').value =string(myCenterLat)+','+string(myCenterLong);
		});*/

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
		var bounds = new google.maps.LatLngBounds();
		var timeSeriesGraphData = "{{ timeSeriesGraphData }}";
		var domainType = document.getElementById('domainType').value;

		var latlong, markers = [];
		//Set initial markers as invisible
		$('.pointCheck[type=checkbox]').each(function() {
		    var point_id = $(this).val();
		    var LongLat = String($('#' + String(point_id)).val()).replace(' ','');
		    var Long = parseFloat(LongLat.split(',')[0]);
		    var Lat = parseFloat(LongLat.split(',')[1]);
		    var latlon = new google.maps.LatLng(Lat,Long);
		    var marker_img = document.getElementById('img' + String(point_id)).src;
		    var marker = new google.maps.Marker({
			map: map,
			position: latlon,
			title:String(point_id),
			draggable:true,
			visible:false,
			icon: marker_img
		    });
		    //Assign point_id to marker for tracking
		    marker.id = point_id;
		    google.maps.event.addListener(marker, 'click', function() {
			//Uncheck checkbox
			var m_id = marker.id;
			$('#check' + String(point_id)).attr('checked', false);
			//Hide marker
			marker.setVisible(false);
		    });
		    google.maps.event.addListener(marker, 'dragend', function (event) {
			var m_id = marker.id;
			//Set new lat,lon
			var new_lat = event.latLng.lat().toFixed(2);;
			var new_long = event.latLng.lng().toFixed(2);
			//Update value in form
			$('#' + String(point_id)).val(new_long + ',' + new_lat);
		    });
		    markers.push(marker);
		});
		window.markers = markers;
		/*********************************
		*      RECTANGLE                    *
		*********************************/
  		bounds = new google.maps.LatLngBounds(
                              new google.maps.LatLng(40.490, -111.649),  //SW corner
                              new google.maps.LatLng(44.599, -97.443)    //NE corner
		  );

		  // Define the rectangle and set its editable property to true.
		  rectangle = new google.maps.Rectangle({
		    bounds: bounds,
		    editable: true,
		    draggable: true
		  });

		  // Add an event listener on the rectangle.
		  google.maps.event.addListener(rectangle, 'bounds_changed', showNewRect);

		  // Define an info window on the map.
		  //infoWindow = new google.maps.InfoWindow();

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
		*      STATES OVERLAY                   *
		*********************************/
		//window.statemarkerOverLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/hegewisch/states_backup.kml', {
		window.statemarkerOverLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/DROUGHT/KML/states_outlined.kmz', {
                map:map,
                    preserveViewport: true,
                    suppressInfoWindows: false
                 }); 
		{% if layer=='stateoverlayer' %}
			window.statemarkerOverLayer.setMap(window.map);
		{% else %}
			window.statemarkerOverLayer.setMap(null);
		{% endif %}
 		/*********************************
                *     COUNTIES OVERLAY                   *
                *********************************/
		window.countymarkerOverLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/DROUGHT/KML/counties_outlined.kmz', {
                map:map,
                    preserveViewport: true,
                    suppressInfoWindows: false
                 }); 
		{% if layer=='countyoverlayer' %}
			window.countymarkerOverLayer.setMap(window.map);
		{% else %}
			window.countymarkerOverLayer.setMap(null);
		{% endif %}
	 	/*********************************
                *     HUCS OVERLAY                   *
                *********************************/
                window.hucsmarkerOverLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/DROUGHT/KML/hucs_outlined.kmz', {
                map:map,
                    preserveViewport: true,
                    suppressInfoWindows: false
                 });
		{% if layer=='hucoverlayer' %}
			window.hucsmarkerOverLayer.setMap(window.map);
		{% else %}
			window.hucsmarkerOverLayer.setMap(null);
		{% endif %}
 		/*********************************
                *     CLIMATE DIVS OVERLAY                   *
                *********************************/
                window.climatedivmarkerOverLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/DROUGHT/KML/divs_outlined.kmz', {
                map:map,
                    preserveViewport: true,
                    suppressInfoWindows: false
                 });
		{% if layer=='hucoverlayer' %}
			window.climatedivmarkerOverLayer.setMap(window.map);
		{% else %}
			window.climatedivmarkerOverLayer.setMap(null);
		{% endif %}
 		/*********************************
                *     PSAS OVERLAY                   *
                *********************************/
                window.psasmarkerOverLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/DROUGHT/KML/psa_outlined.kmz', {
                map:map,
                    preserveViewport: true,
                    suppressInfoWindows: false
                 });
		{% if layer=='psaoverlayer' %}
			window.psasmarkerOverLayer.setMap(window.map);
		{% else %}
			window.psasmarkerOverLayer.setMap(null);
		{% endif %}
		/*********************************
		*      KML LAYER                    *
		*********************************/
		{% if layer=='kmloverlayer' %}
			window.kmlmarkerLayer = new google.maps.KmlLayer('{{ kmlurl }}', {
			map:map,
			    preserveViewport: true,
			    suppressInfoWindows: false
			 }); 
			map.overlayMapTypes.push(mapType);
			window.kmlmarkerOverLayer.setMap(window.map);
		{% endif %}
		/*********************************/
		window.map.overlayMapTypes.push(mapType);
	      }

	      google.maps.event.addDomListener(window, 'load', initialize);
	      window.onload = initialize;

	      //$('#dataTab a').click(function (e) {
              //            e.preventDefault()
              //           $(this).tab('show')
            // })

	</script>

 	<!------------------------------------>
        <!-- Script for charts            (these D3 graphs have problems right now.. because of needing javascript array inputs.. not python array inputs-->
        <!------------------------------------>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript" src="/media/myjs/graph_utils.js"></script>
<script src="http://d3js.org/d3.v3.min.js"></script>
<!--<script type="text/javascript" src="media/myjs/d3Example.js"></script>-->
