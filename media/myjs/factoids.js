
function showFactoids(cbox) {
	if(cbox.checked) {		
		var graphics = [];				
		for (var i = 0; i < factoids.length - 1; i++) {		
			var imageIcon = new esri.symbol.PictureMarkerSymbol("factoids/icons/" + factoids[i].icon, 30, 30).setOffset(-15, -15);
			var point = new esri.geometry.Point(factoids[i].lon, factoids[i].lat);
			var attr = {
				content: '<img style="padding:5px;" width="150px" height="100px" src="factoids/images/' + i + '.png" align="left">' + factoids[i].desc + '<br/>' + '<a href="' + factoids[i].hlink + '" target="_blank">Click Here For more information</a><img src="images/hide.png" align="right" width="12px" height="12px" title="Close" alt="Close" onclick="g_mouseout()"/>'
			};
			var graphic = new esri.Graphic(esri.geometry.geographicToWebMercator(point), imageIcon, attr, null);
			graphics.push(graphic);
		}
		
		for (var i = graphics.length - 1; i >= 0; i--) {
        	map.graphics.add(graphics[i]);
    	}
				
		dojo.connect(map.graphics, "onMouseOver", g_mouseover);
		//dojo.connect(map.graphics, "onMouseOut", g_mouseout);			
	} else {		
		if (iTip.isShowing) iTip.hide();
		map.graphics.clear();	
	}
}

factoids = [{desc:"China Academy of Science reported that annual rainfall in the area of the Yangtze River had dropped 10.3 and 6.9 percent respectively in 2006 and 2007 due to climate change.  Additionally, severe droughts in 2007 and 2008 resulted in the shrinking of two of the nation's biggest freshwater lakes, Poyang and Dongting.",
			hlink:"http://www.nature.org/wherewework/asiapacific/china/work/yangtze.html",
			reference:"http://www2.chinadaily.com.cn/china/2009-04/20/content_7693329.htm",
			credit:"Photo Â© CJ Hudlow/ TNC",
			lat:33.468028,
			lon:91.195903,
			icon:"rain.png"},
]
