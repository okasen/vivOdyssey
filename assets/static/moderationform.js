<script>
function createDeleteButton(rowId) {
	var deleteButton = document.createElement('button');
	deleteButton.textContent = 'delete';
	deleteButton.className = 'deleteClass';
	deleteButton.id = rowId;
	return deleteButton;
}
var pollsRows = document.querySelector(".questionTable");

var qTable = document.getElementById("all_questions");
var thead, tr, td;
	qTable.appendChild(thead = document.createElement("thead"));
	thead.appendChild(tr = document.createElement("tr"));
	tr.appendChild(td = document.createElement("td"));
	td.innerHTML = "Title";
	tr.appendChild(td = document.createElement("td"));
	td.innerHTML = "Description";
	tr.appendChild(td = document.createElement("td"));
	td.innerHTML = "Delete?";

{% for question in questions %}
	tr = document.createElement("tr");
	qTable.appendChild(tr);
	tr.appendChild(td = document.createElement("td"));
	td.innerHTML = "{{question.title}}";
	tr.appendChild(td = document.createElement("td"));
	td.innerHTML = "{{question.text}}";
	tr.appendChild(td = document.createElement("td"));
	td.appendChild(this.createDeleteButton("{{question.title}}"));
{% endfor %}

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

		$("#question-form").submit(function (e) {
			e.preventDefault();
			var serializedData = $(this).serialize();
			
			$.ajax({
				type: "POST",
				url: "{% url "moderation" %}",
				beforeSend: function(xhr) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				},
				headers: {
					'reqType': "Post",
				},
				data: serializedData,
				success: function (response){
					console.log("success");
					$("#question-form").trigger('reset');
					$("#id_question").focus();
					
					var instance = JSON.parse(response["instance"]);
					var field = instance[0]["fields"];
					tr = document.createElement("tr");
					qTable.appendChild(tr);
					var id = field["title"]||"";
					tr.appendChild(td = document.createElement("td"));
					td.innerHTML = id;
					tr.appendChild(td = document.createElement("td"));
					td.innerHTML = field["text"]||"";
					tr.appendChild(td = document.createElement("td"));
					td.appendChild(createDeleteButton(id));
				},
					error: function (response) {
						// alert the error if any error occured
						alert(response["responseJSON"]["error"]);
				}
			})
		})
		

	
	});
	
function deleteFromDb(toDelete) {
	if(confirm("are you sure you want to delete this question? ID: " + toDelete)){
		$.ajax({
			type: "POST",
			url: "{% url "moderation" %}",
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
			headers: {
				'reqType': "Delete",
			},
			data: {
				'delId': toDelete
			},
		}).done(
			function(){alert("deleted");}
			).fail(
				function(){alert("error. Did not delete");}
			)
		}

}
	
pollsRows.addEventListener('click', function(event) {

	var elementClicked = event.target;

	if (elementClicked.className === 'deleteClass'){
		console.log(event.target);
		TrToDel = event.target.parentNode.parentNode;
		TrToDel.parentNode.removeChild(TrToDel);
		deleteFromDb(event.target.id);
	}
});
</script>