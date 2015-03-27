
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

  // External links open in new tabs
  $.each(['http', 'https'], function( index, protocol ) {
  	$("a[href*='" + protocol + "://']:not([href*='"+location.hostname.replace
	           ("www.","")+"'])").each(function() {
	       $(this).click(function(event) {
	             event.preventDefault();
	             event.stopPropagation();
	             window.open(this.href, '_blank');
	        }).addClass('externalLink');
	    });
  });
	
    
});

