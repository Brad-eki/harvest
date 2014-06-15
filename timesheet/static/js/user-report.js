/**
 * Created by sergio on 31/03/14.
 */

$(function () {
      $(".user").click(function(){
        window.location="/reports/users/"+$(this).attr('id');

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

