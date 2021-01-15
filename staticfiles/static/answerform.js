<script>
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');
			
$(document).ready(function (){		

		$("#answer-form").submit(function (e) {
			e.preventDefault();
			var serializedData = $(this).serialize();
			
			$.ajax({
				type: "POST",
				url: "{% url "answer" question_id=question.id %}",
				beforeSend: function(xhr) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				},
				data: {
					'answer' : answer-form.answer,
				}
				success: function (response){
					console.log("success");
					console.log(serializedData);
					$("#answer-form").trigger('reset');
				},
					error: function (response) {
						// alert the error if any error occured
						alert(response["responseJSON"]["error"]);
				}
			})
		})
		

	
	});
</script>