$(function(){
	    $( "#dateStart" ).datepicker({
	      //defaultDate: "-2w",
	      changeMonth: true,
	      changeYear: true,
	      numberOfMonths: 3,
	      //minDate: "01/01/1979",
	      minDate: "1979-01-01",
	      maxDate: "0",
	      dateFormat: "yy-mm-dd",
	      onClose: function( selectedDate ) {
		$( "#dateStart" ).datepicker( "option", "minDate", selectedDate );
	      }
	  }).datepicker('setDate', "01/01/1979");
	 $( "#dateEnd" ).datepicker({
	      //defaultDate: "+1w",
	      changeMonth: true,
	      changeYear: true,
	      numberOfMonths: 3,
	      minDate: "1979-01-01",
	      //minDate: "01/01/1979",
	      maxDate: "0",
	      dateFormat: "yy-mm-dd",
	      onClose: function( selectedDate ) {
		$( "#dateEnd" ).datepicker( "option", "maxDate", selectedDate );
      		}
	  }).datepicker('setDate', 'today');
});
