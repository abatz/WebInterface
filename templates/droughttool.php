<!DOCTYPE html>
<html lang="en">
{% include 'includes/header.html'%}
<body>
	<div id="wrapper">
		{% include 'includes/navigation.html'%}
		<div id="menu">
				<form  id="form_map" method="post" onsubmit="showLoadingImage.show_loading()">
					{% include 'includes/dataform.html'%}
				</form>
		</div>
		<!------------------------->
		<!-- TITLE and COLORBAR -->
		<!------------------------>
		  {% if ppost ==1 %}
			<br>
			<span style="font-size:18pt"><center>{{ title }}</center></span>
			<span style="font-size:10pt"><center>Source: {{ source }}</center></span>
			{% if anomOrValue=='anom' or anomOrValue=='clim' %}
				 <span style ="font-size:10pt"><center> {{ climatologyNotes }}</center></span>
			{% endif %}
			<div name="form_colorbar" id="target_colorbar">
				<center>
				<img class="img-responsive img-hover" 
					src="/images/colorbars/colorbar_{% if anomOrValue =='anom' %}d{% endif %}{{ variable }}.png" 
					id="colorbar">
				</center>
			</div>
		{% endif %}
		<!----------MAP------------>
		<div id="map"></div>
		<!---------------------->

	      </div>
	  </body> 
	</div>
        {% include 'includes/basicscripts.php'%}
        {% include 'includes/scripts.php'%}

</body>

</html>

