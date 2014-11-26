<!DOCTYPE html>
<html lang="en">
<!-- Base bones skeleton of webpage-->
{% include 'includes/header.html'%}

<body>

	{% include 'includes/navigation.html'%}

	<!-- Page Content -->
	<div class="container">
        	<div class="row">
			{% block content %}  {% endblock %}
			<hr>
			{% include 'includes/footer.html'%}
		</div>
	</div>
	<!-- /.container -->

	
	{% include 'includes/basicscripts.php'%}
<!--
	<script type="text/javascript">
	      google.load("visualization", "1", {packages:["corechart"]});
	      google.setOnLoadCallback(drawChart);
	      function drawChart() {
		  var TimeSeries_array = {{ timeSeriesData }};
		    
		  var data = google.visualization.arrayToDataTable(TimeSeries_array);
		  
		  var options = {
		    title: 'NDVI',
		    hAxis: {title: 'Dates', titleTextStyle: {color: 'blue'}},
		    vAxis: {title: 'NDVI', titleTextStyle: {color: 'blue'}}
		  };
		  
		  var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
		  chart.draw(data, options);
    }
    </script>
-->

</body>

</html>
