//var chart;
//var data;
google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawGraph);

function drawGraph() {
    var TimeSeriesArray = {{ timeSeriesData }};
    var data = google.visualization.arrayToDataTable(TimeSeriesArray);

    var options = {
	    title: 'NDVI',
	    hAxis: {title: 'Dates', titleTextStyle: {color: 'blue'}},
	    vAxis: {title: 'NDVI', titleTextStyle: {color: 'blue'}}
    };

     var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

    chart.draw(data, options);
}
