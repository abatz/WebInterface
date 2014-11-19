{% extends "base.php" %}
{% block content %}
<!----------------------------->
<table border="1" width="100%" height="100%" table-layout="fixed">
         <tr>
		<!----------------------------->
		<!--     OPTIONS FORM        -->
		<!----------------------------->
                <td valign="top" width="25%" height="600px">
                        <form  id="form_div" method="post" onsubmit="showLoadingImage.show_loading();findAddress();">
                        {% include 'includes/dataform.html'%}
                        </form>
                </td>
		<!----------------------------->
		<!--     CONTENT                -->
		<!----------------------------->
                <td valign="top" width="75%" height="600px">
                        {% include 'includes/mapfiguredata.html'%}
                </td>
        </tr>
</table>
{% include 'includes/scripts.php'%}
<!----------------------------->
{% endblock %}
