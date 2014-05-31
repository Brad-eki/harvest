/**
 * Created by sergio on 31/03/14.
 */


$(".project").click(function(){
    window.location="/manage/projects/edit/"+$(this).attr('id');

});

function archiveProject(projectId, archive){
    $("#"+projectId).remove();

    var count = $(".manage-list").children().length - 1;
    if(count>0)
        $("#projects-count").text("Projects ("+count+")");
    else $("#projects-count").text("Projects (0)");

    $.ajax({
        url : '/manage/projects/archive/'+projectId+"/?archive="+archive,
        data : {},
        type : 'GET',
        dataType : 'json',
        success : function(json) {

        },
        error : function(jqXHR, status, error) {
           alert("error: "+error);
        },
        complete : function(jqXHR, status) {
        }
    });

    return false;
}

function validateProjectForm(){

    if($("#project-name").val().length == 0 || $("#project-type").val().length==0){
        $("#project-error").fadeIn(300);

        if($("#project-name").val().length == 0)
            $("#form-project-name").addClass("has-error");

        if($("#project-type").val().length == 0)
            $("#form-project-type").addClass("has-error");

        return false;
    }

    var numbers = /^[0-9]+$/;
    if($("#estimated-hours").val().length != 0 && !$("#estimated-hours").val().match(numbers)){
        $("#form-estimated_hours").addClass("has-error");
        return false;
    }

    return true;
}

  $("#estimated-hours").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
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


