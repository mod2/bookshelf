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
	$(".entry").on("click", function() {
		// Only show if it's not already open
		if ($("#add-entry-modal:visible").length == 0) {
			// On click, populate the dialog and pull it up
			var book = $(this).parents("li:first");		
			if (book.length > 0) {
				var readingId = book.attr("data-reading-id");
			} else {
				var readingId = $(".detail.info").attr("data-reading-id");
			}

			var currentPageNumber = $(this).find(".page_number");
			var endPage = $(this).find(".total").attr("data-end-page");
			var title = book.find(".title").html();

			$("#add-entry-modal").attr("data-reading-id", readingId);
			$("#add-entry-modal .end-page").html(endPage);
			$("#add-entry-modal .title").html(title);

			$("#add-entry-modal").slideDown(150);

			$("#entry-box").focus();
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
					// Update the entry
					if ($("ul.booklist").length) {
						var reading = $("ul.booklist li[data-reading-id=" + data.reading_id + "]");
						reading.removeClass("stale");
					} else {
						var reading = $(".detail.info");
					}
					reading.find(".info .num").html(data.percentage);
					reading.find(".percentage .bar").css("width", data.percentage + "%");
					reading.find(".entry .page_number").html(data.page_number);
					reading.find(".entry .sub .pages").html(data.pages_left);
					reading.find(".stale").slideUp(150);

					// Close the modal and clear it
					$("#add-entry-modal").slideUp(150);
					$("#add-entry-modal #entry-box").val('');
					$("#add-entry-modal textarea#comment").val('');
				},
				error: function(data) {
					console.log("Error! :(", data);
				},
			});
		}

		return false;
	});


	$(".folders").sortable({
		placeholder: "folder-item placeholder container",
		update: function(event, ui) {
			var order = [];
			var items = ui.item.parents(".folders").find(".folder-item");

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

	$("ul.booklist:not(.history)").sortable({
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

	$(document).bind('keypress', '/', function() {
		$(".search input#q").focus();

		return false;
	});

	$(".search input#q").bind('keyup', 'esc', function() {
		$(".search input#q").val('');
		$(".search input#q").blur();

		return false;
	});

	// Hotkey to go home
	$(document).bind('keypress', 'h', function() {
		window.location.href = '/';

		return false;
	});

	// Hotkey to add a book
	$(document).bind('keypress', 'a', function() {
		window.location.href = '/add/';

		return false;
	});

	// See if we're on a page with charts
	if ($(".chart-wrapper").length && data.list) {
		var margin = {
			top: 10,
			right: 10,
			bottom: 10,
			left: 30,
		};

		var width = $(".chart-wrapper").width() - margin.left - margin.right;
		var height = 200 - margin.top - margin.bottom;
		var barWidth = (width - margin.left - margin.right) / data.list.length;

		var y = d3.scale.linear()
			.range([height, 0])
			.domain([data.start_page, data.end_page]);

		var yPercent = d3.scale.linear()
			.range([height, 0])
			.domain([0, 1]);

		var chart = d3.select(".chart-wrapper")
			.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
			.attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

		var bar = chart.selectAll("g")
			.data(data.list)
			.enter().append("g")
			.attr("transform", function(d, i) { return "translate(" + (i * barWidth + margin.left) + ", 0)"; })
	
		// Already-read pages
		var rect = bar.append("rect")
			.data(data.list)
			.attr("y", function(d) { return y(d.base); })
			.attr("height", function(d) { return height - y(d.base); })
			.attr("width", barWidth - 1)
			.attr("transform", "translate(0, " + margin.bottom + ")")
			.attr("class", "base");

		// New pages
		var newRect = bar.append("rect")
			.data(data.list)
			.attr("y", function(d) { return y(d.base + d.new); })
			.attr("height", function(d) { return height - y(d.new); })
			.attr("width", barWidth - 1)
			.attr("transform", "translate(0, " + margin.bottom + ")")
			.attr("class", "new");

		var yAxis = d3.svg.axis()
			.scale(y)
			.orient("left")
			.ticks(5);

		var yPercentAxis = d3.svg.axis()
			.scale(yPercent)
			.orient("right")
			.ticks(2, "%");

		chart.append("g")
			.attr("class", "y axis")
			.attr("transform", "translate(" + margin.left + ", " + margin.top + ")")
			.call(yAxis);

		chart.append("g")
			.attr("class", "y axis right")
			.attr("transform", "translate(" + (width - margin.right - 1) + ", " + margin.top + ")")
			.call(yPercentAxis);

		var line = chart.append("line")
			.attr("x1", margin.left)
			.attr("y1", height)
			.attr("x2", width - margin.right)
			.attr("y2", height)
			.attr("transform", "translate(0, " + margin.bottom + ")")
			.attr("class", "baseline");

	}
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
