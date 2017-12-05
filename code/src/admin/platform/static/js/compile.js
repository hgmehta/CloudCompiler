$(function() {
  $('#compile').click( function() {
	$.ajax({
		url: '/compile',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response) {
			console.log(response);
			var res = JSON.parse(response)
			document.getElementById("output").innerHTML=res['compilation_res']
		},
		error: function(error) {
			console.log(error);
		}
	});
  });
});
