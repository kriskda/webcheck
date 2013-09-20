$(document).ready(function(){
	var FADE_INOUT_TIME = 500;

	$('#addlink').click(function() {
		var url = document.getElementById('input-url').value;
		
		if (url.indexOf('http://') == -1) {
			url = 'http://' + url;
		}

		$.ajax({
			type: "POST",
			contentType: "application/json; charset=utf-8",
			url: "/add",
			data: JSON.stringify({ url: url }),
			success: function(site) {
				var id = site.id;
		
				$.get("site/" + id, function(data) {
					$("#sites-list").append(data);
					$("#site-entry" + id).hide().fadeIn(FADE_INOUT_TIME);
					
					if ($("#no-site-entry")){
						$("#no-site-entry").fadeOut(FADE_INOUT_TIME, function() { 
							$(this).remove();
						});
					}
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
			success: function(data)	{

				$("#site-entry" + id).fadeOut(FADE_INOUT_TIME, function(){ 
					$(this).remove();
					
					if (data.sites_number == 0) {
						$("#sites-list").append('<div id="no-site-entry"><em>No sites so far...</em></div>').hide().fadeIn(FADE_INOUT_TIME);
					}
				});
						
			},	
		});
		
	});

});
