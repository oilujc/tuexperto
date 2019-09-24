
init();

function init() {

	if ($("#id_category").val() !== null && $("#id_subcategory").val() !== null){
		searchSubcategory($("#id_category").val(), $("#id_subcategory").val());
	} else {
		cleanSubcategory();
	}
}

function cleanSubcategory() {
	$("#id_subcategory").find("option").remove().end().prepend('<option selected >---------</option>');
}

function searchSubcategory(category, subcategory = null) {
	$.ajax({
		url: `/api/subcategory/`,
		type: 'GET',
		dataType: 'json',
		data: {category: category},
		beforeSend: function( xhr ) {
		    cleanSubcategory();
		},
		success: function(data) {
			$.each(data, function(index, val) {
				 /* iterate through array or object */
				if (subcategory !== null) {
					if (val.id == subcategory) {
						$("#id_subcategory").append(`<option value=${val.id} selected>${val.subcategory}</option>`)
					} else {
						$("#id_subcategory").append(`<option value=${val.id}>${val.subcategory}</option>`)
					}
				} else {
					$("#id_subcategory").append(`<option value=${val.id}>${val.subcategory}</option>`)
				}

									
			});
		}
	});
}

$("#id_category").change(function(event) {
	/* Act on the event */
	var value = $(this).val();
	searchSubcategory(value);
	
});