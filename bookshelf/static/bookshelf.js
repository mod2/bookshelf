$(document).ready(function() {
	// From https://gist.github.com/alanhamlett/6316427
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE' || settings.type == 'PATCH') {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		}
	});


	// Menu code
	$("a.menu").on("click touchstart", function(e) {
		$("body").toggleClass("active-nav");

		return false;
	});

	$(".mask").on("click touchstart", function(e) {
		$("body").removeClass("active-nav");

		return false;
	});


	// Entry adding
	$(".booklist .entry").on("click", function() {
		// Only show if it's not already open
		if ($("#add-entry-modal:visible").length == 0) {
			// On click, populate the dialog and pull it up
			var book = $(this).parents("li:first");		
			var readingId = book.attr("data-reading-id");
			var currentPageNumber = $(this).find(".page_number");

			$("#add-entry-modal").attr("data-reading-id", readingId);

			if (currentPageNumber != "—") {
				$("#add-entry-modal input[type=number]").val(currentPageNumber);
			}

			$("#add-entry-modal input[type=number]").focus();

			$("#add-entry-modal").slideDown(150);
		}

		return false;
	});

	$(".modal .cancel-link").on("click", function() {
		$(".modal").slideUp(150);
	});


	$("nav[role=menu] .folders").sortable({
		placeholder: "folder placeholder container",
		update: function(event, ui) {
			var order = [];
			var items = ui.item.parents(".folders").find(".folder");

			for (var i=0; i<items.length; i++) {
				var item = $(items[i]);
				order.push(item.attr("data-slug"));
			}

			$.ajax({
				url: '/api/folder/update-order/?order=' + order,
				method: 'POST',
				success: function(data) {
				},
				error: function(data) {
					console.log("Error! :(", data);
				},
			});
		},
	});

	$("ul.booklist").sortable({
		placeholder: "placeholder container",
		update: function(event, ui) {
			var order = [];
			var items = ui.item.parents("ul.booklist").find("li");

			for (var i=0; i<items.length; i++) {
				var item = $(items[i]);
				order.push(item.attr("data-reading-id"));
			}

			$.ajax({
				url: '/api/reading/update-order/?order=' + order,
				method: 'POST',
				success: function(data) {
				},
				error: function(data) {
					console.log("Error! :(", data);
				},
			});
		},
	});


	// Adding a book
	$("#add-book-form").on("submit", function() {
		var starting_page = $(this).find("input[name=starting_page]").val().trim();
		starting_page = (starting_page != '') ? parseInt(starting_page) : 1;

		data = {
			title: $(this).find("input[name=title]").val().trim(),
			author: $(this).find("input[name=author]").val().trim(),
			num_pages: parseInt($(this).find("input[name=num_pages]").val().trim()),
			starting_page: starting_page,
		};

		$.ajax({
			url: '/add/',
			method: 'POST',
			data: data,
			success: function(data) {
				console.log("success", data);
				window.location.href = "/";
			},
			error: function(data) {
				console.log("Error! :(", data);
			},
		});

		return false;
	});
});


// From https://gist.github.com/alanhamlett/6316427
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i=0; i<cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
