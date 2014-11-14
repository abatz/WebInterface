$(function(){
    jQuery('#domainType').on('change', function(){
            if(jQuery(this).val()=='states'){
                 jQuery('.points').hide();
                 jQuery('.polygon').hide();
                 jQuery('.states').show();   

		 window.pointmarker.setVisible(false);
	

		//hide until I figure out the state map
		 window.statemarkerLayer.setMap(window.map);
		 //window.statemarkerLayer.setMap(null);
                 //jQuery('.basicvariable').val(0);

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
