$(document).ready(function() {
	$("#generateTokenButton").click(function() {
		$.ajax({
			url: 'http://localhost:5001/create_token',
			type: 'POST',
			cache:false,
			async: true,
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
				$("#generatedToken").prop('value', result['token']);
				return false;
			}
		});
		return false;
	});

});
