<!DOCTYPE html>
<html lang="en">
{% include 'includes/header.html'%}
<body>
	<div id="wrapper">
		{% include 'includes/navigation.html'%}
		<div id="menu">
				<form  action="/" id="form_map" method="post" onsubmit="showLoadingImage.show_loading()">
					{% include 'includes/dataform.html'%}
				</form>
		</div>
		<!------------------------->
		<!-- TITLE and COLORBAR -->
		<!------------------------>
		  {% if ppost ==1 %}
			<br>
			<table padding="1">
			<tr>
			<td width="30%" padding="1"> 
			</td>
			<td width="40%">
				<span style="font-size:18pt"><center>{{ title }}</center></span>
				<span style="font-size:10pt"><center>Source: {{ source }}</center></span>
				{% if anomOrValue=='anom' or anomOrValue=='clim' %}
					 <span style ="font-size:10pt"><center> {{ climatologyNotes }}</center></span>
				{% endif %}
			</td>
			<td width="30%">
				<div id="colorbar"><svg style="width:400px;height:30px;"></svg></div><br>
				<center>{{ colorbarLabel }}</center>
				<div name="form_colorbar" id="target_colorbar" style="width:100%">
					<center>
					<img class="img-responsive img-hover" 
						src="/images/colorbars/colorbar_{% if anomOrValue =='anom' %}d{% endif %}{{ variable }}.png" 
						id="colorbar">&nbsp;
					</center>
				</div>
			</td>
			</tr>
			</table>
		{% endif %}
		<!----------MAP------------>
		<div id="map"></div>
		<!---------------------->
	      </div>

             {% include 'droughthomemodal.html'%}
             {% include 'aboutdatamodal.html'%}
             {% include 'contactmodal.html'%}
             {% include 'aboutmetricsmodal.html'%}
             {% include 'sharelinkmodal.html'%}
             {% include 'optionsmodal.html'%}
             {% include 'figuresmodal.html'%}
             {% include 'datamodal.html'%}
	  </body> 
	</div>
        {% include 'includes/basicscripts.php'%}
        {% include 'includes/scripts.php'%}

</body>

</html>

