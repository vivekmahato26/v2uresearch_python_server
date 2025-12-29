$(document).ready(function() {
    const $toggle = $('#mobileMenuToggle');
    const $nav = $('#mobileNav');
    const $body = $('body');
    
    // Create overlay if it doesn't exist
    if ($('.mobile-overlay').length === 0) {
        $body.append('<div class="mobile-overlay"></div>');
    }
    const $overlay = $('.mobile-overlay');
    
    console.log('Mobile menu initialized');

    $toggle.on('click', function(e) {
        e.preventDefault();
        console.log('Menu toggle clicked');
        $toggle.toggleClass('active');
        $nav.toggleClass('active');
        $overlay.toggleClass('active');
        
        if ($nav.hasClass('active')) {
            $body.css('overflow', 'hidden');
        } else {
            $body.css('overflow', '');
        }
    });
    
    $overlay.on('click', function() {
        $toggle.removeClass('active');
        $nav.removeClass('active');
        $overlay.removeClass('active');
        $body.css('overflow', '');
    });
    
    // Handle submenu toggles
    $(document).on('click', '.submenu-toggle', function(e) {
        e.preventDefault();
        $(this).parent().toggleClass('active');
    });
    
    // Close mobile menu when clicking a link (except submenu toggles)
    $(document).on('click', '.mobile-menu li a:not(.submenu-toggle)', function() {
        $toggle.removeClass('active');
        $nav.removeClass('active');
        $overlay.removeClass('active');
        $body.css('overflow', '');
    });
});
