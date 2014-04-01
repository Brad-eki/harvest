/**
 * Created by sergio on 31/03/14.
 */
$(function () {

    $(".user").click(function(){
        window.location="/manage/projects/edit/"+$(this).attr('id');

    });

    $(".archived").click(function(){
        $(this).remove();
        //TODO: llamar al WS
    });

    function validateProjectForm(){
        if($("#project-name").val().length == 0 || $("#project-type").val().length==0){
            $("#edit-project-error").fadeIn(300);

            if($("#project-name").val().length == 0)
                $("#form-project-name").addClass("has-error");

            if($("#project-type").val().length == 0)
                $("#form-project-type").addClass("has-error");

            return false;
        }
        return true;
    }

    $("#edit-project").click(function(){

        if(validateProjectForm()){
            $("#content_profile_password").fadeOut(0);
            window.location="/manage/projects/";
            //TODO: llamar al WS
        }

    });

    $("#create-project").click(function(){

        if(validateProjectForm()){
            $("#content_profile_password").fadeOut(0);
            window.location="/manage/projects/";
            //TODO: llamar al WS
        }

    });

    $("#navigation_profile_users").click(function(){
        $(".menu-items li").removeClass("selected");
        $(this).addClass("selected");
        $("#content_profile_users").fadeIn(300);
        $("#content_profile_base").fadeOut(0);
    });

    $("#navigation_profile_base").click(function(){
        $(".menu-items li").removeClass("selected");
        $(this).addClass("selected");
        $("#content_profile_users").fadeOut(0);
        $("#content_profile_base").fadeIn(300);
    });

});
