$(function() {
	   $(".input-group input").focus(function() {
	
		  $(this).parent(".input-group").each(function() {
			 $("label", this).css({
				"font-size": "15px",
			 })
		  });
	   }).blur(function() {
		  if ($(this).val() == "") {
			 $(this).parent(".input-group").each(function() {
				$("label", this).css({
				   "font-size": "20px",
				})
			 });
		  }
	   });
	});