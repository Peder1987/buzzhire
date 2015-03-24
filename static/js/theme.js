
jQuery(document).ready(function() {

/***** Scroll Up *****/

		$('a[href*=#]').bind("click", function(e){
			var anchor = $(this);
			$('html, body').stop().animate({
				scrollTop: $(anchor.attr('href')).offset().top - 50
			}, 1500);
			e.preventDefault();
		});

    $(window).scroll(function() {
      if ($(this).scrollTop() > 100) {
        $('.menu-top').addClass('menu-shrink');
      } else {
        $('.menu-top').removeClass('menu-shrink');
      }
    });

		$(document).on('click','.navbar-collapse.in',function(e) {
			if( $(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle' ) {
				$(this).collapse('hide');
			}
		});


	
/***** Background slideshow *****/

    var background_images = $('.top-content').data('background-images');
	$('.top-content').backstretch(background_images, {duration: 3000, fade: 800});
    

/***** Contact form *****/
	    
//    $('.contact-form form input[type="text"], .contact-form form textarea').on('focus', function() {
//    	$('.contact-form form input[type="text"], .contact-form form textarea').removeClass('contact-error');
//    });
//	$('.contact-form form').submit(function(e) {
//		e.preventDefault();
//	    $('.contact-form form input[type="text"], .contact-form form textarea').removeClass('contact-error');
//	    var postdata = $('.contact-form form').serialize();
//	    $.ajax({
//	        type: 'POST',
//	        url: 'assets/contact.php',
//	        data: postdata,
//	        dataType: 'json',
//	        success: function(json) {
//	            if(json.emailMessage != '') {
//	                $('.contact-form form .contact-email').addClass('contact-error');
//	            }
//	            if(json.subjectMessage != '') {
//	                $('.contact-form form .contact-subject').addClass('contact-error');
//	            }
//	            if(json.messageMessage != '') {
//	                $('.contact-form form textarea').addClass('contact-error');
//	            }
//	            if(json.emailMessage == '' && json.subjectMessage == '' && json.messageMessage == '') {
//	                $('.contact-form form').fadeOut('fast', function() {
//	                    $('.contact-form').append('<p>Thanks for contacting us!</p>');
//	                });
//	            }
//	        }
//	    });
//	});

    
});

