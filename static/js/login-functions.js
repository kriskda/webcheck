$(document).ready(function(){

	$('#login-button').click(function() {
		var username = $('#username').val();
		var password = $('#password').val();
		
		$.ajax({
			type: "POST",
			contentType: "application/json; charset=utf-8",
			url: "/signin",
			data: JSON.stringify({ username: username, password: password }),
			success: function(site) {
				
			},
			dataType: "json",
		});
		
	});
	
})
