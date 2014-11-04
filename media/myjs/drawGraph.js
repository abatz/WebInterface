var data={{ timeSeriesData }};
var chart;

google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawGraph);

function drawGraph() {
    timeSeriesData = data;

    var data = google.visualization.arrayToDataTable(timeSeriesData);

    var options = {
	    title: 'NDVI',
	    hAxis: {title: 'Dates', titleTextStyle: {color: 'blue'}},
	    vAxis: {title: 'NDVI', titleTextStyle: {color: 'blue'}}
    };

    //var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

    chart.draw(data, options);
}
