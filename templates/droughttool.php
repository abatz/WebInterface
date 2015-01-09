<!DOCTYPE html>

<html lang="en">

<!-- Call HTML head template -->
{% include 'includes/head.html'%}

<body>
	<div id="wrapper">

		<!-- Call navigation template -->
		{% include 'includes/navigation.html'%}

		<!-- Menu form -->
		<div id="menu">
			<form  action="/" id="form_map" method="post" onsubmit="showLoadingImage.show_loading()">
				{% include 'includes/dataform.html'%}
			</form>
		</div>
		
		<!-- Title and colorbar -->
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
		
		<!-- Call templates -->
        {% include 'aboutdatamodal.html'%}
        {% include 'contactmodal.html'%}
        {% include 'aboutmetricsmodal.html'%}
        {% include 'sharelinkmodal.html'%}
        {% include 'optionsmodal.html'%}
        {% include 'droughthomemodal.html'%}
        {% include 'caseStudiesModal.html'%}

	</div>

	<!-- Call scripts -->
    {% include 'includes/basicscripts.php'%}
    {% include 'includes/scripts.php'%}

</body>

</html>

