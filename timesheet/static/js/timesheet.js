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


    $('#datePicker').datepicker();
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

    function updateDurationInTheNavigation(oldDuration, newDuration){
        var total = parseFloat($("#totalHours").text());
        var today = parseFloat($("#today").text());
        today -= oldDuration;
        total -= oldDuration;
        today += newDuration;
        total += newDuration;

        $("#totalHours").text(""+total.toFixed(2));
        $("#today").text(""+today.toFixed(2));
    }

    function validateTime(time){
        var reg = new RegExp("^[0-9]+[\.\:]?[0-9]+$");
        if(time.length>0 && reg.test(time))
            return true;
        return false;
    }

    function convertTime(time){
        array = time.split(":");

        if(array.length==2){
            time = ""+(parseFloat(array[0])+parseFloat(array[1]/60));
        }

        return time;
    }

    function removeProjectFromUser(taskId){

        $.ajax({
            url : '/manage/tasks/'+taskId+'/edit/',
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
                duration=convertTime($("#edit-duration").val());
                updateDurationInTheNavigation(parseFloat(duration), 0.0);
                $("#"+taskId).remove();

            }
        });
    }

    $("#remove").click(function(){
        removeProjectFromUser($("#edit-taskId").val())
    });

    $("#save").click(function(){
        if(!validateTime($("#new-duration").val())){
            $("#new-duration-content").addClass("has-error");
            return;
        }
      addNewTask();
    });

    function createContent(projectName,taskType,description,duration,projectId,taskId){
              var html = '';
              html += '<div class="manage-list-item col disabled-hightlight">';
              html += ' <div class="col-xs-10 col-md-10 left left-block">';
              html += '<h3 >'+projectName+' - ('+taskType+')</h3>';
              html += '<p>'+description+'</p>';
              html += '</div>';
              html += '<div class="col-xs-2 col-md-2 right right-block">';
              html += '<h3>'+parseFloat(duration).toFixed(2)+'</h3>';
              html += '<button type="button" class="btn btn-default btn-lg" onclick="javascript:showEditModal(\''+taskId+'\',\''+projectId+'\',\''+taskType+'\',\''+description+'\',\''+duration+'\')">';
              html += '<span class="glyphicon glyphicon-pencil"></span>';
              html += '</button>';
              html += '</div>';
              html += '</div>';
              return html;
    }

    function addTaskToList(projectName,taskType,description,duration,projectId,taskId){
              var html = '<li id="'+taskId+ '">';
              html += createContent(projectName,taskType,description,duration,projectId,taskId);
              html += '</li>';
              $("#tasks").append(html);
    }

    function addNewTask(){
            projectName=$( "#new-project option:selected" ).text();
            taskType=$( "#new-type option:selected" ).text();
            description=$("#new-description").val();
            duration=convertTime($("#new-duration").val());
            date = $("#new-date").val();
            projectId = $("#new-project").val();

            $.ajax({
                url : '/manage/tasks/new/',
                data : {'date':date,'projectId':projectId,'type':taskType,'duration':duration,'description':description},
                type : 'POST',
                headers: { "X-CSRFToken": getCookie('csrftoken') },
                dataType : 'json',
                success : function(json) {

                },
                error : function(jqXHR, status, error) {
                   alert("error: "+error);
                },
                complete : function(jqXHR, status) {
                //jqXHR.responseJSON
                  if(jqXHR.status==200){
                      taskId = "1"
                      updateDurationInTheNavigation(0.0, parseFloat(duration));
                      addTaskToList(projectName,taskType,description,duration,projectId,taskId)
                      $('#new-entry-modal').modal('hide');
                      $("#new-project").val("");
                      $("#new-task").val("");
                      $("#new-description").val("");
                      $("#new-duration").val("");
                      $("#new-duration-content").removeClass("has-error");
                  }
                }
            });

    }

    var durationAfterEdit = 0;
    function showEditModal(taskId,projectId,type,description,duration){
        $("#edit-description").val(description);
        $("#edit-duration").val(duration);
        durationAfterEdit = duration;
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
    });

    function editNewTask(){
        projectName=$( "#edit-project option:selected" ).text();
        projectId=$( "#edit-project option:selected" ).val();
        taskType=$( "#edit-task option:selected" ).text();
        description=$("#edit-description").val();
        duration=convertTime($("#edit-duration").val());
        date = $("#edit-date").val();
        taskId = $("#edit-taskId").val();

        $.ajax({
            url : '/manage/tasks/'+taskId+'/edit/',
            data : {'date':date,'id':taskId,'projectId':projectId,'type':taskType,'duration':duration,'description':description},
            type : 'POST',
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            dataType : 'json',
            success : function(json) {

            },
            error : function(jqXHR, status, error) {
               alert("error: "+error);
            },
            complete : function(jqXHR, status) {
              updateDurationInTheNavigation(parseFloat(durationAfterEdit), parseFloat(duration));
              durationAfterEdit = 0;
              html = createContent(projectName,taskType,description,duration,projectId,taskId);
              $("#"+taskId).html(html);
              $('#edit-entry-modal').modal('hide');
              $("#edit-description").val("");
              $("#edit-duration").val("");
              $("#edit-project").val("");
              $("#edit-type").val("");
              $("#edit-taskId").val("");
              $("#edit-duration-content").removeClass("has-error");
            }
        });

    }


    $("#edit-duration").keydown(function (e) {
        var n = $("#edit-duration").val().indexOf(".");
        var foundChar = false;

        if(n!=-1)
            foundChar=true;
        else{
            var n = $("#edit-duration").val().indexOf(":");
            if(n!=-1)
                foundChar=true;
        }

        if(foundChar && $.inArray(e.keyCode, [186, 190]) !== -1){
            e.preventDefault();
        }else{
            // Allow: backspace, delete, tab, escape, enter and : .
            if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 186, 190]) !== -1 ||
                 // Allow: Ctrl+A
                (e.keyCode == 65 && e.ctrlKey === true) ||
                (e.shiftKey && e.keyCode == 186) ||
                 // Allow: home, end, left, right
                (e.keyCode >= 35 && e.keyCode <= 39)) {
                     // let it happen, don't do anything
                     return;
            }
            // Ensure that it is a number and stop the keypress
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        }
    });

    $("#new-duration").keydown(function (e) {
        var n = $("#new-duration").val().indexOf(".");
        var foundChar = false;

        if(n!=-1)
            foundChar=true;
        else{
            var n = $("#new-duration").val().indexOf(":");
            if(n!=-1)
                foundChar=true;
        }

        if(foundChar && $.inArray(e.keyCode, [186, 190]) !== -1){
            e.preventDefault();
        }else{
            // Allow: backspace, delete, tab, escape, enter and : .
            if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 186, 190]) !== -1 ||
                 // Allow: Ctrl+A
                (e.keyCode == 65 && e.ctrlKey === true) ||
                (e.shiftKey && e.keyCode == 186) ||
                 // Allow: home, end, left, right
                (e.keyCode >= 35 && e.keyCode <= 39)) {
                     // let it happen, don't do anything
                     return;
            }
            // Ensure that it is a number and stop the keypress
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        }
    });