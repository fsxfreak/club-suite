jQuery(document).ready(function ($) {
    $('.modal-button').click(function() {
        var target = $(this).data('target');
        $('html').addClass('has-modal-open');
        $(target).addClass('is-active');
    });

    $('.modal-background, .modal-close').click(function() {
        $('html').removeClass('has-modal-open');
        $(this).parent().removeClass('is-active');
    });

    $('.delete').click(function() {
        $('html').removeClass('has-modal-open');
        $(this).closest('#modal').removeClass('is-active');
    });
});
