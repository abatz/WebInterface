$(function(){
	    $( "#dailyfrom" ).datepicker({
	      //defaultDate: "+1w",
	      changeMonth: true,
	      changeYear: true,
	      numberOfMonths: 1,
	      minDate: "01/01/1979",
	      maxDate: "0",
	      onClose: function( selectedDate ) {
		$( "#to" ).datepicker( "option", "minDate", selectedDate );
	      }
	  }).datepicker('setDate', "01/01/1979");
	 $( "#dailyto" ).datepicker({
	      //defaultDate: "+1w",
	      changeMonth: true,
	      changeYear: true,
	      numberOfMonths: 1,
	      minDate: "01/01/1979",
	      maxDate: "0",
	      onClose: function( selectedDate ) {
		$( "#from" ).datepicker( "option", "maxDate", selectedDate );
      		}
	  }).datepicker('setDate', 'today');
	$(function() {
		 $("#monthlyto").datepicker({
			dateFormat: 'MM yy',
			changeMonth: true,
			changeYear: true,
			showButtonPanel: false,

			onClose: function(dateText, inst) {
			    var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
			    var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
			    $(this).val($.datepicker.formatDate('MM yy', new Date(year, month, 1)));
			}
		    });
		    $("#monthlyto").focus(function () {
			$(".ui-datepicker-calendar").hide();
			$("#ui-datepicker-div").position({
			    my: "center top",
			    at: "center bottom",
			    of: $(this),
			});
		    });
		 $("#monthlyfrom").datepicker({
			dateFormat: 'MM yy',
			changeMonth: true,
			changeYear: true,
			showButtonPanel: false,

			onClose: function(dateText, inst) {
			    var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
			    var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
			    $(this).val($.datepicker.formatDate('MM yy', new Date(year, month, 1)));
			}
		    });

		    $("#monthlyfrom").focus(function () {
			$(".ui-datepicker-calendar").hide();
			$("#ui-datepicker-div").position({
			    my: "center top",
			    at: "center bottom",
			    of: $(this)
			});
		    });
	});
});
