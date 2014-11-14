graph_utils = {
	//=================================
	//    AndyChart 
	//=================================
AndyChart: function(Data) {
		var chart, data, options;

		google.load("visualization", "1", {packages:["corechart"]});
		google.setOnLoadCallback(drawGraph);

		function drawGraph() {
    			data = google.visualization.arrayToDataTable(Data);
    			options = {
	    			title: 'NDVI',
	    			hAxis: {title: 'Dates', titleTextStyle: {color: 'blue'}},
	    			vAxis: {title: 'NDVI', titleTextStyle: {color: 'blue'}}
    			};

    			var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
			chart.draw(data, options);
		}//end drawGraph
	},//end AndyChart function



	//=================================
	//     HELLO WORLD
	//=================================

	HelloWorld: function() {
		alert("Hello World");
	}//End HelloWorld
}
