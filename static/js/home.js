jQuery(document).ready(function () {
	jQuery("#cargarUsuarios").click(function() {
  		//var usersURL = "http://localhost:5000/usuarios/";
  		var usersURL = "http://amc.eu-gb.mybluemix.net/usuarios/";
	    jQuery.getJSON(usersURL, {
	  		format: "json"
	  	}) 
	  	.done(function(data) {
		    var obj_json = JSON.stringify(data, undefined, 4);
			jQuery(".listOfUsers").append("<pre>" + obj_json + "</pre>");
		})
		.fail(function() {
		    alert("Error al hacer la consulta de usuarios.");
		});
	});
});

function getLastConnection() {
	var last_connection = "{{ last_connection }}";
	alert(last_connection);
}