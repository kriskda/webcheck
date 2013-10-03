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

	$(document).on("click", '.delete-button', function(e) {				
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
	
    function setDBState(stateCode) {
		$.ajax({
			type: "POST",
			contentType: "application/json; charset=utf-8",
			url: "/set_db_state",
			data: JSON.stringify({ db_code: '0' }),
			success: function(data) {
				
			},
			dataType: "json",
		});
	};
	
	function reloadChanges() {
		console.log("reload");
		
		$.ajax({
			type: "GET",
			url: "/sites",
			success: function(data) {	
				var sites = data.result;						
				var className, statusCode;
				
				for (var i = 0 ; i < sites.length ; i++) {
					statusCode =  sites[i].status_code;
					
					if (statusCode == "200") {
						className = "span1 status status-normal";
					} else if (statusCode == "Unknown") {
						className = "span1 status status-unknown";
					} else if (statusCode == "Offline") {
						className = "span1 status status-alert";
					} else {
						className = "span1 status status-alert";
					}		
					
					$("#last-check" + sites[i].id).text(sites[i].last_check);
					$("#status-code" + sites[i].id).text(statusCode);
					$("#status-code" + sites[i].id).attr('class', className);	
				}		
				
				setDBState(0);												
			},
		});
	};
	
	function checkDBForUpdate() {
		console.log("checking");
		$.ajax({
			type: "GET",
			url: "/check_db_state",	
			success: function(data)	{			
				if (data['1'] == '1') {
					reloadChanges();
				}							
			},	
		});
	};
		
	setInterval(function() {checkDBForUpdate()}, 5000);

});
