<!DOCTYPE html>

<html lang="en">

<!-- Call HTML head template -->
{% include 'includes/head.html'%}
{% include 'includes/basicscripts.php'%}

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
			 <form action="/" id="form_map" method="post">
				onsubmit="">
		<!--
                                onsubmit="waitingDialog.show('Processing Request',
                                        {dialogSize: 'sm', progressType: 'warning'});
                                window.timeoutID =setTimeout(function () {waitingDialog.hide();}, 60000);">
			-->
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
						{% if source %}<span style="font-size:10pt"><center>Source: {{ source }}</center></span>{% endif %}
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
		<!-- LAYER DROPDOWN             -->
		<!---------------------------->
<!--
<div class="layercontainer">
    <div class="dropDownControl" id="ddControl" title="A custom drop down select with mixed elements" onclick="(document.getElementById('myddOptsDiv').style.display == 'block') ? document.getElementById('myddOptsDiv').style.display = 'none' : document.getElementById('myddOptsDiv').style.display = 'block';"">
        My Box
        <img class="dropDownArrow" src="http://maps.gstatic.com/mapfiles/arrow-down.png"/>
    </div>
    <div class = "dropDownOptionsDiv" id="myddOptsDiv">
        <div class = "dropDownItemDiv" id="mapOpt"  title="This acts like a button or click event" onClick="alert('option1')">Option 1</div>
        <div class = "dropDownItemDiv" id="satelliteOpt" title="This acts like a button or click event" onClick="alert('option2')">Option 2</div>
        <div class="separatorDiv"></div>
        <div class="checkboxContainer" title="This allows for multiple selection/toggling on/off" onclick="(document.getElementById('terrainCheck').style.display == 'block') ? document.getElementById('terrainCheck').style.display = 'none' : document.getElementById('terrainCheck').style.display = 'block';">
        <span role="checkbox" class="checkboxSpan ">
            <div class="blankDiv" id="terrainCheck">
                <img class="blankImg" src="http://maps.gstatic.com/mapfiles/mv/imgs8.png" />
            </div>
        </span>             
        <label class="checkboxLabel">On/Off</label>             
    </div>          
    </div>
</div>		
-->
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
    	{% include 'includes/scripts.php'%}

</body>

</html>

