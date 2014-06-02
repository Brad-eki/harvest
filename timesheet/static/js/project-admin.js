/**
 * Created by sergio on 31/03/14.
 */

function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(".project").click(function(){
    window.location="/manage/projects/"+$(this).attr('id')+"/edit/";
});

function archiveProject(projectId, archive){
    $("#"+projectId).remove();

    var count = $(".manage-list").children().length - 1;
    if(count>0)
        $("#projects-count").text("Projects ("+count+")");
    else $("#projects-count").text("Projects (0)");

    $.ajax({
        url : "/manage/projects/"+projectId+"/archive/?archive="+archive,
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




$("#assign-users").click(function(){
    var array = $(".chosen-select").val();

    if(array==null)
        return;

    var projectId = $("#projectId").val();
    var usersStr = "users=";

    for(var i=0; i < array.length; i++){
        if(array[i]!=""){
            var userName = $(".chosen-select option[value='"+array[i]+"']").text();
            usersStr += array[i];

            if(i != array.length-1)
                usersStr += ",";

            addUsersToTable(array[i],userName,projectId);
            $(".chosen-select option[value='"+array[i]+"']").attr('disabled','disabled');
        }
    }

    $(".chosen-select").val('').trigger("chosen:updated");
  //  $('.search-choice').remove();

    if(usersStr!="users=")
        addUsersToProject(projectId,usersStr);

});

function addUsersToTable(userId,userName,projectId){
     var newRow = '<tr id="'+userId+'">';
     newRow += '<td class="decoration-none">';
     newRow +=  '<a href="javascript:removeUserFromProject(\''+userId+'\',\''+projectId+'\')">';
     newRow += '<span class="glyphicon glyphicon-remove"></span>';
     newRow += '<span class="proyect-link">'+userName+'</span></a>';
     newRow += '</td>';
     newRow += '</tr>';
     $( ".user-list .table" ).append( newRow );
}

function addUsersToProject(projectId,users){
    $("#assign-users-loading").css("display","inline");
    $.ajax({
        url : '/manage/projects/'+projectId+'/add/users/',
        data : users,
        type : 'POST',
        dataType : 'json',
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        success : function(json) {

        },
        error : function(jqXHR, status, error) {
           alert("error: "+error);
        },
        complete : function(jqXHR, status) {
            $("#assign-users-loading").css("display","none");
        }
    });
}


function removeUserFromProject(userId,projectId){
    $(".chosen-select option[value='"+userId+"']").removeAttr('disabled');
    $(".chosen-select").val('').trigger("chosen:updated");
    $("#"+userId).remove();
    $.ajax({
        url : '/manage/projects/'+projectId+'/remove/users/'+userId+'/',
        data : {},
        type : 'DELETE',
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        dataType : 'json',
        success : function(json) {

        },
        error : function(jqXHR, status, error) {
           alert("error: "+error);
        },
        complete : function(jqXHR, status) {
        }
    });
}
