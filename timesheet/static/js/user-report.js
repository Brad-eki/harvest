/**
 * Created by sergio on 31/03/14.
 */

$(function () {
      $(".user").click(function(){
        window.location="/reports/users/"+$(this).attr('id');

    });
});
