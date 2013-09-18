$(document).ready(function(){
	var FADE_INOUT_TIME = 500;

	$('#addlink').click(function() {
		var url = document.getElementById('input-url').value;

		$.ajax({
			type: "POST",
			contentType: "application/json; charset=utf-8",
			url: "/add",
			data: JSON.stringify({ url: url }),
			success: function(data) {
				var id = data.site.id;
												
				if ($("#no-site-entry")){
					$("#no-site-entry").fadeOut(FADE_INOUT_TIME, function(){ 
						$(this).remove();
					});
				}
						
				$.get("site/" + id, function(data) {
					$("#sites-list").append(data);
					$("#site-entry" + id).hide().fadeIn(FADE_INOUT_TIME);
				});	
						
			},
			dataType: "json",
		});
	});

	$(document).on("click", '.btn-danger', function(e) {				
		var id = e.target.id.replace("delete-site", "");

		$.ajax({
			type: "DELETE",
			url: "/delete/" + id,	
			success: function()	{

				$("#site-entry" + id).fadeOut(FADE_INOUT_TIME, function(){ 
					$(this).remove();
				});
						
			},	
		});
		
	});

});
