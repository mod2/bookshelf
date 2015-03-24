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

			$("#entry-box").focus();

			$("#add-entry-modal").slideDown(150);
		}

		return false;
	});

	$(".modal .cancel-link").on("click", function() {
		$(".modal").slideUp(150);
	});


	// Adding an entry
	
	$("form#add-entry-modal").on("submit", function() {
		var pageNumber = parseInt($(this).find("#entry-box").val().trim());
		var comment = $(this).find("textarea#comment").val().trim();
		var readingId = parseInt($(this).attr("data-reading-id"));

		if ((pageNumber || comment) && readingId) {
			data = {
				reading_id: readingId,
				page_number: pageNumber,
				comment: comment,
			};

			$.ajax({
				url: '/api/reading/add-entry/',
				method: 'POST',
				data: data,
				success: function(data) {
					console.log("success", data);

					// Update the entry
					var reading = $("ul.booklist li[data-reading-id=" + data.reading_id + "]");
					reading.find(".info .num").html(data.percentage);
					reading.find(".percentage .bar").css("width", data.percentage + "%");
					reading.find(".entry .page_number").html(data.page_number);
					reading.find(".entry .sub .pages").html(data.pages_left);

					// Close the modal and clear it
					$("#add-entry-modal").slideUp(150);
					$("#add-entry-modal input[type=number]").val('');
					$("#add-entry-modal textarea#comment").val('');
				},
				error: function(data) {
					console.log("Error! :(", data);
				},
			});
		}

		return false;
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
