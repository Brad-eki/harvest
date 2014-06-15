/**
 * Created by sergio on 31/03/14.
 */

$(function () {
    $(".project").click(function(){
        window.location="/reports/projects/"+$(this).attr('id');
    });

    $( document ).ready(function() {

    });

    $(window).bind('resize', function(e)
    {
        //defined in utils.js
        updateScrollContentHeight(".scroll-content");
    });

    jQuery( document ).ready(function( $ ) {
        updateScrollContentHeight(".scroll-content");
    });
});

