$(document).ready(function() {
	$("#registerButton").click(function() {
		$.ajax({
			url: 'http://localhost:5001/check_for_user',
			type: 'POST',
			cache:false,
			async: false,
			data: {'username': $('#registerUsername').val(),
						  'hash': md5($('#registerPassword').val()),
						  'token': $('#token').val()},
			beforeSend: function() {
				$.blockUI({ css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#000',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: .5,
            color: '#fff'
        } });
			},
			success: function(result){
				$.unblockUI();
				if(result == 'False'){
					$('#loginAlert').show();
					return false;
				}
				$(location).prop('href', 'http://localhost:5001/logged_in');
			}
		});
		return false;
	});
});
