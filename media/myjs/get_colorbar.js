(function($){
	window.get_colorbar=function(){
		
	$.ajax( {   url : "/media/myjs/get_colorbar_url.php",
               dataType: 'json',
                type    : 'post',
               data    : $('#form_div').serialize(),
                success : function(data){
                               if (data.status == "success"){
                                        $('img#target_colorbar').attr({src: data.colorbar}).parent().attr({href:data.colorbar});
                                }
                                else{
                                        alert(data.error)
                                }
                        } // anon function
                }); // ajax	

	}
})
