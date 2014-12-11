 	<!------------------------------------>
        <!-- JQUERY/JQUERY UI/AJAX          -->
        <!------------------------------------>
	<script type="text/javascript"
            src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

	<!-- for date picker calendar -->
	<link rel="stylesheet" href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css">
	<script type="text/javascript" src="//code.jquery.com/ui/1.11.1/jquery-ui.js"></script>

 	<!------------------------------------>
        <!--		D3                  -->
        <!------------------------------------>

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
		$(function(){
		    $( "#dateStart" ).datepicker({
		      //setDate: {{ dateStart }},
		      changeMonth: true,
		      changeYear: true,
		      numberOfMonths: 3,
		      //minDate: "01/01/1979",
		      minDate: "1979-01-01",
		      maxDate: "0",
		      dateFormat: "yy-mm-dd",
		      onClose: function( selectedDate ) {
			$( "#dateEnd" ).datepicker( "option", "minDate", selectedDate );
		      }
		  }).datepicker('setDate', "{{ dateStart }}");
		 $( "#dateEnd" ).datepicker({
		      //defaultDate: {{ dateEnd }},
		      changeMonth: true,
		      changeYear: true,
		      numberOfMonths: 3,
		      minDate: "1979-01-01",
		      //minDate: "01/01/1979",
		      maxDate: "0",
		      dateFormat: "yy-mm-dd",
		      onClose: function( selectedDate ) {
			$( "#dateStart" ).datepicker( "option", "maxDate", selectedDate );
			}
		  }).datepicker('setDate', '{{ dateEnd }}');
		});
	</script>
	<!------------------------------------>
        <!-- NOT USED YET -->
        <!------------------------------------>
	<!--<script type="text/javascript" src="media/myjs/infoMarkers.js"></script>--> <!-- INFO MARKERS -->

	<!------------------------------------>
        <!-- Google Earth Map -->
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
	      var statemarkerLayer = null;
	      var kmlmarkerLayer = null;
	      var myZoom;	
	      var infomarkers;
	      /*********************************
	      *    INITIALIZE CALL
	      *********************************/
	      function initialize() {

       		geocoder = new google.maps.Geocoder();
            var mapCenterLongLat = "{{ mapCenterLongLat}}";
            var mapCenterLat = parseFloat(mapCenterLongLat.split(',')[1]);
            var mapCenterLong = parseFloat(mapCenterLongLat.split(',')[0]);
            //var pointsLongLat = "{{ pointsLongLat}}";
            //var pointsLat = parseFloat(pointsLongLat.split(',')[1]);
            //var pointsLong = parseFloat(pointsLongLat.split(',')[0]);

		var myCenter = new google.maps.LatLng(mapCenterLat, mapCenterLong);
		//var myCenter = new google.maps.LatLng(pointsLat, pointsLong);
		var myZoom ={{ mapzoom }}
		var mapOptions = {
		  center: myCenter,
		  zoom: myZoom,
		  maxZoom: 12,
		  streetViewControl: false,
                  mapTypeControl: true,
                   navigationControl: true, 
		  mapTypeId: google.maps.MapTypeId.ROADMAP,
                  mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
		  clickable:true,
		};

		window.map = new google.maps.Map(document.getElementById("map"),mapOptions);

 		function showNewRect(event) {
                  var ne = rectangle.getBounds().getNorthEast();
                  var sw = rectangle.getBounds().getSouthWest();

                    document.getElementById('NELat').value = ne.lat().toFixed(4);
                    document.getElementById('NELong').value = ne.lng().toFixed(4);
                    document.getElementById('SWLat').value = sw.lat().toFixed(4);
                    document.getElementById('SWLong').value = sw.lng().toFixed(4);
                }

		/*********************************
		*     COLORBAR                   *
		*********************************/
		palette_string = "{{ palette }}"
                palette_list = palette_string.split(",");
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


                /******ON OPTIONS*****/
                palette_string =document.getElementById('palette').value;
                palette_list = palette_string.split(",");
                var myPalette = new Array();
                for (var i = 0; i < palette_list.length; i++) {
                        myPalette[i]="#"+palette_list[i];
                }
		
		/*myPalette=colorbrewer['RdBu'][9];*/
		/*myPalette=colorbrewer["{{ colorbarmap }}"][{{ colorbarsize }}];*/

		colorbarsize = parseInt(document.getElementById('colorbarsize').value);
                colorbarmap = document.getElementById('colorbarmap').value;
		/*myPalette=colorbrewer["{{ colorbarmap }}"][{{ colorbarsize }}];*/
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
		for (var i=0;i<myPalette.length;i++){
			palette = palette+','+myPalette[i];
		} 
		
		/*********************************
		*      POINTS                    *
		*********************************/
        var bounds = new google.maps.LatLngBounds();
	var pointsLongLat = "{{ pointsLongLat}}";
        var point_list = pointsLongLat.split(',');
        var pLat,pLong
        for (i=0;i<point_list.length - 1;i+=2){
            pLat = point_list[i+1];
            pLong = point_list[i];
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
               
            window.pointmarker = new google.maps.Marker({
                position:new google.maps.LatLng(parseFloat(pLat),parseFloat(pLong)),
                map: map, 
                draggable: true
            });

            google.maps.event.addListener(window.pointmarker, 'dragend', function(a) {
                var div = document.createElement('div');
                var longitude=a.latLng.lng().toFixed(4);
                var latitude=a.latLng.lat().toFixed(4);
                var new_point_list = points_pre.concat([String(longitude),String(latitude)]).concat(points_post);
                document.getElementById('pointsLongLat').value = new_point_list.join();
            });
            window.pointmarker.setVisible(false);
        }

        /*
		window.pointmarker = new google.maps.Marker({position:new google.maps.LatLng({{ pointLat }},{{ pointLong }}),
			     map: map, draggable: true});

		google.maps.event.addListener(window.pointmarker, 'dragend', function(a) {
			  var div = document.createElement('div');
			  var longitude=a.latLng.lng().toFixed(4)
			  var latitude=a.latLng.lat().toFixed(4)
			  document.getElementById('pointLatLong').value = longitude+','+latitude;
			  document.getElementById('pointLat').value = latitude;
			  document.getElementById('pointLong').value = longitude;
		});
        
		window.pointmarker.setVisible(false); 
        */
        
        /*
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
		*      KML LAYER                    *
		*********************************/
		window.kmlmarkerLayer = new google.maps.KmlLayer('{{ kmlurl }}', {
		map:map,
                    preserveViewport: true,
                    suppressInfoWindows: false
                 }); //end KmlLayer
		map.overlayMapTypes.push(mapType);
		//window.kmlmarkerLayer.setMap(null);
		window.kmlmarkerLayer.setMap(window.map);
        	//window.kmlmarkersArray.push(kmlmarkerLayer);

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

<!------------------------------------>
<!--        DATE PICKER          -->
<!------------------------------------>
<script type="text/javascript">
$(function(){
    $( "#dateStart" ).datepicker({
      //setDate: {{ dateStart }},
      changeMonth: true,
      changeYear: true,
      numberOfMonths: 3,
      //minDate: "01/01/1979",
      minDate: "1979-01-01",
      maxDate: "0",
      dateFormat: "yy-mm-dd",
      onClose: function( selectedDate ) {
        $( "#dateEnd" ).datepicker( "option", "minDate", selectedDate );
      }
    }).datepicker('setDate', "{{ dateStart }}");

    $( "#dateEnd" ).datepicker({
      //defaultDate: {{ dateEnd }},
      changeMonth: true,
      changeYear: true,
      numberOfMonths: 3,
      minDate: "1979-01-01",
      //minDate: "01/01/1979",
      maxDate: "0",
      dateFormat: "yy-mm-dd",
      onClose: function( selectedDate ) {
        $( "#dateStart" ).datepicker( "option", "maxDate", selectedDate );
        }
    }).datepicker('setDate', '{{ dateEnd }}');
});
</script>


