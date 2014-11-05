$(function(){
     jQuery('#product').on('change', function(){
	    if(jQuery(this).val()=='gridded'){
		 jQuery('.variableGrid').show();
		 jQuery('.variableLandsat').hide();
		 jQuery('.basicvariable').val(0);
		
	    }
	    else if(jQuery(this).val()=='landsat'){
		 jQuery('.variableLandsat').show();
		 jQuery('.variableGrid').hide();
		 jQuery('.basicvariable').val(0);
	    }
	   else{
	   }
    });

});
