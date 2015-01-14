<!DOCTYPE html>

<html lang="en">

<!-- Call HTML head template -->
{% include 'includes/head.html'%}

<body>
	<div id="wrapper">
		<!---------------------------->
		<!-- NAVIGATION             -->
		<!---------------------------->
		{% include 'includes/navigation.html'%}

		<!---------------------------->
		<!-- TAB WINDOW             -->
		<!---------------------------->
		<div id="menu">
			<form   {% if timeSeriesData%} action="#timeseriesoutput"{% else %}action="/"{% endif %} id="form_map" method="post" onsubmit="showLoadingImage.show_loading()">
				{% include 'includes/tabwindow.html'%}
			</form>
		</div>
		
		<!---------------------------->
		<!-- GOOGLE MAP             -->
		<!---------------------------->
		{% if mapid %}
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
						<div name="form_colorbar" id="target_colorbar" style="width:100%">
							<center>
            					<div id="colorbar"><svg style="width:400px;height:30px;"></svg></div>
							</center>
						</div>
						<center>{{ colorbarLabel }}</center>
					</td>
				</tr>
			</table>
		{% endif %}
		<!-- Map -->
		<div id="map"></div>
		
		<!---------------------------->
		<!-- MODAL WINDOWS             -->
		<!---------------------------->
		{% include 'modal_aboutdata.html'%}
		{% include 'modal_contact.html'%}
		{% include 'modal_aboutmetrics.html'%}
		{% include 'modal_sharelink.html'%}
		{% include 'modal_home.html'%}
		{% include 'modal_caseStudies.html'%}
		{% include 'modal_tutorial.html'%}
		{% include 'modal_introvideo.html'%}

	</div>

	<!---------------------------->
	<!-- SCRIPTS             -->
	<!---------------------------->
    {% include 'includes/basicscripts.php'%}
    {% include 'includes/scripts.php'%}

</body>

</html>

