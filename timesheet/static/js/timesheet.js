/**
 * Created by sergio on 31/03/14.
 */


    $("#datePicker").on('changeDate', function (ev)   {
                    window.location.href="/timesheet/day/"+$("#datePicker").data('date')
                });


    $("#edit-duration").popover();
    $("#new-duration").popover();

    $('#edit-entry-modal').on('hidden.bs.modal', function (e) {
      $('#edit-duration').popover('hide')
    })

    $('#new-entry-modal').on('hidden.bs.modal', function (e) {
      $('#new-duration').popover('hide')
    })

    function validateTime(time){
        var reg = new RegExp("^[0-9]+[\.\:]?[0-9]+$");
        if(time.length>0 && reg.test(time))
            return true;
        return false;
    }

    function convertTime(time){
        array = time.split(":");

        if(array.length==2){
            time = array[0]+"."+array[1]/60;
        }

        return time;
    }

    function removeProjectFromUser(taskId){
        $("#"+taskId).remove();
        /*
        $.ajax({
            url : '/manage/task/'+userId,
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
        */
    }
    $("#remove").click(function(){
        removeProjectFromUser($("#edit-taskId").val())
    });

    $("#save").click(function(){
        if(!validateTime($("#new-duration").val())){
            $("#new-duration-content").addClass("has-error");
            return;
        }

        convertTime("");
        return;
      addNewTask();
      $('#new-entry-modal').modal('hide');
    });

    function addNewTask(){
              projectName=$( "#new-project option:selected" ).text();
              taskType=$( "#new-task option:selected" ).text();
              description=$("#new-description").val();
              duration=convertTime($("#new-duration").val());
              date = $("#new-date").val();
              projectId = $("#new-project").val();
              taskId = $("#new-task").val();

              var html = '<li id="'+taskId+ '">';
              html += '<div class="manage-list-item col disabled-hightlight">';
              html += ' <div class="col-xs-10 col-md-10 left left-block">';
              html += '<h3 >'+projectName+' - ('+taskType+')</h3>';
              html += '<p>'+description+'</p>';
              html += '</div>';
              html += '<div class="col-xs-2 col-md-2 right right-block">';
              html += '<h3>'+duration+'</h3>';
              html += '<button type="button" class="btn btn-default btn-lg" onclick="javascript:showEditModal('+taskId+','+projectId+','+taskType+','+description+','+duration+')">';
              html += '<span class="glyphicon glyphicon-pencil"></span>';
              html += '</button>';
              html += '</div>';
              html += '</div>';
              html += '</li>';



              $("#tasks").append(html);

              $("#new-project").val("");
              $("#new-task").val("");
              $("#new-description").val("");
              $("#new-duration").val("");
              $("#new-duration-content").removeClass("has-error");

        /*
        $.ajax({
            url : '/manage/task/',
            data : {'date':date,'projectId':projectId,'taskId':taskId,'duration':duration,'description':description},
            type : 'POST',
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
        */
    }

    function showEditModal(taskId,projectId,type,description,duration){
        $("#edit-description").val(description);
        $("#edit-duration").val(duration);
        $("#edit-project").val(projectId);
        $("#edit-type").val(type);
        $("#edit-taskId").val(taskId);
        $("#edit-entry-modal").modal("show");

    }

    $("#update").click(function(){
        if(!validateTime($("#edit-duration").val())){
            $("#edit-duration-content").addClass("has-error");
            return;
        }
        editNewTask();
        $('#edit-entry-modal').modal('hide');
    });

    function editNewTask(){
          projectName=$( "#edit-project option:selected" ).text();
          taskType=$( "#edit-task option:selected" ).text();
          description=$("#edit-description").val();
          duration=convertTime($("#edit-duration").val());
          date = $("#edit-date").val();
          taskId = $("#edit-taskId").val();

          $("#edit-description").val("");
          $("#edit-duration").val("");
          $("#edit-project").val("");
          $("#edit-type").val("");
          $("#edit-taskId").val("");
          $("#edit-duration-content").removeClass("has-error");
        /*
        $.ajax({
            url : '/manage/task/'+userId,
            data : {'taskId':taskId,'projectId':projectId,'taskId':taskId,'duration':duration,'description':description},
            type : 'PUT',
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
        */
    }


    $("#edit-duration").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and , .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 188, 190]) !== -1 ||
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

    $("#new-duration").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and , .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 188, 190]) !== -1 ||
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