$(document).ready(function(){
	$(".btn-add").click(function() {
		$(".modal-add").modal()
	})

	var forms = document.getElementsByClassName("form-add")
	var validation = Array.prototype.filter.call(forms, function(form) {
		form.addEventListener("submit", function(event) {
			event.stopPropagation()
			event.preventDefault()

			if (form.checkValidity() === false) {
			} else {
				addSubmit()
			}
			form.classList.add("was-validated")
		}, false)
	})

	function addSubmit() {
		console.log("HI")
		formData = {}
		$(".form-control-add").each(function() {
			formData[$(this).attr("name")] = $(this).val();
		})

		formData["maintainers"] = []
		$(".maintainer-group").each(function() {
			maintainer = {}
			$(".form-control-maintainer-add").each(function() {
				maintainer[$(this).attr("name")] = $(this).val();
			})
			formData["maintainers"].push(maintainer)
		})
		console.log(JSON.stringify(formData))
		$.ajax({
			type: "POST",
			contentType: "application/json",
			data: JSON.stringify(formData),
			dataType: "json",
			url: "/add",
			success: function (e) {
				location.reload();
			},
			error: function(error) {
				$(".form-error").removeClass('d-none').text(error.responseJSON["message"])
			}
		});
	}

	$(".btn-add-maintainer").click(function() {
		$(".maintainer-group").first().clone().appendTo($(".maintainers"))
	})

	$(".btn-search").click(function() {
		title = $(".text-search").val()
		var params = {
			t: title
		}
		var array = JSON.stringify(params);

		$.ajax({
			url: "/search/" + title,
			type: "GET",
			contentType: "application/json",
			success: function(data) {
				$(".results").empty();
				data = $.parseJSON(data);
				$.each(data, function(i, metadata) {
					console.log(metadata)
					_id = metadata["_id"]["$oid"]
					element = "<div>" + 
					"<h2><a href='/metadata/" + _id + "'>" + metadata["title"] + "</a></h2>" + 
					"<h4>" + metadata["description"] + "</h4>"
					+ "</div>"
					$(".results").append(element)
				});
			}
		});
	})
})