var table = $('#keys-table').DataTable({
	pagingType: "simple_numbers",
	initComplete: function() {
	$("<div id='keys-table-tablediv'></div>'").insertAfter("#keys-table_filter");
	$("#keys-table-tablediv").addClass("overflow-x-auto relative shadow-md sm:rounded-lg md:col-span-2'></div>");
	$("#keys-table-tablediv").append($("#keys-table"));
	$('#keys-table').addClass("w-full text-sm text-left text-gray-500 dark:text-gray-400");
	
	// Info above the table
	$("<div id='keys-table_topinfo'></div>'").insertBefore("#keys-table_length");
	$("#keys-table_topinfo").addClass("flex justify-between mt-2 mb-4");
	$("#keys-table_topinfo").append($("#keys-table_length"));
	$("#keys-table_topinfo").append($("#keys-table_filter"));

	// Length
	$("#keys-table_length").addClass("");
	$("#keys-table_length").append($("#keys-table_length select"));
	$("#keys-table_length > select").addClass("flex w-20 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-1.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500");
	$("#keys-table_length > label").text("Show keys: ");
	$("#keys-table_length > label").addClass("w-full text-md font-medium text-gray-900 dark:text-gray-400");
	$("#keys-table_length > label").insertBefore($("#keys-table_topinfo"));

	// Search
	$("#keys-table_filter").addClass("relative content-end");
	$("#keys-table_filter").append($('<div></div>'));
	$("#keys-table_filter").append($("#keys-table_filter input"));
	$("#keys-table_filter > label").remove();
	$("#keys-table_filter > div").addClass("flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none");
	$("#keys-table_filter > div").append($('<svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>'));
	$("#keys-table_filter > input").addClass("block p-2.5 pl-10 w-72 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500");
	$("#keys-table_filter > input").attr("placeholder", "Search for keys");
	},

	drawCallback: function() {
		styleTableInfo();
	}
});

function styleTableInfo() {
	// Info under the table
	if (!$("#keys-table_botinfo").length) {
		$("<div id='keys-table_botinfo'></div>'").insertBefore("#keys-table_info");
	}
	$("#keys-table_botinfo").addClass("justify-between flex mt-4")
	$("#keys-table_botinfo").append($("#keys-table_info"));
	$("#keys-table_botinfo").append($("#keys-table_paginate"));
	$("#keys-table_info").addClass("text-md text-gray-700 dark:text-gray-400");
	var t = $("#keys-table_info").text().split(" ");
	$("#keys-table_info").empty();
	for (var i=0; i < t.length; i++){
		val = t[i]
		if (isNaN(val)) {
			$("#keys-table_info").append($(`<span>${val}&nbsp;</span>`))
		}
		else {
			$("#keys-table_info").append($(`<b>${val}&nbsp;</b>`))
		}
	}
	$("#keys-table_paginate").addClass("inline-flex items-center -space-x-px");
	$("#keys-table_previous").addClass("block py-2 px-3 ml-0 leading-tight text-gray-500 bg-white rounded-l-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white");
	$("#keys-table_paginate > span > a").addClass("py-2 px-3 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white");
	$("#keys-table_next").addClass("block py-2 px-3 leading-tight text-gray-500 bg-white rounded-r-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white");
}
