$(function(){

	/*--------------------------------------------*/
	/*         POINTS LISTENERS                    */
	/*--------------------------------------------*/
	    /*
	    Deal with three inputs
	    1. Checkbox for a marker has changed
	    See if point is checked and update map, pointsLongLat accordingly
	    */
	    $(".pointCheck").bind("keyup change", function(e) {
		    var LongLatStr,LongLatList,LongLat;
		    var Long,Lat,latlong;
		    LongLatStr = $('#pointsLongLat').val();
		    LongLatList = LongLatStr.replace(' ','').split(',');
		    point_id = parseInt($(this).val());
		    LongLat = String($('#p' + point_id).val()).replace(' ','');
		    Long = parseFloat(LongLat.split(',')[0])
		    Lat = parseFloat(LongLat.split(',')[1])
		    //See if point is checked and update map, pointsLongLat accordingly
		    if ($(this).is(':checked')) {
		        //Show marker to map
		        if (LongLat){
			        latlong = new google.maps.LatLng(Lat,Long);
			        window.markers[point_id-1].position = latlong;
			        window.markers[point_id-1].setVisible(true);
		        }
		        //Update hidden variable that keeps track of checkboxes
		        $('#p' + String(point_id) + 'check').val('checked');
		    }
		    else {
		        //Update hidden variable that keeps track of checkboxes
		        $('#p' + String(point_id) + 'check').val('');
		        //Hide marker from map
		        window.markers[point_id-1].setVisible(false);
		    }
	    });
	    
        //2. Input field for marker
	    jQuery('.point').on('change','input.pointLongLat[type=text]', function(){
		    //Change position of marker on map
		    //Generate new pointsLongLat string
		    var point_id,LongLat,Lat,Long,latlong;
		    $('.point').each(function() {
		        if ($(this).css('display') == 'block' && $('#check' + String(point_id)).is(':checked')){
			        point_id = parseInt($(this).attr('id').split('point')[1]);
			        LongLat = String($('#p' + String(point_id)).val()).replace(' ','');
			        Long = parseFloat(LongLat.split(',')[0]);
			        Lat = parseFloat(LongLat.split(',')[1]);
			        latlong = new google.maps.LatLng(Lat,Long);
			        //Update marker on map
			        window.markers[point_id-1].position = latlong;
			        window.markers[point_id-1].setVisible(true);
		        }
		    });
	    });
	    
	    //3. Add another point button
	    jQuery('.point').on('click','.add', function(){
		    var next_point_id = parseInt($(this).attr('id').split('pl')[1]);
		    //Hide plus icon of this marker
		    $(this).css('display','none');
		    //Show next point
		    $('#point' + String(next_point_id)).css('display','block');
		    //Show next marker
		    window.markers[next_point_id - 1].setVisible(true);            
		    //Update check value
		    $('#p' + String(next_point_id) + 'check').val('checked');
	    });

	    //3. Take point button away
	    jQuery('.point').on('click','.minus', function(){
		    var point_id = parseInt($(this).attr('id').split('mi')[1]);
		    //Find last marker and show the plus sign on that marker
		    idx = point_id -1;
		    if (String(point_id)== '1' ||  String(point_id) == 7){
		        while ($('#point' + idx).css('display') == 'none' ){
			        idx-=1;
		        }
		    }
		    $('#pl' + String(idx +1)).css('display','inline');
		    //Hide this point
		    $('#point' + String(point_id)).css('display','none');
		    //Hide this marker
		    window.markers[point_id - 1].setVisible(false);
		    $('#p' + String(point_id) + 'check').val('');
	    });
	    
        //onsubmit of form, update pointsLongLat
        //And show progressbar if domaintType == points
	    //This function is called in 
        //templates/includes/timeseriesoptions.html on form_map submit
	    jQuery('#form_map').submit(function( event ) {
            if ( $('#domainType').val() == 'points') {
                //Show Progress Bar
                //If large request, show special progress bar
                var dS = new Date($('#dateStart').val()).getTime();
                var dE = new Date($('#dateEnd').val()).getTime();
                var message;
                if (dE - dS >= 5 * 365 * 24 * 60 * 60 * 1000){
                    p_message = 'You asked for a large amount of data. ' + 
                    'Please be patient while we process your request.'
                }
                else{
                    p_message = 'Processing Request';
                }
                waitingDialog.show(p_message,{dialogSize: 'sm', progressType: 'warning'});
                window.timeoutID =setTimeout(function () {waitingDialog.hide();}, 180000);
		        //Update LongLat
                var LongLatStr = '';
		        $('.point').each(function() {
			        point_id = parseInt($(this).attr('id').split('point')[1]);
			        if ($(this).is(':visible') && $('#check' + String(point_id)).is(':checked')) {
			            //Update hidden check variables for display and checkbox
			            $('#p' + String(point_id) + 'check').val('checked');
			            $('#p' + String(point_id) + 'display').val('block');
			            //Point visible and checkbox checked, add to pointsLongLat variable
			            LongLat = String($('#p' + String(point_id)).val()).replace(' ','');
			            Long = parseFloat(LongLat.split(',')[0]);
			            Lat = parseFloat(LongLat.split(',')[1]);
			            //Update LongLat string
			            if (LongLatStr != '') {
				            LongLatStr+=',' + LongLat;
			            }
			            else{
				            LongLatStr+=LongLat;
			            }
			        }
			        else {
			            //Update hidden variables for display and checkbox
			            if ($(this).not(':visible')){
				            $('#p' + String(point_id) + 'display').val('none');
			            }
			            if ($('#check' + String(point_id)).not(':checked')){
				            $('#p' + String(point_id) + 'check').val('checked');
			            }
			        }
		        });
		        //Update pointsLongLat
		        $('#pointsLongLat').val(LongLatStr);
		    }
	    }); 

});
