$(document).ready(function() {
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
});
