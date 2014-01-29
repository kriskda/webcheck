$(document).ready(function(){
	var FADE_INOUT_TIME = 500;

	$('#addlink').click(function() {
		var url = document.getElementById('input-url').value;

		if ((url.indexOf('http://') == -1) && (url.indexOf('https://') == -1)) {
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

	$(document).on("click", '.edit-button', function(e) {
		var id = this.id.slice(-1);
		
		var url_obj = $("#url-link" + id);
		var url = url_obj.attr("href");
		
		var edit_form_code = '<form id="edit-form' + id + '" name="addsite" method="POST">' +
					         '<input id="edit-input' + id + '" type="text" value="' + url + '"><br />' + 
					         '<a id="save-button' + id + '" href="#" class="save-button btn btn-small btn-primary">Save</a>' + " " +
					         '<a id="cancel-button' + id + '" href="#" class="cancel-button btn btn-small btn-primary">Cancel</a>' +
						     '</form>';
		
		url_obj.replaceWith(edit_form_code);
	});

	$(document).on("click", '.save-button', function(e) {
		var id = this.id.slice(-1);
		var url = $("#edit-input" + id).val();

		$.ajax({
			type: "PUT",
			contentType: "application/json; charset=utf-8",
			url: "/edit/" + id,
			data: JSON.stringify({ url: url }),
			success: function(data)	{
				closeEditInput(id, url);
		
				$("#last-check" + id).text("Not checked yet");
				$("#status-code" + id).text("Unknown");
				$("#status-code" + id).attr('class', "span1 status status-unknown");
			}
		});

	});

	$(document).on("click", '.cancel-button', function(e) {
		var id = this.id.slice(-1);
		var url = $("#edit-input" + id).attr("value");

		closeEditInput(id, url);
	});

	function closeEditInput(id, url) {		
		var url_code = '<a id="url-link' + id + '" href="' + url + '" target="_blank"><b>' + url + '</b></a>';
		
		$('#edit-form' + id).replaceWith(url_code);
	};

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
