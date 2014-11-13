$(function(){
    jQuery('#domainType').on('change', function(){
            if(jQuery(this).val()=='states'){
                 jQuery('.points').hide();
                 jQuery('.states').show();
                 //jQuery('.basicvariable').val(0);

            }
            else if(jQuery(this).val()=='points'){
                 jQuery('.points').show();
                 jQuery('.states').hide();
            }
           else{
           }
    });


});
