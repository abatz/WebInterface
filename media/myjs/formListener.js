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

 	jQuery('#mapCenterLongLat').keyup( function(){
		var mapCenterLongLat = document.getElementById('mapCenterLongLat').value;
            	var mapCenterLong = parseFloat(mapCenterLongLat.split(',')[0]);
            	var mapCenterLat = parseFloat(mapCenterLongLat.split(',')[1]);
		window.map.setCenter(new google.maps.LatLng(mapCenterLat,mapCenterLong));
        });
	jQuery('#mapzoom').on('change', function(){
		mapzoom = parseInt(document.getElementById('mapzoom').value)
		window.map.setZoom(mapzoom);
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
        });



	/*--------------------------------------------*/
	/*       COLORBAR       		      */
	/*--------------------------------------------*/
       jQuery('.basicvariable, .anomOrValue').on('change', function(){
           if(jQuery('.basicvariable').val()=='NDVI' || jQuery('.basicvariable').val()=='EVI' ){
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
           }else if(jQuery('.basicvariable').val()=='NDSI' || jQuery('.basicvariable').val()=='NDWI'){
		 if(jQuery('.anomOrValue').val()=='anom'){
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
	   }else if(jQuery('.basicvariable').val()=='pr'){
                 if(jQuery('.anomOrValue').val()=='anom'){
                        minColorbar = 0;
                        maxColorbar = 200;
                        palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
			colorbarmap='RdBu' 
			colorbarsize=8
                }else{
                        minColorbar = 0;
                        maxColorbar = 400; //mm
                        palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,41B6C4,1D91C0,225EA8,0C2C84"
			colorbarmap='YlGnBu' 
			colorbarsize=8
                }
            }else if(jQuery('.basicvariable').val()=='tmmx' || jQuery('.basicvariable').val()=='tmmn'){
                 if(jQuery('.anomOrValue').val()=='anom'){
                        minColorbar =-5;
                        maxColorbar = 5;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse 
			colorbarsize=8
                }else if ( jQuery('.basicvariable').val()=='tmmx'){
                        minColorbar = -20;
                        maxColorbar = 30;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }else if ( jQuery('.basicvariable').val()=='tmmn'){
                        minColorbar = -25;
                        maxColorbar = 25; //deg C
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
	    }else if(jQuery('.basicvariable').val()=='rmin' || jQuery('.basicvariable').val()=='rmax'){
                 if(jQuery('.anomOrValue').val()=='anom'){
                        minColorbar =-25;
                        maxColorbar = 25;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }else{
                        minColorbar =0 ;
                        maxColorbar = 100; ///%
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
	    }else if(jQuery('.basicvariable').val()=='srad'){
                 if(jQuery('.anomOrValue').val()=='anom'){
                        minColorbar =-25;
                        maxColorbar = 25;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }else{
                        minColorbar =100 ;
                        maxColorbar = 350; ///W/m2
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
	    }else if(jQuery('.basicvariable').val()=='vs'){
                 if(jQuery('.anomOrValue').val()=='anom'){
                        minColorbar =-2.5;
                        maxColorbar = 2.5;
                        palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
			colorbarmap='RdBu' //need inverse
			colorbarsize=8
                }else{ 
                        minColorbar = 0;
                        maxColorbar = 5; //m/s
                        palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,5DC2C1,41B6C4,1D91C0,225EA8,253494,081D58"
			colorbarmap='YlGnBu' //need inverse
			colorbarsize=8
                }
	 }else if(jQuery('.basicvariable').val()=='sph'){
                 if(jQuery('.anomOrValue').val()=='anom'){
                        minColorbar =-30;
                        maxColorbar = 30;
                        palette="053061,2166AC,4393C3,67ADD1,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,E88465,D6604D,B2182B,67001F"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }else{
                        minColorbar = 0;
                        maxColorbar = 0.02; //kg/kg
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026,D6604D,B2182B,67001F"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
	 }else if(jQuery('.basicvariable').val()=='erc'){
                 if(jQuery('.anomOrValue').val()=='anom'){
                        minColorbar =-20;
                        maxColorbar = 20;
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='YlRdBl' //need inverse
			colorbarsize=8
                }else{
                        minColorbar = 10;
                        maxColorbar = 120; //
                        palette="FFFFFF,FFFFCC,FFEDA0,FED976,FEB24C,FD8D3C,FC4E2A,E31A1C,BD0026,800026,000000"
			colorbarmap='YlOrRd' 
			colorbarsize=8
                }
         }else if(jQuery('.basicvariable').val()=='pet'){
                 if(jQuery('.anomOrValue').val()=='anom'){
                        minColorbar =80;
                        maxColorbar =120;
                        palette="053061,2166AC,4393C3,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,D6604D,B2182B,67001F"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }else{
                        minColorbar = 300;
                        maxColorbar = 800; //mm
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
         }else if(jQuery('.basicvariable').val()=='pdsi'){
                 if(jQuery('.anomOrValue').val()=='anom'){
                        minColorbar =-.4;
                        maxColorbar =.4;
                        palette="053061,2166AC,4393C3,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,D6604D,B2182B,67001F"
                        colorbarmap='RdBu' 
                        colorbarsize=8
                }else{
                        minColorbar = -3;
                        maxColorbar = 3; 
                        palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
                        colorbarmap='RdBu' //need inverse
                        colorbarsize=6
                }
	 }else if(jQuery('.basicvariable').val()=='wb'){
                 if(jQuery('.anomOrValue').val()=='anom'){
                        minColorbar =-100;
                        maxColorbar = 100;
                        palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
			colorbarmap='RdBu' //need inverse
			colorbarsize=8
                }else{
                        minColorbar = -200;
                        maxColorbar = 200; //mm
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
	/*        KML LAYER       		      */
	/*--------------------------------------------*/

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
	 //jQuery('#state').on('change', function(){
//		var longitude=map.LatLng.lng().toFixed(4) 
//		var latitude=map.LatLng.lat().toFixed(4) 
//          	document.getElementById("mapCenterLatLong").value = longitude+','+latitude;
 //         	document.getElementById("mapzoom").value = '6';
//		
//	});
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
