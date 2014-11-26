$(function(){

	 jQuery('#state').on('change', function(){
		 //NewMapCenter = window.map.getCenter();
		//alert(NewMapCenter)
                 //jQuery('.pointLat').val(NewMapCenter.lat());
                 //jQuery('.pointLon').val(NewMapCenter.lng());
	});
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
	
    jQuery('#domainType').on('change', function(){
            if(jQuery(this).val()=='states'){
                 jQuery('.points').hide();
                 jQuery('.polygon').hide();
                 jQuery('.states').show();   
		 window.pointmarker.setVisible(false);
	
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
            }
            else if(jQuery(this).val()=='polygon'){
                 jQuery('.points').hide();
                 jQuery('.polygon').show();
                 jQuery('.states').hide();
		 window.pointmarker.setVisible(true);
		 window.statemarkerLayer.setMap(null);
	}
           else{
                 jQuery('.points').hide();
                 jQuery('.polygon').hide();
                 jQuery('.states').hide();
		 window.pointmarker.setVisible(false);
		 window.statemarkerLayer.setMap(null);
		
           }
    });


});
