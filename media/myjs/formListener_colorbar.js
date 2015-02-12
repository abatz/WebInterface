$(function(){

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
	/*       COLORBAR OPTIONS      		      */
	/*--------------------------------------------*/
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
			colorbarmap='RdYlGn'
			colorbarsize=8
			varUnits=''
		}else{
			minColorbar = -.1;
			maxColorbar = .9;
			colorbarmap='YlGn'
			colorbarsize=9
			varUnits=''
		}
           }else if(variable=='NDSI' || variable=='NDWI'){
                statistic='Median';
		if(anomOrValue=='anom'){
                        minColorbar = -.5;
                        maxColorbar = .5;
			colorbarmap='RdYlBu' 
			colorbarsize=8
			varUnits=''
                }else{
                        minColorbar = -.2;
                        maxColorbar = .7;
			colorbarmap='invBlues'  //need inverse here
			colorbarsize=8
			varUnits=''
                }
	   }else if(variable=='pr'){
                 statistic='Total';
                 if(anomOrValue=='anompercentof'){
			minColorbar = 0;
			maxColorbar = 200;
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
			colorbarmap='BuYlRd' 
			colorbarsize=8
                }else if ( variable=='tmmx'){
                 	if(units=='metric'){
				minColorbar = -5;
				maxColorbar = 35;
				varUnits='deg C'
                 	}else if(units=='english'){
				minColorbar =20;
				maxColorbar = 100;
				varUnits='deg F'
			}
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }else if ( variable=='tmmn'){
                 	if(units=='metric'){
				minColorbar = -20;
				maxColorbar = 25; //deg C
				varUnits='deg C'
                 	}else if(units=='english'){
				minColorbar = 0;
				maxColorbar = 80; //deg F 
				varUnits='deg F'
			}
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
                        colorbarmap='BuRd' //need inverse
                        colorbarsize=8
                }
	    }else if(variable=='rmin' || variable=='rmax'){
                 statistic='Mean';
                 if(variable=='anom'){
                        minColorbar =-15;
                        maxColorbar = 15;
			colorbarmap='BrBG' //need inverse
			colorbarsize=9
			varUnits='%'
                }else{
                        minColorbar =0 ;
                        maxColorbar = 100; ///%
			colorbarmap='BrBG' //need inverse
			colorbarsize=8
			varUnits='%'
                }
	    }else if(variable=='srad'){
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                        minColorbar =-25;
                        maxColorbar = 25;
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
			varUnits='W/m2'
                }else{
                        minColorbar =100 ;
                        maxColorbar = 350; ///W/m2
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
			colorbarmap='YlGnBu' //need inverse
			colorbarsize=8
                }
	 }else if(variable=='sph'){
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                        minColorbar =-30;
                        maxColorbar = 30;
			colorbarmap='BuYlRd' //need inverse
			colorbarsize=8
			varUnits='kg/kg';
                }else{
                        minColorbar = 0;
                        maxColorbar = 0.02; //kg/kg
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
			varUnits='kg/kg';
                }
	 }else if(variable=='erc'){
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                        minColorbar =-20;
                        maxColorbar = 20;
			colorbarmap='BuYlRd' 
			colorbarsize=8
			varUnits='';
                }else{
                        minColorbar = 10;
                        maxColorbar = 120; //
			colorbarmap='YlOrRd' 
			colorbarsize=8
			varUnits='';
                }
         }else if(variable=='pet'){
                 statistic='Total';
                 if(anomOrValue=='anom'){
			minColorbar =80;
			maxColorbar =120;
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
			colorbarmap='BuRd' //need inverse
			colorbarsize=8
                }
         }else if(variable=='pdsi'){
                 statistic='Mean';
                 if(anomOrValue=='anom'){
			minColorbar =-6;
			maxColorbar =6;
                        colorbarmap='RdYlBu' 
                        colorbarsize=8
			varUnits='';
                }else{
                        minColorbar = -6;
                        maxColorbar = 6; 
                        colorbarmap='RdYlBu' //need inverse
                        colorbarsize=8
			varUnits='';
                }
	 }else if(variable=='wb'){
                 statistic='Total';
                 if(anomOrValue=='anom'){
                        minColorbar =-100;
                        maxColorbar = 100;
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

});
