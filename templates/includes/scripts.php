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
		function activaTab(tab){
			$('.tab-pane a[href="#' + tab + '"]').tab('show');
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
	      var pointmarker = null;
	      var pointmarker1 = null;
	      var pointmarker2 = null;
	      var pointmarker3 = null;
	      var pointmarker4 = null;
	      var statemarkerLayer = null;
	      var statemarkerOverLayer = null;
	      var countymarkerOverLayer = null;
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
		google.maps.event.addListener(map,'center_changed',function(){
			newCenter = window.map.getCenter();
			//myCenterLat = newCenter.lat().toFixed(4);
			//myCenterLong = newCenter.lon().toFixed(4);
			//document.getElementById('mapCenterLongLat').value =str(myCenterLat)+','+str(myCenterLong);
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
		var bounds = new google.maps.LatLngBounds();
		var timeSeriesGraphData = "{{ timeSeriesGraphData }}";
		var domainType = document.getElementById('domainType').value;
		var pointsLongLat = document.getElementById('pointsLongLat').value.replace(' ','');
		var point_list = pointsLongLat.split(',');
		var pLat,pLong, pointmarkers = [];
		//FIX ME: multi points not working correctly!!
		//Take first coords form pointsLongLat input variable for marker showing
		pLat = parseFloat(point_list[1]);
		pLong = parseFloat(point_list[0]);

/*	doesn't work!
		//katherine's attempt at the points
		color=['blank','red', 'blue','green', 'orange','purple'];
		   i=1;
		   var point1LongLat = document.getElementById('point1LongLat').value.replace(' ','');
		    var pointmarker1 = new google.maps.Marker({
			position:new google.maps.LatLng(pLat,pLong),
			map: map,
			draggable: true,
			icon: new google.maps.MarkerImage("http://google.com/mapfiles/ms/micons/" + color[i] + ".png")
		    });
		    google.maps.event.addListener(pointmarker1, 'dragend', function(a) {
			var div = document.createElement('div');
			var longitude=a.latLng.lng().toFixed(4);
			var latitude=a.latLng.lat().toFixed(4);
		    });
		    window.pointmarker1.setVisible(false);
		  i=2;
                   var point2LongLat = document.getElementById('point2LongLat').value.replace(' ','');
                    var pointmarker2 = new google.maps.Marker({
                        position:new google.maps.LatLng(pLat,pLong),
                        map: map,
                        draggable: true,
                        icon: new google.maps.MarkerImage("http://google.com/mapfiles/ms/micons/" + color[i] + ".png")
                    });
                    google.maps.event.addListener(pointmarker2, 'dragend', function(a) {
                        var div = document.createElement('div');
                        var longitude=a.latLng.lng().toFixed(4);
                        var latitude=a.latLng.lat().toFixed(4);
                    });
                    window.pointmarker2.setVisible(true);
		 i=3;
                   var point3LongLat = document.getElementById('point3LongLat').value.replace(' ','');
                    var pointmarker3 = new google.maps.Marker({
                        position:new google.maps.LatLng(pLat,pLong),
                        map: map,
                        draggable: true,
                        icon: new google.maps.MarkerImage("http://google.com/mapfiles/ms/micons/" + color[i] + ".png")
                    });
                    google.maps.event.addListener(pointmarker3, 'dragend', function(a) {
                        var div = document.createElement('div');
                        var longitude=a.latLng.lng().toFixed(4);
                        var latitude=a.latLng.lat().toFixed(4);
                    });
                    window.pointmarker3.setVisible(true);
		   i=4;
                   var point4LongLat = document.getElementById('point4LongLat').value.replace(' ','');
                    var pointmarker4 = new google.maps.Marker({
                        position:new google.maps.LatLng(pLat,pLong),
                        map: map,
                        draggable: true,
                        icon: new google.maps.MarkerImage("http://google.com/mapfiles/ms/micons/" + color[i] + ".png")
                    });
                    google.maps.event.addListener(pointmarker4, 'dragend', function(a) {
                        var div = document.createElement('div');
                        var longitude=a.latLng.lng().toFixed(4);
                        var latitude=a.latLng.lat().toFixed(4);
                    });
                    window.pointmarker4.setVisible(true);
*/		   
/*    britta's multi point

		for (i=0;i<point_list.length - 1;i+=2){
		    pLat = parseFloat(point_list[i+1]);
		    pLong = parseFloat(point_list[i]);
		    bounds.extend(new google.maps.LatLng(pLat,pLong));
		    var points_pre, points_post, new_point_list =[]
		    if (i > 0){
			points_pre = point_list.splice(0,i);
		    }
		    else {
			var points_pre =[];
		    }
		    if (i < point_list.length - 2) {
			points_post = point_list.splice(i+2, point_list.length);
		    }
		    else {
			points_post = [];
		    }
		    var pointmarker = new google.maps.Marker({
			position:new google.maps.LatLng(pLat,pLong),
			map: map, 
			draggable: true
		    });
		    google.maps.event.addListener(pointmarker, 'dragend', function(a) {
			var div = document.createElement('div');
			var longitude=a.latLng.lng().toFixed(4);
			var latitude=a.latLng.lat().toFixed(4);
			var new_point_list = points_pre.concat([String(longitude),String(latitude)]).concat(points_post);
			document.getElementById('pointsLongLat').value = new_point_list.join();
		    });
		    window.pointmarker.setVisible(false);
		}
		window.pointmarkers = pointmarkers;
*/

		window.pointmarker = new google.maps.Marker({
			position:new google.maps.LatLng(parseFloat(pLat),parseFloat(pLong)),
			map: map, 
			draggable: true
		});
		google.maps.event.addListener(window.pointmarker, 'dragend', function(a) {
			  var div = document.createElement('div');
			  var longitude=a.latLng.lng().toFixed(4)
			  var latitude=a.latLng.lat().toFixed(4)
			  document.getElementById('pointsLongLat').value = longitude+','+latitude;
		});
		if (domainType == 'points' && timeSeriesGraphData != '') {
		    window.pointmarker.setVisible(true); 
		}
		else {
			    window.pointmarker.setVisible(false); 
		}
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
			//alert(kmlEvent.featureData.name);
                        $('#state').val(kmlEvent.featureData.name);
                	findAddress();
			//var NewMapCenter = window.map.getCenter();
			//var longitude = NewMapCenter.lng();
			//var latitude = NewMapCenter.lat();
			//document.getElementById('pointLatLong').value = longitude+','+latitude
			//NewMapCenter = window.map.getCenter();
			//window.pointmarker.latLng = window.map.getCenter();
                	//jQuery('#pointLat').html(NewMapCenter.lat());
                 	//jQuery('#pointLong').hmtl(NewMapCenter.lon());
	
          	}); //end listener
		window.statemarkerLayer.setMap(null);
		/*********************************
		*      STATES OVERLAY                   *
		*********************************/
		//window.statemarkerOverLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/hegewisch/USStatesOutline.kmz', {
		window.statemarkerOverLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/hegewisch/states_backup.kml', {
                map:map,
                    preserveViewport: true,
                    suppressInfoWindows: false
                 }); 
		window.statemarkerOverLayer.setMap(null);
 		/*********************************
                *     COUNTIES OVERLAY                   *
                *********************************/
                /*window.countymarkerOverLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/hegewisch/counties.kml', {
                map:map,
                    preserveViewport: true,
                    suppressInfoWindows: false
                 }); 
                window.countymarkerOverLayer.setMap(null);
		*/
		/*********************************
		*      KML LAYER                    *
		*********************************/
		window.kmlmarkerLayer = new google.maps.KmlLayer('{{ kmlurl }}', {
		map:map,
                    preserveViewport: true,
                    suppressInfoWindows: false
                 }); 
		map.overlayMapTypes.push(mapType);
		window.kmlmarkerLayer.setMap(window.map);

		/*********************************
		*      MULTIPLE POINTS           *
		*********************************/

		/*********************************/
		window.map.overlayMapTypes.push(mapType);
	      }
		

	      google.maps.event.addDomListener(window, 'load', initialize);
	      window.onload = initialize;
	</script>

 	<!------------------------------------>
        <!-- Script for charts            (these D3 graphs have problems right now.. because of needing javascript array inputs.. not python array inputs-->
        <!------------------------------------>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript" src="/media/myjs/graph_utils.js"></script>
<script src="http://d3js.org/d3.v3.min.js"></script>
<!--<script type="text/javascript" src="media/myjs/d3Example.js"></script>-->
