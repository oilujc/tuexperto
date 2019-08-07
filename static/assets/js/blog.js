(function($){
	"use strict";

	/*--------- Category ----------*/
	$('#id_category').change(function(event) {
		/* Act on the event */
		var category = $(this);

		if (category != null) {
			$.ajax({
				url: `/api/subcategory/?category=${category.val()}`,
				type: 'get',
				dataType: "json",
				contentType: 'application/json',
				success: function(data) {
					$.each(data, function(key, value) {   	     
						console.log(key);
						console.log(value);
					});
				}
			});
		}
		
	});
	
	
})(jQuery);