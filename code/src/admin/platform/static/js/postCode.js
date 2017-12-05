$(function(){
	$('#btnSubmitCode').click(function(event){
		event.preventDefault();
	    $('html, body').animate({
	        scrollTop: $("#compilation_result").offset().top
	    }, 2000);

		$.ajax({
			url: '/postCode',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				var res = JSON.parse(response)
			    document.getElementById("compilation_result").innerHTML=res['compilation_res']
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
