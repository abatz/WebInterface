$(function(){

	/*--------------------------------------------*/
	/*         LAYERS LISTENER                    */
	/*--------------------------------------------*/
	jQuery('.layer').on('change','input[type=radio]', function(){
		/*-------------------*/
		/*         STATES    */
		/*-------------------*/
		if($('input[id=stateoverlayer]:checked').val()=="stateoverlayer"){
			 window.statemarkerOverLayer = new google.maps.KmlLayer(
				'http://nimbus.cos.uidaho.edu/DROUGHT/KML/states_outlined.kmz', {
			 map:window.map,
			    preserveViewport: true,
			    suppressInfoWindows: false
			 });
			 window.statemarkerOverLayer.setMap(window.map);
		}else{
		  	window.statemarkerOverLayer.setMap(null);
		};
		/*-------------------*/
		/*        COUNTY    */
		/*-------------------*/
		if($('input[id=countyoverlayer]:checked').val()=="countyoverlayer"){
			 window.countymarkerOverLayer = new google.maps.KmlLayer(
				'http://nimbus.cos.uidaho.edu/DROUGHT/KML/counties_outlined.kmz', {
                	    map:window.map,
			    preserveViewport: true,
			    suppressInfoWindows: false
			 });
		  	window.countymarkerOverLayer.setMap(window.map);
		}else{
		  	window.countymarkerOverLayer.setMap(null);
		};
		/*-------------------*/
		/*        HUC    */
		/*-------------------*/
		if($('input[id=hucoverlayer]:checked').val()=="hucoverlayer"){
			 window.hucsmarkerOverLayer = new google.maps.KmlLayer(
				'http://nimbus.cos.uidaho.edu/DROUGHT/KML/hucs_outlined.kmz', {
			map:window.map,
			    preserveViewport: true,
			    suppressInfoWindows: false
			 });
                  	window.hucsmarkerOverLayer.setMap(window.map);
                }else{
                 	 window.hucsmarkerOverLayer.setMap(null);
                };
		/*-------------------*/
		/*        CLIMATE DIV    */
		/*-------------------*/
		if($('input[id=climatedivoverlayer]:checked').val()=="climatedivoverlayer"){
			window.climatedivmarkerOverLayer = new google.maps.KmlLayer(
                        'http://nimbus.cos.uidaho.edu/DROUGHT/KML/divs_outlined.kmz', {
                        map:window.map,
                            preserveViewport: true,
                            suppressInfoWindows: false
                         });
                  	window.climatedivmarkerOverLayer.setMap(window.map);
                }else{
                  	window.climatedivmarkerOverLayer.setMap(null);
                };
		/*-------------------*/
		/*       PSAS        */
		/*-------------------*/
		if($('input[id=psaoverlayer]:checked').val()=="psaoverlayer"){
			  window.psasmarkerOverLayer = new google.maps.KmlLayer(
                        'http://nimbus.cos.uidaho.edu/DROUGHT/KML/psa_outlined.kmz', {
                        map:window.map,
                            preserveViewport: true,
                            suppressInfoWindows: false
                         });
                  	window.psasmarkerOverLayer.setMap(window.map);
                }else{
                  	window.psasmarkerOverLayer.setMap(null);
                };
		/*-------------------*/
		/*       KML        */
		/*-------------------*/
		if($('input[id=kmloverlayer]:checked').val()=="kmloverlayer"){
			kmlurl=document.getElementById('kmlurl').value;
			if(kmlurl!=''){
				window.kmlmarkerOverLayer = new google.maps.KmlLayer(kmlurl, {
				  map:window.map,
				    preserveViewport: true,
				    suppressInfoWindows: false
				});
				window.kmlmarkerOverLayer.setMap(window.map);
			}
		}else{
		  	window.kmlmarkerOverLayer.setMap(null);
		};
	});

// This does not work well for autocomplete
 	jQuery('#kmlurl').on('change paste keyup', function(){
	       if($('input[id=kmloverlayer]:checked').val()=="kmloverlayer"){
			var kmlurl=document.getElementById('kmlurl').value;
			window.kmlmarkerOverLayer = new google.maps.KmlLayer(kmlurl, {
				map:window.map,
				    preserveViewport: true,
				    suppressInfoWindows: false
			});
                	window.kmlmarkerOverLayer.setMap(window.map);
		}else{
                	window.kmlmarkerOverLayer.setMap(null);
		}
//                window.kmlmarkerOverLayer.setMap(window.map);
	});


});
