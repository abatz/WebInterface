$(function(){
	/*--------------------------------------------*/
	/*         POINTS LISTENERS                    */
	/*--------------------------------------------*/
    /*Show markesr only of time series option is expanded*/
     $('#accordionBUILDTIMESERIES').on('shown.bs.collapse', function (e) {
        //Show markers
       var point_id;
        $('.point').each(function() {
            point_id = parseFloat($(this).attr('id').split('point')[1]);
            if ($(this).css('display') == 'block' && $('#check' + String(point_id)).is(':checked')){
                //Update marker on map
                window.markers[point_id-1].setVisible(true);
            }
        });
    });
    $('#accordionBUILDTIMESERIES').on('hidden.bs.collapse', function (e) {
        //Hide all markers
        for (var i=0;i<window.markers.length;i++){
            window.markers[i].setVisible(false);
        }
    }); 
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
		if($('input[id=stateoverlayer]:checked').val()=="stateoverlayer"){
			 window.statemarkerOverLayer.setMap(window.map);
		}else{
		  	window.statemarkerOverLayer.setMap(null);
		};
		if($('input[id=countyoverlayer]:checked').val()=="countyoverlayer"){
		  	window.countymarkerOverLayer.setMap(window.map);
		}else{
		  	window.countymarkerOverLayer.setMap(null);
		};
		if($('input[id=hucoverlayer]:checked').val()=="hucoverlayer"){
                  	window.hucsmarkerOverLayer.setMap(window.map);
                }else{
                 	 window.hucsmarkerOverLayer.setMap(null);
                };
		if($('input[id=climatedivoverlayer]:checked').val()=="climatedivoverlayer"){
                  	window.climatedivmarkerOverLayer.setMap(window.map);
                }else{
                  	window.climatedivmarkerOverLayer.setMap(null);
                };
		if($('input[id=psaoverlayer]:checked').val()=="psaoverlayer"){
                  	window.psasmarkerOverLayer.setMap(window.map);
                }else{
                  	window.psasmarkerOverLayer.setMap(null);
                };
		if($('input[id=kmloverlayer]:checked').val()=="kmloverlayer"){
			kmlurl=document.getElementById('kmlurl').value;
			window.kmlmarkerLayer = new google.maps.KmlLayer(kmlurl, {
				map:map,
			    preserveViewport: true,
			    suppressInfoWindows: false
			 });
		  	window.kmlmarkerLayer.setMap(window.map);
		}else{
		  	window.kmlmarkerLayer.setMap(null);
		};
	});


 	jQuery('#kmlurl').keyup( function(){
		winndow.kmlmarkerLayer = new google.maps.KmlLayer('{{ kmlurl }}', {
                        map:map,
                            preserveViewport: true,
                            suppressInfoWindows: false
                });
                window.kmlmarkerLayer.setMap(window.map);
});
	/*--------------------------------------------*/
	/*         BACKGROUND LISTENER                */
	/*--------------------------------------------*/
	 jQuery('.backgroundgmap').on('change','input[type=checkbox]', function(){
                if($('input[id=whitebackground]:checked').val()=="whitebackground"){
			window.map.setOptions({styles: window.mapOffStyles});
                }else{
                	window.map.setOptions({styles: window.mapOnStyles});
                };
	});

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

 	jQuery('#mapCenterLongLat').keyup( function(){
		var mapCenterLongLat = document.getElementById('mapCenterLongLat').value;
            	var mapCenterLong = parseFloat(mapCenterLongLat.split(',')[0]).toFixed(4);;
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
		console.log('changed')
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
		console.log('changed')
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
    jQuery('.variable').on('change', function(){
        //strip product character off of variable
        var variable = jQuery('.variable').val();
        product = variable.substr(0,1);
        minYear = "1979";
        if(product=='G'){
            minYear = "1979";
        }
        else if (product=='L'){
            minYear = "1972";
        }
        else if (product=='M'){
            minYear = "1999";
        }
        document.getElementById('minYear').value = minYear;
    });

    jQuery('.variable, .anomOrValue, .units').on('change', function(){
	   
	   //strip product character off of variable
	   var variable = jQuery('.variable').val()
	   variable = variable.substr(1)
	   var anomOrValue = jQuery('.anomOrValue').val()
	   var units = jQuery('.units').val()

           if(variable=='NDVI' || variable=='EVI' ){
           	if(jQuery('.anomOrValue').val()=='anom'){
			minColorbar = -.4;
			maxColorbar = .4;
			palette="A50026,D73027,F46D43,FDAE61,FEE08B,FFFFBF,D9EF8B,A6D96A,66BD63,1A9850,006837"
			colorbarmap='RdYlGn'
			colorbarsize=8
		}else{
			minColorbar = -.1;
			maxColorbar = .9;
			palette="FFFFE5,F7FCB9,D9F0A3,ADDD8E,93D284,78C679,41AB5D,238443,006837,004529"
			colorbarmap='YlGn'
			colorbarsize=9
		}
           }else if(variable=='NDSI' || variable=='NDWI'){
		 if(anomOrValue=='anom'){
                        minColorbar = -.5;
                        maxColorbar = .5;
                        palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
			colorbarmap='RdYlBu' 
			colorbarsize=8
                }else{
                        minColorbar = -.2;
                        maxColorbar = .7;
                        palette="08306B,08519C,2171B5,4292C6,6BAED6,9ECAE1,C6DBEF,DEEBF7,F7FBFF"
			colorbarmap='invBlues'  //need inverse here
			colorbarsize=8
                }
	   }else if(variable=='pr'){
                 if(anomOrValue=='anom'){
			minColorbar = 0;
			maxColorbar = 200;
                        palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
			colorbarmap='RdYlBu' 
			colorbarsize=8
                }else{
                 	if(units=='metric'){
				minColorbar = 0;
				maxColorbar = 400; //mm
                 	}else if(units=='english'){
				minColorbar = 0;
				maxColorbar = 16; //mm
			}
                        palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,41B6C4,1D91C0,225EA8,0C2C84"
			colorbarmap='YlGnBu' 
			colorbarsize=8
                }
            }else if(variable=='tmmx' || variable=='tmmn' || variable=='tmean'){
                 if(anomOrValue=='anom'){
                 	if(units=='metric'){
				minColorbar =-5;
				maxColorbar = 5;
                 	}else if(units=='english'){
				minColorbar =-10;
				maxColorbar = 10;
			}
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuYlRd' 
			colorbarsize=8
                }else if ( variable=='tmmx'){
                 	if(units=='metric'){
				minColorbar = -20;
				maxColorbar = 30;
                 	}else if(units=='english'){
				minColorbar =0;
				maxColorbar = 100;
			}
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }else if ( variable=='tmmn'){
                 	if(units=='metric'){
				minColorbar = -20;
				maxColorbar = 20; //deg C
                 	}else if(units=='english'){
				minColorbar = 0;
				maxColorbar = 80; //deg C
			}
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
		}else if ( variable=='tmean'){
                        if(units=='metric'){
                                minColorbar = -20;
                                maxColorbar = 20; //deg C
                        }else if(units=='english'){
                                minColorbar = 0;
                                maxColorbar = 80; //deg C
                        }
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
                        colorbarmap='BuRd' //need inverse
                        colorbarsize=8
                }
	    }else if(variable=='rmin' || variable=='rmax'){
                 if(variable=='anom'){
                        minColorbar =-25;
                        maxColorbar = 25;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
                }else{
                        minColorbar =0 ;
                        maxColorbar = 100; ///%
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
	    }else if(variable=='srad'){
                 if(anomOrValue=='anom'){
                        minColorbar =-25;
                        maxColorbar = 25;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
                }else{
                        minColorbar =100 ;
                        maxColorbar = 350; ///W/m2
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
	    }else if(variable=='vs'){
                 if(anomOrValue=='anom'){
                 	if(units=='metric'){
				minColorbar =-2.5;
				maxColorbar = 2.5;
                 	}else if(units=='english'){
				minColorbar =-5;
				maxColorbar = 5;
			}
                        palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
                }else{ 
                 	if(units=='metric'){
				minColorbar = 0;
				maxColorbar = 5; //m/s
                 	}else if(units=='english'){
				minColorbar = 0;
				maxColorbar = 10; //mi/hr
			}
                        palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,5DC2C1,41B6C4,1D91C0,225EA8,253494,081D58"
			colorbarmap='YlGnBu' //need inverse
			colorbarsize=8
                }
	 }else if(variable=='sph'){
                 if(anomOrValue=='anom'){
                        minColorbar =-30;
                        maxColorbar = 30;
                        palette="053061,2166AC,4393C3,67ADD1,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,E88465,D6604D,B2182B,67001F"
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
                }else{
                        minColorbar = 0;
                        maxColorbar = 0.02; //kg/kg
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026,D6604D,B2182B,67001F"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
	 }else if(variable=='erc'){
                 if(anomOrValue=='anom'){
                        minColorbar =-20;
                        maxColorbar = 20;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuYlRd' 
			colorbarsize=8
                }else{
                        minColorbar = 10;
                        maxColorbar = 120; //
                        palette="FFFFFF,FFFFCC,FFEDA0,FED976,FEB24C,FD8D3C,FC4E2A,E31A1C,BD0026,800026,000000"
			colorbarmap='YlOrRd' 
			colorbarsize=8
                }
         }else if(variable=='pet'){
                 if(anomOrValue=='anom'){
			minColorbar =80;
			maxColorbar =120;
                        palette="053061,2166AC,4393C3,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,D6604D,B2182B,67001F"
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
                }else{
                 	if(units='metric'){
				minColorbar = 300;
				maxColorbar = 800; //mm
                 	}else if(units=='english'){
				minColorbar = 10;
				maxColorbar = 30; //mm
			}
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
         }else if(variable=='pdsi'){
                 if(anomOrValue=='anom'){
			minColorbar =-6;
			maxColorbar =6;
                        palette="053061,2166AC,4393C3,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,D6604D,B2182B,67001F"
                        colorbarmap='RdYlBu' 
                        colorbarsize=8
                }else{
                        minColorbar = -6;
                        maxColorbar = 6; 
                        palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061";
                        colorbarmap='RdYlBu' //need inverse
                        colorbarsize=8
                }
	 }else if(variable=='wb'){
                 if(anomOrValue=='anom'){
                        minColorbar =-100;
                        maxColorbar = 100;
                        palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
			colorbarmap='RdYlBu' //need inverse
			colorbarsize=8
                }else{
                 	if(units=='metric'){
				minColorbar = -200;
				maxColorbar = 200; //mm
                 	}else if(units=='english'){
				minColorbar = -10;
				maxColorbar = 10; //mm
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
