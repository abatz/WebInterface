<!DOCTYPE html>

<html lang="en">

<!-- Skeleton of webpage -->
{% include 'includes/head.html'%}

	<body>

	<!-- Navigation template -->
		{% include 'includes/navigation.html'%}

		<!-- Page Content -->
		<div class="container">
	        <div class="row">
				{% block content %}  {% endblock %}
				<hr>
				{% include 'includes/footer.html'%}
			</div>
		</div>
		
		<!-- Load general Javascript scripts -->
		{% include 'includes/basicscripts.php'%}

	</body>

</html>
