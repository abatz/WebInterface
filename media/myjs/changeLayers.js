function changeLayers(){
	  window.markerLayer.setMap(null);
	 //setAllMap(null);
	    if(jQuery(this).val()=='states'){
		<!--window.markerLayer.setMap('http://www.wrcc.dri.edu/monitor/WWDT/KML/states.kmz');-->
		var markerLayer = new google.maps.KmlLayer('http://www.wrcc.dri.edu/monitor/WWDT/KML/states.kmz', { 
		    preserveViewport: true,
		    suppressInfoWindows: false
		 }); //end KmlLayer
	    }
	    else if(jQuery(this).val()=='counties'){
		var markerLayer = new google.maps.KmlLayer('http://www.wrcc.dri.edu/monitor/WWDT/KML/counties.kmz', {
		    preserveViewport: true,
		    suppressInfoWindows: false
		 }); //end KmlLayer
	    }
	    else if(jQuery(this).val()=='hucs'){
		var markerLayer = new google.maps.KmlLayer('http://www.wrcc.dri.edu/monitor/WWDT/KML/hucs.kmz', {
		    preserveViewport: true,
		    suppressInfoWindows: false
		 }); //end KmlLayer
	    }
	  else if(jQuery(this).val()=='divs'){
		<!--var markerLayer = new google.maps.KmlLayer('http://www.wrcc.dri.edu/monitor/WWDT/KML/divs.kmz', {-->
		<!--var markerLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/hegewisch/divs_wF.kmz', {-->
		<!--var markerLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/hegewisch/divs_new.kmz', {-->
		var markerLayer = new google.maps.KmlLayer('http://nimbus.cos.uidaho.edu/hegewisch/divs_newer.kmz', {
		    preserveViewport: true,
		    suppressInfoWindows: false
		 }); //end KmlLayer
	    }
	   else if(jQuery(this).val()=='psas'){
		var markerLayer = new google.maps.KmlLayer('http://www.wrcc.dri.edu/monitor/WWDT/KML/psa.kmz', {
		    preserveViewport: true,
		    suppressInfoWindows: false
		 }); //end KmlLayer
	    }
	  else if(jQuery(this).val()=='ushcns'){
		var markerLayer = new google.maps.KmlLayer('http://www.wrcc.dri.edu/monitor/WWDT/KML/stations.kml', {
		    preserveViewport: true,
		    suppressInfoWindows: false
		 }); //end KmlLayer
	    }
	  else if(jQuery(this).val()=='points'){
		markerLayer.setMap(null);
	    }
	  else if(jQuery(this).val()=='CONUS'){
		markerLayer.setMap(null);
	    }
	markerLayer.setMap(window.map);

	  //--------------------------------------------//
	  //           LISTENER				//
	  //--------------------------------------------//
	  google.maps.event.addListener(markerLayer, 'click', function(kmlEvent) {
		//console.log("changed");
		//alert(kmlEvent.featureData.id);
		//$('#SubDomainType').val(kmlEvent.featureData.name);  //only for station.. others are id
		$('#SubDomainType').val(kmlEvent.featureData.id);  //only for station.. others are id
	  }); //end listener
}; 
