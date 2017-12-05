$(function() {
  $('#savefile_id').click( function() {
	$.ajax({
		url: '/savefile',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response) {
			console.log(response);
			var res = JSON.parse(response)
			document.getElementById("code_editor_output").innerHTML=res['message']
		},
		error: function(error) {
			console.log(error);
		}
	});
  });
});