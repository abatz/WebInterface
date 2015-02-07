$(function(){

	jQuery('#chartType').on('change', function(){
	     chartType=document.getElementById('chartType').value;
  	     generateHighChartFigure(series_data,'#container',chartType,title,subtitle,dateStart,dateEnd,
			yLabel,legendTitle,axis_min,variableShortName_time,varUnits);
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
		point_id = parseFloat($(this).val());
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
			point_id = parseFloat($(this).attr('id').split('point')[1]);
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
		var next_point_id = parseFloat($(this).attr('id').split('pl')[1]);
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
		var point_id = parseFloat($(this).attr('id').split('mi')[1]);
		//Find last marker and show the plus sign on that marker
		idx = point_id -1;
		if (String(point_id)== '1' ||  String(point_id) == 7){
		    while ($('#point' + idx).css('display') == 'none' ){
			idx-=1;
		    }
		}
		$('#pl' + String(idx +1)).css('display','inline')
		//Hide this point
		$('#point' + String(point_id)).css('display','none');
		//Hide this marker
		window.markers[point_id - 1].setVisible(false);
		$('#p' + String(point_id) + 'check').val('');
	    });
	    //onsubmit of form , update pointsLongLat
	    //This function is called in templates/includes/timeseriesoptions.html on form_map submit
	    jQuery('#form_map').submit(function( event ) {
		if ( $('#domainType').val() == 'points') {
		    var LongLatStr = '';
		    $('.point').each(function() {
			point_id = parseFloat($(this).attr('id').split('point')[1]);
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

/* This does not work well for autocomplete
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
                window.kmlmarkerOverLayer.setMap(window.map);
	});
*/
	/*--------------------------------------------*/
	/*--                                         --*/
	/*--------------------------------------------*/
	jQuery('#variableT').on('change', function(){
	     variable=document.getElementById('variableT').value;
	     document.getElementById('variable').value =variable;
             //if(variable=='Gpet'||variable=='Gpr'||variable=='Gwb'){
	     //	document.getElementById('chartType').value ='column';
	     //}else{
	    // 	document.getElementById('chartType').value ='spline';
	    //}
	});
	jQuery('#variable').on('change', function(){
	     variable=document.getElementById('variable').value;
	     document.getElementById('variableT').value =variable;
             //if(variable=='Gpet'||variable=='Gpr'||variable=='Gwb'){
	    // 	document.getElementById('chartType').value ='column';
	     //}else{
	    // 	document.getElementById('chartType').value ='spline';
	    //}
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

	jQuery('#minColorbar,#maxColorbar').keyup( function(){
                colorbarsize = parseInt(document.getElementById('colorbarsize').value);
                colorbarmap = document.getElementById('colorbarmap').value;

                minColorbar = document.getElementById('minColorbar').value
                maxColorbar = document.getElementById('maxColorbar').value

                myPalette=colorbrewer[colorbarmap][colorbarsize];

                myScale = d3.scale.quantile().range(myPalette).domain([minColorbar,maxColorbar]);
                colorbar1 = Colorbar()
                   .thickness(30)
                    .barlength(300)
                    .orient("horizontal")
                    .scale(myScale)
                colorbarObject1 = d3.select("#colorbar1").call(colorbar1)
        });
       jQuery('#colorbarmap, #colorbarsize').on('change', function(){
                colorbarsize = parseInt(document.getElementById('colorbarsize').value);
                colorbarmap = document.getElementById('colorbarmap').value;

                minColorbar = document.getElementById('minColorbar').value;
                maxColorbar = document.getElementById('maxColorbar').value;

                myPalette=colorbrewer[colorbarmap][colorbarsize];

                myScale = d3.scale.quantile().range(myPalette).domain([minColorbar,maxColorbar]);
                colorbar1 = Colorbar()
                   .thickness(30)
                    .barlength(300)
                    .orient("horizontal")
                    .scale(myScale)
                colorbarObject1 = d3.select("#colorbar1").call(colorbar1)

		var palette = new String();
                palette=myPalette[0].replace(/#/g, '');
                for (var i=1;i<myPalette.length;i++){
                        palette = palette+','+myPalette[i].replace(/#/g, '');
                }
                jQuery('#palette').val(palette);


        });



	/*--------------------------------------------*/
	/*       COLORBAR       		      */
	/*--------------------------------------------*/
    jQuery('.variable,.variableT').on('change', function(){
        //strip product character off of variable
        var variable = jQuery('.variable').val();
        var product = variable.substr(0,1);
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
       console.log(todayDate)
        if(product=='G'){
            minYear = "1979";
            maxYear = year; 
	    minDate="1979-01-01";
	    maxDate=todayDate;
        }
        else if (product=='8'){
            minYear = "2013";
            maxYear = year; 
	    minDate="2013-04-07";
	    maxDate=todayDate;
            $('#dateStart').val(minDate);
            $('#dateEnd').val(maxDate);
        }
        else if (product=='5'){
            minYear = "1984";
            maxYear = "2012";
	    minDate="1984-01-01";
	    maxDate="2012-05-08";
            $('#dateStart').val(minDate);
            $('#dateEnd').val(maxDate);
        }
        else if (product=='M'){
            minYear = "2000";
            maxYear = year; 
	    minDate="2000-02-24";
	    maxDate=todayDate;
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

    jQuery('.anomOrValue').on('change', function(){
	  var anomOrValue = jQuery('.anomOrValue').val()
          if(anomOrValue=='value'){
                 jQuery('.climatologyYears').hide();
	  }else{
                 jQuery('.climatologyYears').show();
 	  }
    });

    jQuery('.variable, .variableT,.anomOrValue, .units').on('change', function(){
	   
	   //strip product character off of variable
	   var variable = jQuery('.variable').val()
	   variable = variable.substr(1)
	   var anomOrValue = jQuery('.anomOrValue').val()
	   var units = jQuery('.units').val()

           if(variable=='NDVI' || variable=='EVI' ){
                statistic='Median';
           	if(jQuery('.anomOrValue').val()=='anom'){
			minColorbar = -.4;
			maxColorbar = .4;
			palette="A50026,D73027,F46D43,FDAE61,FEE08B,FFFFBF,D9EF8B,A6D96A,66BD63,1A9850,006837"
			colorbarmap='RdYlGn'
			colorbarsize=8
			varUnits=''
		}else{
			minColorbar = -.1;
			maxColorbar = .9;
			palette="FFFFE5,F7FCB9,D9F0A3,ADDD8E,93D284,78C679,41AB5D,238443,006837,004529"
			colorbarmap='YlGn'
			colorbarsize=9
			varUnits=''
		}
           }else if(variable=='NDSI' || variable=='NDWI'){
                statistic='Median';
		if(anomOrValue=='anom'){
                        minColorbar = -.5;
                        maxColorbar = .5;
                        palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
			colorbarmap='RdYlBu' 
			colorbarsize=8
			varUnits=''
                }else{
                        minColorbar = -.2;
                        maxColorbar = .7;
                        palette="08306B,08519C,2171B5,4292C6,6BAED6,9ECAE1,C6DBEF,DEEBF7,F7FBFF"
			colorbarmap='invBlues'  //need inverse here
			colorbarsize=8
			varUnits=''
                }
	   }else if(variable=='pr'){
                 statistic='Total';
                 if(anomOrValue=='anom'){
			minColorbar = 0;
			maxColorbar = 200;
                        palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
			colorbarmap='RdYlBu' 
			colorbarsize=8
			varUnits='%'
                }else{
                 	if(units=='metric'){
				minColorbar = 0;
				maxColorbar = 400; //mm
				varUnits='mm'
                 	}else if(units=='english'){
				minColorbar = 0;
				maxColorbar = 16; //in
				varUnits='in'
			}
                        palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,41B6C4,1D91C0,225EA8,0C2C84"
			colorbarmap='YlGnBu' 
			colorbarsize=8
                }
            }else if(variable=='tmmx' || variable=='tmmn' || variable=='tmean'){
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                 	if(units=='metric'){
				minColorbar =-5;
				maxColorbar = 5;
				varUnits='deg C'
                 	}else if(units=='english'){
				minColorbar =-10;
				maxColorbar = 10;
				varUnits='deg F'
			}
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuYlRd' 
			colorbarsize=8
                }else if ( variable=='tmmx'){
                 	if(units=='metric'){
				minColorbar = -20;
				maxColorbar = 30;
				varUnits='deg C'
                 	}else if(units=='english'){
				minColorbar =0;
				maxColorbar = 100;
				varUnits='deg F'
			}
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }else if ( variable=='tmmn'){
                 	if(units=='metric'){
				minColorbar = -20;
				maxColorbar = 20; //deg C
				varUnits='deg C'
                 	}else if(units=='english'){
				minColorbar = 0;
				maxColorbar = 80; //deg F 
				varUnits='deg F'
			}
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
		}else if ( variable=='tmean'){
                        if(units=='metric'){
                                minColorbar = -20;
                                maxColorbar = 20; //deg C
				varUnits='deg C'
                        }else if(units=='english'){
                                minColorbar = 0;
                                maxColorbar = 80; //deg F
				varUnits='deg F'
                        }
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
                        colorbarmap='BuRd' //need inverse
                        colorbarsize=8
                }
	    }else if(variable=='rmin' || variable=='rmax'){
                 statistic='Mean';
                 if(variable=='anom'){
                        minColorbar =-25;
                        maxColorbar = 25;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
			varUnits='%'
                }else{
                        minColorbar =0 ;
                        maxColorbar = 100; ///%
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
			varUnits='%'
                }
	    }else if(variable=='srad'){
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                        minColorbar =-25;
                        maxColorbar = 25;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
			varUnits='W/m2'
                }else{
                        minColorbar =100 ;
                        maxColorbar = 350; ///W/m2
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
			varUnits='W/m2'
                }
	    }else if(variable=='vs'){
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                 	if(units=='metric'){
				minColorbar =-2.5;
				maxColorbar = 2.5;
				varUnits='m/s';
                 	}else if(units=='english'){
				minColorbar =-5;
				maxColorbar = 5;
				varUnits='mi/hr';
			}
                        palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
                }else{ 
                 	if(units=='metric'){
				minColorbar = 0;
				maxColorbar = 5; //m/s
				varUnits='m/s';
                 	}else if(units=='english'){
				minColorbar = 0;
				maxColorbar = 10; //mi/hr
				varUnits='mi/hr';
			}
                        palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,5DC2C1,41B6C4,1D91C0,225EA8,253494,081D58"
			colorbarmap='YlGnBu' //need inverse
			colorbarsize=8
                }
	 }else if(variable=='sph'){
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                        minColorbar =-30;
                        maxColorbar = 30;
                        palette="053061,2166AC,4393C3,67ADD1,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,E88465,D6604D,B2182B,67001F"
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
			varUnits='kg/kg';
                }else{
                        minColorbar = 0;
                        maxColorbar = 0.02; //kg/kg
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026,D6604D,B2182B,67001F"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
			varUnits='kg/kg';
                }
	 }else if(variable=='erc'){
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                        minColorbar =-20;
                        maxColorbar = 20;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuYlRd' 
			colorbarsize=8
			varUnits='';
                }else{
                        minColorbar = 10;
                        maxColorbar = 120; //
                        palette="FFFFFF,FFFFCC,FFEDA0,FED976,FEB24C,FD8D3C,FC4E2A,E31A1C,BD0026,800026,000000"
			colorbarmap='YlOrRd' 
			colorbarsize=8
			varUnits='';
                }
         }else if(variable=='pet'){
                 statistic='Total';
                 if(anomOrValue=='anom'){
			minColorbar =80;
			maxColorbar =120;
                        palette="053061,2166AC,4393C3,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,D6604D,B2182B,67001F"
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
			varUnits='%';
                }else{
                 	if(units='metric'){
				minColorbar = 300;
				maxColorbar = 800; //mm
				varUnits='mm';
                 	}else if(units=='english'){
				minColorbar = 10;
				maxColorbar = 30; //in
				varUnits='in';
			}
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
         }else if(variable=='pdsi'){
                 statistic='Mean';
                 if(anomOrValue=='anom'){
			minColorbar =-6;
			maxColorbar =6;
                        palette="053061,2166AC,4393C3,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,D6604D,B2182B,67001F"
                        colorbarmap='RdYlBu' 
                        colorbarsize=8
			varUnits='';
                }else{
                        minColorbar = -6;
                        maxColorbar = 6; 
                        palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061";
                        colorbarmap='RdYlBu' //need inverse
                        colorbarsize=8
			varUnits='';
                }
	 }else if(variable=='wb'){
                 statistic='Total';
                 if(anomOrValue=='anom'){
                        minColorbar =-100;
                        maxColorbar = 100;
                        palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
			colorbarmap='RdYlBu' //need inverse
			colorbarsize=8
			varUnits='%';
                }else{
                 	if(units=='metric'){
				minColorbar = -200;
				maxColorbar = 200; //mm
				varUnits='mm';
                 	}else if(units=='english'){
				minColorbar = -10;
				maxColorbar = 10; //in
				varUnits='in';
			}
                        palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
			colorbarmap='RdBu' //need inverse
			colorbarsize=8
                }   
	     }
	     document.getElementById('minColorbar').value =minColorbar;
	     document.getElementById('maxColorbar').value =maxColorbar 
	     document.getElementById('palette').value =palette;
	     document.getElementById('colorbarmap').value =colorbarmap;
	     document.getElementById('colorbarsize').value =colorbarsize;
	     document.getElementById('varUnits').value =varUnits;
	     document.getElementById('statisticChoice').value =statistic;

             colorbarsize = parseInt(document.getElementById('colorbarsize').value);
             colorbarmap = document.getElementById('colorbarmap').value;

             minColorbar = document.getElementById('minColorbar').value
             maxColorbar = document.getElementById('maxColorbar').value

             myPalette=colorbrewer[colorbarmap][colorbarsize];

             myScale = d3.scale.quantile().range(myPalette).domain([minColorbar,maxColorbar]);
             colorbar1 = Colorbar()
                   .thickness(30)
                    .barlength(300)
                    .orient("horizontal")
                    .scale(myScale)
             colorbarObject1 = d3.select("#colorbar1").call(colorbar1)

 	     var palette = new String();
             palette=myPalette[0].replace(/#/g, '');
             for (var i=1;i<myPalette.length;i++){
                    palette = palette+','+myPalette[i].replace(/#/g, '');
            }
            jQuery('#palette').val(palette);
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
