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

	{% include 'includes/scripts.html'%}

</body>

</html>
