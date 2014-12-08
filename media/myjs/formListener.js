$(function(){


	/*--------------------------------------------*/
	/*         INFOMARKER LISTENER **BROKEN       */
	/*--------------------------------------------*/
	/*--jQuery('.infomarkers').on('change', 'input[type=checkbox]',function(){
		console.log('changed infomarkers')
		if(jQuery('#infomarkers').is(':checked')){
		console.log('changed infomarkers')

		}
        });
	*/


	jQuery('#kmloption').on('change', 'input[type=checkbox]',function(){
			console.log('kml changed')
		if(jQuery('#kmloption').is(':checked')){
			console.log('kml added')
  			window.kmlmarkerLayer.setMap(window.map);
		}else{
			console.log('kml removed')
			window.kmlmarkerLayer.setMap(null);
		}

        });

	/*--------------------------------------------*/
	/*         POLYGON LISTENER 		      */
	/*--------------------------------------------*/
	 jQuery('#NELat,#NELong,#SWLat,#SWLong').keyup( function(){
                 var ne_lat =parseFloat(document.getElementById('NELat').value);
                 var ne_long=parseFloat(document.getElementById('NELong').value);
                 var sw_lat =parseFloat(document.getElementById('SWLat').value);
                 var sw_long=parseFloat(document.getElementById('SWLong').value);
                 bounds = new google.maps.LatLngBounds(
                              new google.maps.LatLng(sw_lat, sw_long),  //SW corner
                              new google.maps.LatLng(ne_lat, ne_long)    //NE corner
                          );
                rectangle.setBounds(bounds);
        });


	/*--------------------------------------------*/
	/*        STATE LISTENER 		      */
	/*--------------------------------------------*/
	 jQuery('#state').on('change', function(){
		 //NewMapCenter = window.map.getCenter();
		//alert(NewMapCenter)
                 //jQuery('.pointLat').val(NewMapCenter.lat());
                 //jQuery('.pointLon').val(NewMapCenter.lng());
	});
	/*--------------------------------------------*/
	/*        POINT  LISTENER 		      */
	/*--------------------------------------------*/
	  jQuery('#pointLat').keyup( function(){
		 var latitude =parseFloat(document.getElementById('pointLat').value);
		 var longitude=parseFloat(document.getElementById('pointLong').value);
		var newLatLng = new google.maps.LatLng(latitude, longitude); 
		window.pointmarker.setPosition(newLatLng);
		window.map.setCenter(newLatLng);
        });
         jQuery('#pointLong').keyup( function(){
                var latitude =parseFloat(document.getElementById('pointLat').value);
                 var longitude=parseFloat(document.getElementById('pointLong').value);
		var newLatLng = new google.maps.LatLng(latitude, longitude); 
                window.pointmarker.setPosition(newLatLng);
		window.map.setCenter(newLatLng);
        });
	
	/*--------------------------------------------*/
	/*        DOMAIN  LISTENER 		      */
	/*--------------------------------------------*/
        jQuery('#domainType').on('change', function(){
            if(jQuery(this).val()=='states'){
                 jQuery('.points').hide();
                 jQuery('.polygon').hide();
                 jQuery('.states').show();   
		 window.pointmarker.setVisible(false);
		 jQuery('.rectangle').hide();
		 rectangle.setMap(null);
	
		//hide until I figure out the state map
		 window.statemarkerLayer.setMap(window.map);
		 //window.statemarkerLayer.setMap(null);

            }
            else if(jQuery(this).val()=='points'){
                 jQuery('.points').show();
                 jQuery('.polygon').hide();
                 jQuery('.states').hide();
		 window.pointmarker.setVisible(true);
		 window.statemarkerLayer.setMap(null);
		 jQuery('.rectangle').hide();
		 rectangle.setMap(null);
            }
            else if(jQuery(this).val()=='rectangle'){
                 jQuery('.points').hide();
                 jQuery('.polygon').show();
                 jQuery('.states').hide();
		 window.pointmarker.setVisible(false);
		 window.statemarkerLayer.setMap(null);
		 jQuery('.rectangle').show();
                 rectangle.setMap(window.map);
	}
           else{
                 jQuery('.points').hide();
                 jQuery('.polygon').hide();
                 jQuery('.states').hide();
		 window.pointmarker.setVisible(false);
		 window.statemarkerLayer.setMap(null);
		 jQuery('.rectangle').hide();
		 rectangle.setMap(null);
           }
    });

});
