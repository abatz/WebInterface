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
        jQuery('.variable, .variableT,.anomOrValue, .units,.dateStart,.dateEnd').on('change', function(){
	   //strip product character off of variable
	   var variable = jQuery('.variable').val()
	   variable = variable.substr(1)
	   var anomOrValue = jQuery('.anomOrValue').val()
	   var units = jQuery('.units').val()

	   //Approx number of months in selection
	   var dateStart = new Date(document.getElementById('dateStart').value);
	   var dateEnd = new Date(document.getElementById('dateEnd').value);
	   numMonths = Math.ceil(Math.abs(dateEnd.getTime() - dateStart.getTime())/(1000*3600*24*30));

	   varUnits =''; 
	   if(variable=='NDVI' || variable=='EVI' ){
		variableShortName=variable;
                statistic='Median';
           	if(jQuery('.anomOrValue').val()=='anom'){
			minColorbar = -.4;
			maxColorbar = .4;
			colorbarmap='RdYlGn'
			colorbarsize=8
			varUnits=''
		}else if(anomOrValue=='value' || anomOrValue=='clim'){
			minColorbar = -.1;
			maxColorbar = .9;
			colorbarmap='YlGn'
			colorbarsize=9
			varUnits=''
		}
           }else if(variable=='NDSI' || variable=='NDWI'){
		variableShortName=variable;
                statistic='Median';
		if(anomOrValue=='anom'){
                        minColorbar = -.5;
                        maxColorbar = .5;
			colorbarmap='RdYlBu' 
			colorbarsize=8
			varUnits=''
                }else if(anomOrValue=='value' || anomOrValue=='clim'){
                        minColorbar = -.2;
                        maxColorbar = .7;
			colorbarmap='invBlues' 
			colorbarsize=8
			varUnits=''
                }
	   }else if(variable=='pr'){
		variableShortName='Precipitation';
                 statistic='Total';
                 if(anomOrValue=='anompercentof'){
			minColorbar = 75;
			maxColorbar = 125;
			colorbarmap='BrBG' 
			colorbarsize=9
			varUnits='%'
                 }else if(anomOrValue=='anompercentchange'){
			minColorbar =-100;
			maxColorbar = 100;
			colorbarmap='BrBG' 
			colorbarsize=9
			varUnits='%'
		}else if(anomOrValue=='anom') {
                 	if(units='metric'){
				minColorbar =-100*numMonths;
				maxColorbar =100*numMonths;
				varUnits='mm'
			}else if (units=='english'){
				minColorbar =-4*numMonths;
				maxColorbar =4*numMonths;
				varUnits='in'
			}
			colorbarmap='BrBG' 
			colorbarsize=9
                }else if(anomOrValue=='value' || anomOrValue=='clim'){
                 	if(units=='metric'){
				minColorbar = 0;
				maxColorbar = 200*numMonths; //mm
				varUnits='mm'
                 	}else if(units=='english'){
				minColorbar = 0;
				maxColorbar = 8*numMonths; //in
				varUnits='in'
			}
			colorbarmap='YlGnBu' 
			colorbarsize=8
                }
            }else if(variable=='tmmx' || variable=='tmmn' || variable=='tmean'){
		if(variable=='tmmx'){
			variableShortName='Max Temperature';
		}else if(variable=='tmmn'){
			variableShortName='Min Temperature';
		}else if(variable=='tmean'){
			variableShortName='Mean Temperature';
		}
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
		}else if(anomOrValue=='value' || anomOrValue=='clim'){
               	if ( variable=='tmmx'){
                 	if(units=='metric'){
				minColorbar = -5;
				maxColorbar = 35;
				varUnits='deg C'
                 	}else if(units=='english'){
				minColorbar =20;
				maxColorbar = 100;
				varUnits='deg F'
			}
			colorbarmap='BuRd'
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
			colorbarmap='BuRd' 
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
                        colorbarmap='BuRd' 
                        colorbarsize=8
                }
	     }
	    }else if(variable=='rmin' || variable=='rmax'){
		if(variable=='rmin'){
			variableShortName='Min Rel. Humidity';
		}else if (variable=='rmax'){
			variableShortName='Max Rel. Humidity';
		}
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                        minColorbar =-15;
                        maxColorbar = 15;
			colorbarmap='BrBG' 
			colorbarsize=9
			varUnits='%'
                }else if(anomOrValue=='value' || anomOrValue=='clim'){
                        minColorbar =0 ;
                        maxColorbar = 100; ///%
			colorbarmap='BrBG' 
			colorbarsize=8
			varUnits='%'
                }
	    }else if(variable=='srad'){
		variableShortName='Radiation';
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                        minColorbar =-20;
                        maxColorbar = 20;
			colorbarmap='BuYlRd' 
			colorbarsize=8
			varUnits='W/m2'
                }else if(anomOrValue=='value' || anomOrValue=='clim'){
                        minColorbar =50 ;
                        maxColorbar = 400; ///W/m2
			colorbarmap='YlOrRd' 
			colorbarsize=7
			varUnits='W/m2'
                }
	    }else if(variable=='vs'){
		variableShortName='Wind Speed';
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
			colorbarmap='BuYlRd' 
			colorbarsize=8
                }else if(anomOrValue=='value' || anomOrValue=='clim'){ 
                 	if(units=='metric'){
				minColorbar = 0;
				maxColorbar = 8; //m/s
				varUnits='m/s';
                 	}else if(units=='english'){
				minColorbar = 0;
				maxColorbar = 10; //mi/hr
				varUnits='mi/hr';
			}
			colorbarmap='YlGnBu' 
			colorbarsize=8
                }
	 }else if(variable=='sph'){
		variableShortName='Specific Humidity';
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                        minColorbar =-30;
                        maxColorbar = 30;
			colorbarmap='BuYlRd' 
			colorbarsize=8
			varUnits='kg/kg';
                }else if(anomOrValue=='value' || anomOrValue=='clim'){
                        minColorbar = 0;
                        maxColorbar = 0.02; //kg/kg
			colorbarmap='BuRd' 
			colorbarsize=8
			varUnits='kg/kg';
                }
	 }else if(variable=='erc'){
		variableShortName='Energy Release Component';
                 statistic='Mean';
                 if(anomOrValue=='anom'){
                        minColorbar =-20;
                        maxColorbar = 20;
			colorbarmap='BuYlRd' 
			colorbarsize=8
			varUnits='';
                 }else if(anomOrValue=='anompercentchange'){
                        minColorbar =-100;
                        maxColorbar = 100;
			colorbarmap='BuYlRd' 
			colorbarsize=8
			varUnits='%';
                 }else if(anomOrValue=='anompercentof'){
                        minColorbar =75;
                        maxColorbar = 125;
			colorbarmap='BuYlRd' 
			colorbarsize=8
			varUnits='';
                }else if(anomOrValue=='value' || anomOrValue=='clim'){
                        minColorbar = 10;
                        maxColorbar = 120; //
			colorbarmap='YlOrRd' 
			colorbarsize=8
			varUnits='';
                }
         }else if(variable=='pet'){
		variableShortName='Reference Evapotranspiration';
                 statistic='Total';
                 if(anomOrValue=='anompercentof'){
			minColorbar =75;
			maxColorbar =125;
			colorbarmap='GBBr'
			colorbarsize=9
			varUnits='%';
                 }else if(anomOrValue=='anompercentchange'){
			minColorbar =-100;
			maxColorbar =100;
			colorbarmap='GBBr'
			colorbarsize=9
			varUnits='%';
		}else if (anomOrValue=='anom'){
                 	if(units='metric'){
				minColorbar =-100*numMonths;
				maxColorbar =100*numMonths;
				varUnits='mm';
			}else if (units=='english'){
				minColorbar =-4*numMonths;
				maxColorbar =4*numMonths;
				varUnits='in';
			}
			colorbarmap='BrBG'
			colorbarsize=9
                }else if(anomOrValue=='value' || anomOrValue=='clim'){
                 	if(units='metric'){
				minColorbar = 300;
				maxColorbar = 800; //mm
				varUnits='mm';
                 	}else if(units=='english'){
				minColorbar = 10;
				maxColorbar = 30; //in
				varUnits='in';
			}
			colorbarmap='BuRd' 
			colorbarsize=8
                }
         }else if(variable=='pdsi'){
		variableShortName='PSDI';
                 statistic='Mean';
                 if(anomOrValue=='anom'){
			minColorbar =-6;
			maxColorbar =6;
                        colorbarmap='RdYlBu' 
                        colorbarsize=8
			varUnits='';
                }else if (anomOrValue=='value' || anomOrValue=='clim'){
                        minColorbar = -6;
                        maxColorbar = 6; 
                        colorbarmap='RdYlBu' 
                        colorbarsize=8
			varUnits='';
                }
	 }else if(variable=='wb'){
		variableShortName='Water Balance';
                 statistic='Total';
                 if(anomOrValue=='anompercentof'){
                        minColorbar =75;
                        maxColorbar =125;
			colorbarmap='BrBG' 
			colorbarsize=9
			varUnits='%';
                 }else if(anomOrValue=='anompercentchange'){
			minColorbar =-100;
			maxColorbar =100;
			colorbarmap='BrBG'
			colorbarsize=9
			varUnits='%';
		}else if(anomOrValue=='anom'){
			if(units=='metric'){
				maxColorbar = 100*numMonths;
				minColorbar =-100*numMonths;
			}else if(units=='english'){
				maxColorbar = -4*numMonths;
				minColorbar =4*numMonths;
			}
                        maxColorbar = 100*numMonths;
			colorbarmap='BrBG' 
			colorbarsize=9
			varUnits='%';
                }else if(anomOrValue=='value' || anomOrValue=='clim'){
                 	if(units=='metric'){
				minColorbar = -200;
				maxColorbar = 200; //mm
				varUnits='mm';
                 	}else if(units=='english'){
				minColorbar = -10;
				maxColorbar = 10; //in
				varUnits='in';
			}
			colorbarmap='RdBu' 
			colorbarsize=8
                }   
	     }

             colorbarLabel=variableShortName;
             if(anomOrValue=='anom'){
	   	colorbarLabel=colorbarLabel + ' Difference from Climatology'
  	     }else if(anomOrValue=='anompercentof'){
	   	colorbarLabel=colorbarLabel + ' Percent of Climatology'
  	     }else if(anomOrValue=='anompercentchange'){
	   	colorbarLabel=colorbarLabel + ' Percent Difference from Climatology'
	     }
             if(varUnits!=''){
		colorbarLabel=colorbarLabel+' ('+varUnits+')';
             }
	     document.getElementById('colorbarLabel').value =colorbarLabel;

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
