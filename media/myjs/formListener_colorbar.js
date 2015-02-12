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

});
