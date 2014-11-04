{% extends "base.php" %}
{% block content %}
<!----------------------------->
<table border="1" width="100%" height="100%" table-layout="fixed">
         <tr>
		<!----------------------------->
		<!--     OPTIONS FORM        -->
		<!----------------------------->
                <td valign="top" width="25%" height="600px">
                        <form  id="form_div" action="" target="form_target" method="post">
                        {% include 'includes/dataform.html'%}
                        </form>
                </td>
		<!----------------------------->
		<!--     CONTENT                -->
		<!----------------------------->
                <td valign="top" width="75%" height="600px">
                        {% include 'includes/mapfiguredata.html'%}
       			<div id="map" style="width: 800x; height: 600px;"></div>
                </td>
        </tr>
</table>
<!----------------------------->
{% endblock %}
