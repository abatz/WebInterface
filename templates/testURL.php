<!DOCTYPE html>

<html lang="en">
{% include 'includes/head.html'%}
    <body>
      <div id="wrapper">
          <div class="container">
			<h4>Test Results from Executing URLs from http://drought-monitor3.appspot.com </h4>
			<table border = '5' padding='25'>
			<tr>
				<td><b>Variable</b></td> 
				<td><b>Test Status</b></td>
			</tr>
			<tr>
				<td>myVariable </td>
				<td>
					{% if errorMessage == 'failed' %} 
						<span style="color:red"> 
					{%elif errorMessage =='success' %} 
						<span style="color:green"> 
					{% endif %}
						{{ errorMessage }}</span>
				</td>
			</tr>
			</table>
  	  </div>
       </div>
    </body>
</html>

