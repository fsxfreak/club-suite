jQuery(document).ready(function($) {
    console.log("JavaScript Connected")
    $('.modal-button').click(function() {
        var target = $(this).data('target');
        $('html').addClass('has-modal-open');
        $(target).addClass('is-active');
        //$('.modal-close').show();
    });

    $('.modal-background, .modal-close').click(function() {
        $('html').removeClass('has-modal-open');
        $(this).parent().removeClass('is-active');
        //$('.modal-close').hide();
    });

    $('.delete').click(function() {
        $('html').removeClass('has-modal-open');
        $(this).closest('#modal').removeClass('is-active');
        //$('.modal-close').hide();
    });

});
