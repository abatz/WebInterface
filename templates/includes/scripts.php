 	<!------------------------------------>
        <!-- JQUERY/JQUERY UI/AJAX          -->
        <!------------------------------------>
	<script type="text/javascript"
            src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
	<link rel="stylesheet" href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css">
	<script type="text/javascript" src="//code.jquery.com/ui/1.11.1/jquery-ui.js"></script>

 	<!------------------------------------>
        <!--		MY SCRIPTS           -->
        <!------------------------------------>
	<script type="text/javascript" src="media/myjs/get_colorbar.js"></script> <!-- COLORBAR --> 
	<script type="text/javascript" src="media/myjs/formListener.js"></script> <!-- FORM LISTENER -->
	<script type="text/javascript" src="media/myjs/showLoadingImage.js"></script> <!-- PROGRESS BAR -->
	<script type="text/javascript" src="media/myjs/zoomStates.js"></script> <!-- ZOOM TO STATE -->

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
	      var myZoom;	
	      var infomarkers;
	      /*********************************
	      *    INITIALIZE CALL
	      *********************************/
	      function initialize() {
       		geocoder = new google.maps.Geocoder();
		var myCenter = new google.maps.LatLng({{ pointLat }}, {{ pointLong }});
		var myZoom ={{ mapzoom }}
		var mapOptions = {
		  center: myCenter,
		  zoom: myZoom,
		  maxZoom: 10,
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
		//	bounds.extend(marker.position);
		    //  });
		      //  Fit these bounds to the map
		   //   map.fitBounds(bounds);
		    //}
		    //AutoCenter();

		/*********************************
		*      POINTS                    *
		*********************************/
		window.pointmarker = new google.maps.Marker({position:new google.maps.LatLng({{ pointLat }},{{ pointLong }}),
			     map: map, draggable: true});

		google.maps.event.addListener(window.pointmarker, 'dragend', function(a) {
			  var div = document.createElement('div');
			  var longitude=a.latLng.lng().toFixed(4)
			  var latitude=a.latLng.lat().toFixed(4)
			  document.getElementById('pointLatLong').value = longitude+','+latitude;
			  /*document.getElementById('pointLat').value = latitude;
			  document.getElementById('pointLong').value = longitude;*/
		});
		window.pointmarker.setVisible(false); 

		/*********************************
		*      STATES                    *
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
		  infoWindow = new google.maps.InfoWindow();


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
		*      POLYGON                    *
		*********************************/

		/*********************************
		*      MULTIPLE POINTS           *
		*********************************/

		/*********************************/
		window.map.overlayMapTypes.push(mapType);
	      }
		

	      google.maps.event.addDomListener(window, 'load', initialize);
	      window.onload = initialize;
	</script>

	<!--<script type="text/javascript" src="media/myjs/pointMarkers.js"></script>--> <!-- POINT MARKER FUNCTIONS -->


 	<!------------------------------------>
        <!-- Script for charts            (these D3 graphs have problems right now.. because of needing javascript array inputs.. not python array inputs-->
        <!------------------------------------>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript" src="/media/myjs/graph_utils.js"></script>
        <script src="http://d3js.org/d3.v3.min.js"></script>

	 <!--<script type="text/javascript" src="media/myjs/d3Example.js"></script>-->
	<script type="text/javascript">
		 //de = {{ timeSeriesGraphData }};
		de=[{'name': '01/18/2013', 'count': 0.16711192997972898}, {'name': '01/25/2013', 'count': 0.1506114002764564}, {'name': '02/03/2013', 'count': 0.17008802964192737}, {'name': '02/10/2013', 'count': 0.05392157351396518}, {'name': '02/26/2013', 'count': 0.16506960912310953}, {'name': '03/07/2013', 'count': 0.1948166408371296}, {'name': '03/14/2013', 'count': 0.1671125205954915}, {'name': '03/30/2013', 'count': 0.29349505796330344}];
		  //de=[{'count': 728, 'name': 'sample0'}, {'count': 824, 'name': 'sample1'}, {'count': 963, 'name': 'sample2'}, {'count': 927, 'name': 'sample3'}, {'count': 221, 'name': 'sample4'}, {'count': 574, 'name': 'sample5'}, {'count': 733, 'name': 'sample6'}, {'count': 257, 'name': 'sample7'}, {'count': 879, 'name': 'sample8'}, {'count': 620, 'name': 'sample9'}];

    var mySVG = d3.select("#d3bargraph_div")
      .append("svg")
      .attr("width", 500) 
      .attr("height", 500)
      .style('position','absolute')
      .style('top',50)
      .style('left',40)
      .attr('class','fig');

    var heightScale = d3.scale.linear()
      .domain([0, d3.max(de,function(d) { return d.count;})])
      .range([0, 400]);

    mySVG.selectAll(".xLabel")
      .data(de)
      .enter().append("svg:text")
      .attr("x", function(d,i) {return 113 + (i * 22);})
      .attr("y", 435)
      .attr("text-anchor", "middle") 
      .text(function(d,i) {return d.name;})
      .attr('transform',function(d,i) {return 'rotate(-90,' + (113 + (i * 22)) + ',435)';}); 

	mySVG.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .text("Date");


    mySVG.selectAll(".yLabel")
      .data(heightScale.ticks(10))
      .enter().append("svg:text")
      .attr('x',80)
      .attr('y',function(d) {return 400 - heightScale(d);})
      .attr("text-anchor", "end") 
      .text(function(d) {return d;}); 

	mySVG.append("text")
    .attr("class", "y label")
    .attr("text-anchor", "end")
    .attr("transform", "rotate(-90)")
    .text("NDVI");


    mySVG.selectAll(".yTicks")
      .data(heightScale.ticks(10))
      .enter().append("svg:line")
      .attr('x1','90')
      .attr('y1',function(d) {return 400 - heightScale(d);})
      .attr('x2',320)
      .attr('y2',function(d) {return 400 - heightScale(d);})
      .style('stroke','lightgray'); 

    var myBars = mySVG.selectAll('rect')
      .data(de)
      .enter()
      .append('svg:rect')
      .attr('width',20)
      .attr('height',function(d,i) {return heightScale(d.count);})
      .attr('x',function(d,i) {return (i * 22) + 100;})
      .attr('y',function(d,i) {return 400 - heightScale(d.count);})
      .style('fill','lightblue')
      .on('mouseover', function(d,i) { 
         d3.select(this)
            .style('fill','gray'); 
         statusText 
            .text(d.count)
            .attr('fill','white')
            .attr("text-anchor", "start") 
            .attr("x", (i * 22) + 105) 
            .attr("y", 414) 
            .attr('transform', 'rotate(-90,' + (100 + (i * 22)) + ',400)'); }) 
      .on('mouseout', function(d,i) { 
         statusText 
           .text(''); 
         d3.select(this)
           .style('fill','lightblue'); 
      }); 
   var statusText = mySVG.append('svg:text');


      </script>
 <script type="text/javascript">
                data=[{'name': '01/18/2013', 'count': 0.16711192997972898}, {'name': '01/25/2013', 'count': 0.1506114002764564}, {'name': '02/03/2013', 'count': 0.17008802964192737}, {'name': '02/10/2013', 'count': 0.05392157351396518}, {'name': '02/26/2013', 'count': 0.16506960912310953}, {'name': '03/07/2013', 'count': 0.1948166408371296}, {'name': '03/14/2013', 'count': 0.1671125205954915}, {'name': '03/30/2013', 'count': 0.29349505796330344}];


var margin = {top: 70, right: 70, bottom: 70, left: 70},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parseDate = d3.time.format("%d-%b-%y").parse;

var x = d3.time.scale()
.range([0, width]);

var y = d3.scale.linear()
.range([height, 0]);

var xAxis = d3.svg.axis()
.scale(x)
.orient("bottom");

var yAxis = d3.svg.axis()
.scale(y)
.orient("left");

var line = d3.svg.line()
.x(function(d) { return x(d.date); })
.y(function(d) { return y(d.close); });

var svg = d3.select("d3linegraph_div").append("svg")
.attr("width", width + margin.left + margin.right)
.attr("height", height + margin.top + margin.bottom)
.append("g")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

data.forEach(function(d) {
    d.date = parseDate(d.date);
    d.close = d.close;
});

console.log(data);

x.domain(d3.extent(data, function(d) { return d.date; }));
y.domain(d3.extent(data, function(d) { return d.close; }));

//Create Title 
svg.append("text")
.attr("x", width / 2 )
.attr("y", -10)
.attr("class", "title")
.style("text-anchor", "middle")
.style("font-size", "200%")
.text("Title of Diagram");



//Create X Axis
svg.append("g")
.attr("class", "x axis")
.attr("transform", "translate(0," + height + ")")
.call(xAxis)
.append("text")
.attr("x", width / 2 )
.attr("y", margin.bottom / 2)
.style("text-anchor", "middle")
.style("font-size", "150%")
.text("Date");

//Create Y Axis		
svg.append("g")
.attr("class", "y axis")
.call(yAxis)
.append("text")
.attr("transform", "rotate(-90)")
.attr("y", 6)
.attr("y", - margin.left / 2)
.attr("x", - height / 2)
.style("text-anchor", "middle")
.style("font-size", "150%")
.text("Close");

svg.append("path")
.datum(data)
.attr("class", "line")
.attr("d", line);

// add circles
svg.selectAll('circle')
.data(data)
.enter().append('circle')
.attr('cx', function (d) { return x(d.date); })
.attr('cy', function (d) { return y(d.close); })
.attr('r', 3)
.attr('fill', 'red'); 

// add rectangle for label and line
var infos = svg.append("g")
.selectAll("rect")
.data(data)
.enter()
.append("g")
.attr("transform",function(d,i){d.x = x(d.date); d.y = height/2; return "translate(" + d.x + "," + d.y + ")";})
	



</script>
