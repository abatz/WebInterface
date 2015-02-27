$(function(){

	jQuery('#chartType').on('change', function(){
	     chartType=document.getElementById('chartType').value;
  	     generateHighChartFigure(series_data,'#container',chartType,title_timeseries,subtitle,dateStart,dateEnd,
			yLabel,legendTitle,axis_min,window.variableShortName_time,varUnits);
	});


	/*--------------------------------------------*/
	/*        TIMESERIES ACCORDION LISTENERS      */
	/*--------------------------------------------*/
        /*Show markers only of time series option is expanded*/
	/*jQuery('#accordionBUILDTIMESERIES').on('hidden.bs.collapse', function (e) {     //for accordion*/  
	/*jQuery('#tab2mapoptions,#tabmaprequired,#tabmapoptions').on('show.bs.tab', function (e) {*/
	jQuery('[data-toggle="tab"]').on('shown.bs.tab', function (e) {
	        var target = $(e.target).attr("href") // activated tab
		if(target=='#tabmapoptions' || target=='#tabblank'){
			 //Hide all markers
			for (var i=0;i<window.markers.length;i++){
			    window.markers[i].setVisible(false);
			};
		}else if(target=='#tabtimeseriesoptions'){
			var point_id,LongLat,Lat,Long,latlong;
			$('.point').each(function() {
			    point_id = parseFloat($(this).attr('id').split('point')[1]);
			    if ($(this).css('display') == 'block' && $('#check' + String(point_id)).is(':checked')){
				LongLat = String($('#p' + String(point_id)).val()).replace(' ','');
				Long = parseFloat(LongLat.split(',')[0]);
				Lat = parseFloat(LongLat.split(',')[1]);
				latlong = new google.maps.LatLng(Lat,Long);
				//Update marker on map
				window.markers[point_id-1].position = latlong;
				window.markers[point_id-1].setVisible(true);
			    };
			});
		};
	});


	jQuery('#accordionDOWNMAP').on('hidden.bs.collapse', function (e) {  
		        rectangle.setMap(null);
	});
	jQuery('#accordionDOWNMAP').on('shown.bs.collapse', function (e) {  
		        rectangle.setMap(window.map);
	});

	/*--------------------------------------------*/
	/*--                                         --*/
	/*--------------------------------------------*/
	jQuery('#variableT').on('change', function(){
	     variable=document.getElementById('variableT').value;
	     document.getElementById('variable').value =variable;
             if(variable=='Gpet'||variable=='Gpr'||variable=='Gwb'){
	     	//document.getElementById('chartType').value ='column';
                jQuery('.prpetwb').css("display",'inline');
	     }else{
	     	//document.getElementById('chartType').value ='spline';
                jQuery('.prpetwb').css("display",'none');
	    }
	     	document.getElementById('mapid').value ='';
	     	document.getElementById('token').value ='';
	});
	jQuery('#variable').on('change', function(){
	     variable=document.getElementById('variable').value;
	     document.getElementById('variableT').value =variable;
             if(variable=='Gpet'||variable=='Gpr'||variable=='Gwb'){
	     	//document.getElementById('chartType').value ='column';
                jQuery('.prpetwb').css("display",'inline');
	     }else{
	     	//document.getElementById('chartType').value ='spline';
                jQuery('.prpetwb').css('display','none');
	    }
	});

 	jQuery('#mapCenterLongLat').keyup( function(){
		var mapCenterLongLat = document.getElementById('mapCenterLongLat').value;
            	var mapCenterLong = parseFloat(mapCenterLongLat.split(',')[0]).toFixed(4);
            	var mapCenterLat = parseFloat(mapCenterLongLat.split(',')[1]).toFixed(4);
		window.map.setCenter(new google.maps.LatLng(mapCenterLat,mapCenterLong));
        });
	jQuery('#mapzoom').on('change', function(){
		mapzoom = parseInt(document.getElementById('mapzoom').value)
		window.map.setZoom(mapzoom);
        });
	jQuery('#unitsT').on('change', function(){
	     units=document.getElementById('unitsT').value;
	     document.getElementById('units').value =units;
        });
	jQuery('#units').on('change', function(){
	     units=document.getElementById('units').value;
	     document.getElementById('unitsT').value =units;
        });


/*       jQuery('#mapzoom).on('change',function(){

          //Update sharelink
          var sL = document.getElementById('sL').value;
          var sL_new = sL.replace(/mapzoom=\d+/m,'mapzoom=' + String(myZoom));
          sL_new = sL_new.replace(/mapCenterLongLat=([\-\d.]+),([\d.]+)/m,'mapCenterLongLat=' + LongLat);
          document.getElementById('shareLink').value = sL_new;
                google.maps.event.addListener(map,'center_changed',function(){
                        var newCenter = window.map.getCenter();
                        myCenterLat = newCenter.lat().toFixed(4);
                        myCenterLong = newCenter.lng().toFixed(4);
            var LongLat = String(myCenterLong)+','+String(myCenterLat);
            var latlong = new google.maps.LatLng(myCenterLat,myCenterLong);
                        document.getElementById('mapCenterLongLat').value = LongLat;
            });
            //Update sharelink
            var sL = document.getElementById('sL').value;
            var sL_new = sL.replace(/mapCenterLongLat=([\-\d.]+),([\d.]+)/m,'mapCenterLongLat=' + LongLat);

            document.getElementById('shareLink').value = sL_new;


        });
*/



	/*--------------------------------------------*/
        /*       DATE PICKER 			      */
	/*--------------------------------------------*/
    jQuery('.variable,.variableT').on('change', function(){
        //strip product character off of variable
        var variable = jQuery('.variable').val();
        var product = variable.substr(0,1);
	document.getElementById('product').value =product; 
	
        var minDate,maxDate,yearRange;

        thisDate = new Date();
        thisDate.setDate(thisDate.getDate()-2); //2 day lag on data
        year = thisDate.getFullYear();
        mm = thisDate.getMonth()+1; //Jan is 0
        dd = thisDate.getDate();
        if(dd<10){
           dd='0'+dd;
        }
        if(mm<10){
           mm='0'+mm;
        }
        todayDate=year+'-'+mm+'-'+dd;
	$('.landsat5').css('display','none');
	$('.landsat8').css('display','none');
	$('.modis').css('display','none');
	$('.gridmet').css('display','none');
        if(product=='G'){
            minYear = "1979";
            maxYear = year; 
	    minDate="1979-01-01";
	    maxDate=todayDate;
	    document.getElementById('yearEndClim').value =maxYear; //let's not change the end date each time.. saved
	    $('.gridmet').css('display','inline');
        }
        else if (product=='8'){
            minYear = "2013";
            maxYear = year; 
	    minDate="2013-04-07";
	    maxDate=todayDate;
            //$('#dateStart').val(minDate);
            //$('#dateEnd').val(maxDate);
	  document.getElementById('yearEndClim').value =maxYear; //let's not change the end date each time.. saved
	    $('.landsat8').css('display','inline');
        }
        else if (product=='5'){
            minYear = "1984";
            maxYear = "2011";
	    minDate="1984-01-01";
	    maxDate="2011-11-01";
            //$('#dateStart').val(minDate);
            //$('#dateEnd').val(maxDate);
	  document.getElementById('yearEndClim').value =maxYear; //let's not change the end date each time.. saved
	    $('.landsat5').css('display','inline');
        }
        else if (product=='M'){
            minYear = "2000";
            maxYear = year; 
	    minDate="2000-02-24";
	    maxDate=todayDate;
	    document.getElementById('yearEndClim').value =maxYear; //let's not change the end date each time.. saved
	    $('.modis').css('display','inline');
        }
        yearRange = minYear + ':'+maxYear;

        $('#minYear').val(minYear);
        $('#maxYear').val(maxYear);

        $('.dateStart').datepicker( "option", "minDate", minDate);
        $('.dateStart').datepicker( "option", "maxDate", maxDate);
        $('.dateStart').datepicker( "option", "yearRange", yearRange);

        $('.dateEnd').datepicker( "option", "minDate", minDate);
        $('.dateEnd').datepicker( "option", "maxDate", maxDate);
        $('.dateEnd').datepicker( "option", "yearRange",yearRange);
        $('.dateEnd').datepicker( "option", "maxDate", maxDate);

	document.getElementById('yearStartClim').value =minYear;
	//document.getElementById('yearEndClim').value =maxYear; //let's not change the end date each time.. saved
        
    });

    jQuery('.calculation').on('change', function(){
	  var calculation = jQuery('.calculation').val()
          if(calculation=='value'){
                 jQuery('.climatologyYears').hide();
	  }else{
                 jQuery('.climatologyYears').show();
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
	 //jQuery('#state').on('change', function(){
//		var longitude=map.LatLng.lng().toFixed(4) 
//		var latitude=map.LatLng.lat().toFixed(4) 
//          	document.getElementById("mapCenterLatLong").value = longitude+','+latitude;
 //         	document.getElementById("mapzoom").value = '6';
//		
//	});

	/*--------------------------------------------*/
	/*        TIMESERIES  LISTENER 		      */
	/*--------------------------------------------*/
        jQuery('#timeSeriesCalc').on('change', function(){
            if(jQuery(this).val()=='season'){
                 jQuery('.seasontimeperiod').show();
                 jQuery('.daytimeperiod').hide();

	    }
            else if(jQuery(this).val()=='days'){
                 jQuery('.seasontimeperiod').hide();
                 jQuery('.daytimeperiod').show();

	    }
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
