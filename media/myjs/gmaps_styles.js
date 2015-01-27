/*!
 * GMaps_styles.js v0.1.1
 * https://github.com/KilukruMedia/gmaps_styles
 *
 * Copyright 2014, Alfred Dagenais - Kilukru Media
 * Released under the MIT License.
 */

var GMaps_styles = (function(global) {
  "use strict";

  var GMaps_styles = function(options) {
    if (!this) return new GMaps_styles(options);

    if( typeof(options) == 'undefined' ){options = [];}
    options.custom_styles = options.custom_styles || [];

    var self = this;

    // Define styles
    this.data = [];


    this.data["light-political"] = {
      mapName : "\u00c9l\u00e9ments g\u00e9ographiques att\u00e9nu\u00e9s et fronti\u00e8res politiques",
      mapId   : "light-political",
      styles : [{
          featureType: "water",
          stylers: [{
              visibility: "on"
          }, {
              saturation: 2
          }, {
              hue: "#004cff"
          }, {
              lightness: 40
          }]
      }, {
          featureType: "administrative",
          elementType: "geometry",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "landscape",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 45
          }]
      }, {
          featureType: "transit",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "poi.government",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "poi",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "road",
          elementType: "labels",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "road",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }, {
              saturation: -99
          }, {
              lightness: 60
          }]
      }, {
          featureType: "administrative.country",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 50
          }]
      }, {
          featureType: "administrative.province",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 50
          }]
      }, {
          featureType: "administrative.country",
          elementType: "labels",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 50
          }]
      }, {
          featureType: "administrative.locality",
          elementType: "labels",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 60
          }]
      }, {
          featureType: "administrative.neighborhood",
          elementType: "labels",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 65
          }]
      }, {
          featureType: "administrative.province",
          elementType: "label",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 55
          }]
      }]
    };



    this.data["dark-landmass"] = {
      mapName : "Masse terrestre sombre",
      mapId   : "dark-landmass",
      styles : [{
          elementType: "labels",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "water",
          elementType: "geometry",
          stylers: [{
              hue: "#223D4A"
          }, {
              saturation: -18
          }, {
              lightness: -72
          }, {
              visibility: "on"
          }]
      }, {
          featureType: "landscape",
          elementType: "all",
          stylers: [{
              hue: "#728A96"
          }, {
              saturation: -46
          }, {
              lightness: -42
          }, {
              visibility: "on"
          }]
      }, {
          featureType: "administrative.country",
          elementType: "labels",
          stylers: [{
              hue: "#728A96"
          }, {
              saturation: -26
          }, {
              lightness: 22
          }, {
              gamma: 1.2
          }, {
              visibility: "on"
          }]
      }, {
          featureType: "administrative.locality",
          elementType: "labels",
          stylers: [{
              hue: "#728A96"
          }, {
              saturation: -26
          }, {
              lightness: -22
          }, {
              gamma: 1
          }, {
              visibility: "on"
          }]
      }, {
          featureType: "administrative",
          elementType: "geometry",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "road",
          elementType: "geometry",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "poi.park",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "poi",
          stylers: [{
              hue: "#728A96"
          }, {
              saturation: -26
          }, {
              lightness: -22
          }, {
              gamma: 1
          }, {
              visibility: "off"
          }]
      }, {
          featureType: "transit",
          stylers: [{
              visibility: "off"
          }]
      }]
    };


    this.data["light-landmass"] = {
      mapName : "Masse terrestre claire",
      mapId   : "light-landmass",
      styles : [{
          elementType: "labels",
          stylers: [{
              visibility: "off"
          }]
      }, {
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }, {
              saturation: -60
          }, {
              lightness: -2
          }]
      }, {
          featureType: "administrative",
          elementType: "geometry",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "administrative.country",
          elementType: "labels",
          stylers: [{
              hue: "#CCCCCC"
          }, {
              saturation: -90
          }, {
              lightness: 60
          }, {
              visibility: "on"
          }]
      }, {
          featureType: "administrative.locality",
          elementType: "labels",
          stylers: [{
              hue: "#CCCCCC"
          }, {
              saturation: -90
          }, {
              lightness: 50
          }, {
              gamma: 1
          }, {
              visibility: "on"
          }]
      }, {
          featureType: "road",
          elementType: "geometry",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "poi.park",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "poi",
          stylers: [{
              saturation: -55
          }, {
              gamma: .79
          }, {
              visibility: "off"
          }]
      }, {
          featureType: "transit",
          stylers: [{
              visibility: "off"
          }]
      }]
    };


    this.data["mono-city"] = {
      mapName : "Ville en monochrome",
      mapId   : "mono-city",
      styles : [{
            featureType: "administrative",
            elementType: "geometry",
            stylers: [{
                visibility: "off"
            }]
        }, {
            featureType: "administrative.country",
            elementType: "geometry",
            stylers: [{
                visibility: "off"
            }, {
                lightness: 58
            }]
        }, {
            featureType: "road",
            elementType: "geometry",
            stylers: [{
                visibility: "on"
            }, {
                lightness: 99
            }]
        }, {
            featureType: "transit.line",
            stylers: [{
                visibility: "simplified"
            }, {
                lightness: 99
            }]
        }, {
            featureType: "administrative.land_parcel",
            stylers: [{
                visibility: "off"
            }, {
                lightness: 25
            }]
        }, {
            stylers: [{
                visibility: "on"
            }, {
                hue: "#000000"
            }, {
                saturation: -20
            }, {
                lightness: 20
            }]
        }, {
            featureType: "water",
            stylers: [{
                visibility: "on"
            }, {
                hue: "#ffd500"
            }, {
                saturation: -73
            }, {
                lightness: 11
            }]
        }, {
            featureType: "poi",
            stylers: [{
                visibility: "off"
            }]
        }, {
            featureType: "road",
            elementType: "labels",
            stylers: [{
                visibility: "off"
            }]
        }, {
            featureType: "administrative",
            stylers: [{
                visibility: "on"
            }, {
                lightness: 40
            }]
        }]
    };


    this.data["simple-atlas"] = {
      mapName : 'Atlas simple',
      mapId   : 'simple-atlas',
      styles : [{
          featureType: "poi",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "administrative",
          elementType: "geometry",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "administrative.land_parcel",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }]
      }, {
          featureType: "administrative.country",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }]
      }, {
          featureType: "administrative.province",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }]
      }, {
          featureType: "administrative.neighborhood",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }]
      }, {
          featureType: "administrative.locality",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }]
      }, {
          featureType: "administrative.locality",
          elementType: "labels",
          stylers: [{
              hue: "#548096"
          }, {
              saturation: -50
          }, {
              lightness: 35
          }, {
              visibility: "on"
          }]
      }, {
          featureType: "road",
          elementType: "labels",
          stylers: [{
              visibility: "simplified"
          }]
      }, {
          featureType: "water",
          elementType: "geometry",
          stylers: [{
              hue: "#548096"
          }, {
              saturation: -37
          }, {
              lightness: -10
          }, {
              visibility: "on"
          }]
      }, {
          featureType: "landscape",
          elementType: "all",
          stylers: [{
              hue: "#E3CBAC"
          }, {
              saturation: 31
          }, {
              lightness: -12
          }, {
              visibility: "on"
          }]
      }, {
          featureType: "road",
          stylers: [{
              visibility: "simplified"
          }, {
              saturation: -49
          }, {
              lightness: 5
          }]
      }, {
          featureType: "road",
          elementType: "geometry",
          stylers: [{
              visibility: "simplified"
          }, {
              saturation: -90
          }, {
              lightness: 90
          }]
      }, {
          featureType: "administrative.land_parcel",
          stylers: [{
              visibility: "off"
          }, {
              lightness: 25
          }]
      }]
    };



    this.data["whitewater"] = {
      mapName : "Eaux blanches",
      mapId   : "whitewater",
      styles : [{
          stylers: [{
              visibility: "on"
          }, {
              saturation: -13
          }, {
              lightness: -17
          }, {
              hue: "#ff6e00"
          }]
      }, {
          featureType: "water",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 100
          }]
      }, {
          featureType: "poi",
          stylers: [{
              lightness: 39
          }, {
              saturation: -43
          }, {
              visibility: "on"
          }]
      }, {
          featureType: "roads",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 30
          }]
      }, {
          elementType: "labels",
          stylers: [{
              lightness: 35
          }]
      }]
    };


    this.datas = function( element ) {
      if( typeof(element) != 'undefined' && typeof(this.data[element]) != 'undefined' ){
        return this.data[element];
      }else{
        return this.data;
      }
    };

  };

  return GMaps_styles;
})(this);
