/**
 * Created by sergio on 27/03/14.
 */


$(window).bind('resize', function(e)
{
    //defined in utils.js
    updateScrollContentHeight(".scroll-content");
});

jQuery( document ).ready(function( $ ) {
    updateScrollContentHeight(".scroll-content");
});


function archiveUser(userId, archive){
    $("#"+userId).remove();

    var count = $(".scroll-content").children().length;
    if(count>0)
        $("#users-count").text("Users ("+count+")");
    else $("#users-count").text("Users (0)");

    $.ajax({
        url : "/manage/users/"+userId+"/archive/?archive="+archive,
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


$(".user").click(function(){
   window.location="/manage/users/"+$(this).attr('id')+"/edit/";
});


$("#assign-projects").click(function(){
    var array = $(".chosen-select").val();

    if(array==null)
        return;

    var userId = $("#userId").val();
    var projectsStr = "projects=";

    for(var i=0; i < array.length; i++){
        if(array[i]!=""){
            var projectName = $(".chosen-select option[value='"+array[i]+"']").text();
            projectsStr += array[i];

            if(i != array.length-1)
                projectsStr += ",";

            addProjectToTable(array[i],projectName,userId);
            $(".chosen-select option[value='"+array[i]+"']").attr('disabled','disabled');
        }
    }

    $(".chosen-select").val('').trigger("chosen:updated");
  //  $('.search-choice').remove();

    if(projectsStr!="projects=")
        addProjectsToUser(userId,projectsStr);

});

function addProjectToTable(projectId,projectName,userId){
     var newRow = '<tr id="'+projectId+'">';
     newRow += '<td class="decoration-none">';
     newRow +=  '<a href="javascript:removeProjectFromUser(\''+projectId+'\',\''+userId+'\')">';
     newRow += '<span class="glyphicon glyphicon-remove"></span>';
     newRow += '<span class="proyect-link">'+projectName+'</span></a>';
     newRow += '</td>';
     newRow += '</tr>';
     $( ".proyect-list .table" ).append( newRow );
}

function addProjectsToUser(userId,projects){
    $("#assign-projects-loading").css("display","inline");
    $.ajax({
        url : '/manage/users/'+userId+'/add/projects/',
        data : projects,
        type : 'POST',
        dataType : 'json',
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        success : function(json) {

        },
        error : function(jqXHR, status, error) {
           alert("error: "+error);
        },
        complete : function(jqXHR, status) {
            $("#assign-projects-loading").css("display","none");
        }
    });
}



function removeProjectFromUser(projectId,userId){
    $(".chosen-select option[value='"+projectId+"']").removeAttr('disabled');
    $(".chosen-select").val('').trigger("chosen:updated");
    $("#"+projectId).remove();
    $.ajax({
        url : '/manage/users/'+userId+'/remove/project/'+projectId+'/',
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

function notifyIfPasswordsMach(){
    var est1 = password_validation.check_confirmation_match();
    var est2 = password_validation.check_length();

    if(est1 && est2){
        $("#password-match-icon").css("display","block");
    }else{
        $("#password-match-icon").css("display","none");
    }
}

$("#navigation_profile_projects").click(function(){
    $(".chosen-container").css("width","100%");
    $(".menu-items li").removeClass("selected");
    $(this).addClass("selected");
    $("#content_profile_projects").fadeIn(300);
    $("#content_profile_base").fadeOut(0);
    $("#content_profile_password").fadeOut(0);
	preventPageShift();    
});

$("#navigation_profile_base").click(function(){
    $(".menu-items li").removeClass("selected");
    $(this).addClass("selected");
    $("#content_profile_projects").fadeOut(0);
    $("#content_profile_base").fadeIn(300);
    $("#content_profile_password").fadeOut(0);
	preventPageShift();    
});

$("#navigation_profile_password").click(function(){
    $(".menu-items li").removeClass("selected");
    $(this).addClass("selected");
    $("#content_profile_projects").fadeOut(0);
    $("#content_profile_base").fadeOut(0);
    $("#content_profile_password").fadeIn(300);
	preventPageShift();    
});

$("#password").keyup(function() {
    password_validation.check_strength($(this).val());
    notifyIfPasswordsMach();
});

$("#password_confirmation").keyup(function() {
    notifyIfPasswordsMach();
});


function validatePassword(){
    var est1 = password_validation.check_confirmation_match();
    var est2 = password_validation.check_length();

    if(!est1 || !est2){
        $("#password-form").addClass("has-error");
        $("#confirm-password-form").addClass("has-error");
    }else{
        $("#password-form").removeClass("has-error");
        $("#confirm-password-form").removeClass("has-error");
    }

    if(est1 && est2)
        return true;
    else return false;
}

function validateCreateUserForm(shouldValidatePassword) {
    var passwordValid = true;

    if(shouldValidatePassword)
        passwordValid = validatePassword();

    if($("#username").val().length<=3){
        $("#username-form").addClass("has-error");
    }else{
        $("#username-form").removeClass("has-error");
    }

    if($("#email").val().length<=0 || !isEmail($("#email").val())){
        $("#email-form").addClass("has-error");
    }else{
        $("#email-form").removeClass("has-error");
    }

    if(passwordValid && $("#username").val().length>0 && $("#email").val().length>0){
        $("#create-user-error").hide(300);
        return true;
    }else{
        $("#create-user-error").show(300);
        return false;
    }
};

$("#reset-password").click(function() {
    var est1 = password_validation.check_confirmation_match();
    var est2 = password_validation.check_length();

    if(est1 && est2){
        $("#reset-password-loading").show(300);
        $("#alert-password-success").show(300);
        $("#alert-password-error").hide(300);
    }else{
        $("#reset-password-loading").hide(300);
        $("#alert-password-success").hide(300);
        $("#alert-password-error").show(300);
    }

});

$('#alert-password-success .close').click(function () {
    $("#alert-password-success").hide(300);
});


$('#photo').change(function (){
        $('.thumbnail').removeClass('selected');
        $('.image-picker :selected').val("");
        $('.image-picker').find(":selected").prop('selected', false);

    /*
    $('.image-picker').find(":selected").prop('selected', false);
jQuery("select.image-picker").imagepicker({
		    hide_select : true,
            show_label  : true,
            clicked:function(){
                $('#photo').val(null);
            }
        });
*/
});



var password_validation= {
    minChar: 4,

	check_strength:function(s) {
		var t = this.strength_score(s)
		switch(t) {
			case 0:
                $("#strength-meter").removeClass("good").removeClass("strong").addClass("weak");
                $("#password-strength").text("Weak");
			break;
			case 1:
                $("#strength-meter").removeClass("weak").removeClass("strong").addClass("good");
                $("#password-strength").text("Good");
			break;
			case 2:
                $("#strength-meter").removeClass("weak").removeClass("good").addClass("strong");
                $("#password-strength").text("Strong")
            break;
            default:
		        $("#strength-meter").removeClass("weak").removeClass("good").removeClass("strong");
                $("#password-strength").text("");
		}
	}
	,strength_score:function(pass) {

            var checks= [
                    /* alphaLower */ {
                        re: /[a-z]/,
                        score: 1
                    },
                    /* alphaUpper */ {
                        re: /[A-Z]/,
                        score: 5
                    },
                    /* mixture of upper and lowercase */ {
                        re: /([a-z].*[A-Z])|([A-Z].*[a-z])/,
                        score: 2
                    },
                    /* threeNumbers */ {
                        re: /(.*[0-9].*[0-9].*[0-9])/,
                        score: 7
                    },
                    /* special chars */ {
                        re: /.[!@#$%^&*?_~]/,
                        score: 5
                    },
                    /* multiple special chars */ {
                        re: /(.*[!@#$%^&*?_~].*[!@#$%^&*?_~])/,
                        score: 7
                    },
                    /* all together now, does it look nice? */ {
                        re: /([a-zA-Z0-9].*[!@#$%^&*?_~])|([!@#$%^&*?_~].*[a-zA-Z0-9])/,
                        score: 3
                    },
                    /* password of a single char sucks */ {
                        re: /(.)\1+$/,
                        score: 2
                    },
                    {
                        re: /password|12345678|87654321|1234|4321|qwer[tu]|asdf[gj]|zxcv[bnm]/i,
                        score : -20
                    }/*,
                   {
                        re: /(.*[111])|(.*[222])|(.*[333])|(.*[444])|(.*[555])|(.*[666])|(.*[777])|(.*[888])|(.*[999])|(.*[000])/,
                        score: -7
                    }
                */
                ];

            var score = 0;
            var	len = pass.length;
            var	diff = len - this.minChar;

            if(len<=0)
                return -1;

            if(diff<0)
                return 0;

            (diff >= 5 && (score += 18)) || (diff >= 3 && (score += 12)) || (diff === 2 && (score += 6));

            $.each(checks, function(key,value){
                pass.match(value.re) && (score += value.score);
            });
            console.info(score);
            // bonus for length per char
            score && (score += len);
            if(score<10)
                return 0;

            if(score<30)
                return 1;

            return 2;
	}
	,check_confirmation_match:function() {
        var p1 = $("#password").val();
        var p2 = $("#password_confirmation").val();
        if(p1 == p2){
            return true;
        }

        return false;
	}
    ,check_length:function() {
        var pass = $("#password").val();
        if(pass.length >= this.minChar){
            return true;
        }else{
            return false;
        }
	}
};

addDOMLoadEvent = (function(){
	// create event function stack
	var load_events = [],
		load_timer,
		script,
		done,
		exec,
		old_onload,
		init = function () {
			done = true;
 
			// kill the timer
			clearInterval(load_timer);
 
			// execute each function in the stack in the order they were added
			while (exec = load_events.shift())
				exec();
 
			if (script) script.onreadystatechange = '';
		};
 
	return function (func) {
		// if the init function was already ran, just run this function now and stop
		if (done) return func();
 
		if (!load_events[0]) {
			// for Mozilla/Opera9
			if (document.addEventListener)
				document.addEventListener("DOMContentLoaded", init, false);
 
			// for Internet Explorer
			/*@cc_on @*/
			/*@if (@_win32)
				document.write("<script id=__ie_onload defer src=//0><\/scr"+"ipt>");
				script = document.getElementById("__ie_onload");
				script.onreadystatechange = function() {
					if (this.readyState == "complete")
						init(); // call the onload handler
				};
			/*@end @*/
 
			// for Safari
			if (/WebKit/i.test(navigator.userAgent)) { // sniff
				load_timer = setInterval(function() {
					if (/loaded|complete/.test(document.readyState))
						init(); // call the onload handler
				}, 10);
			}
 
			// for other browsers set the window.onload, but also execute the old window.onload
			old_onload = window.onload;
			window.onload = function() {
				init();
				if (old_onload) old_onload();
			};
		}
 
		load_events.push(func);
	}
})();
 
function getScrollerWidth() {
	var scr = null;
	var inn = null;
	var wNoScroll = 0;
	var wScroll = 0;
 
	// Outer scrolling div
	scr = document.createElement('div');
	scr.style.position = 'absolute';
	scr.style.top = '-1000px';
	scr.style.left = '-1000px';
	scr.style.width = '100px';
	scr.style.height = '50px';
	// Start with no scrollbar
	scr.style.overflow = 'hidden';
 
	// Inner content div
	inn = document.createElement('div');
	inn.style.width = '100%';
	inn.style.height = '200px';
 
	// Put the inner div in the scrolling div
	scr.appendChild(inn);
	// Append the scrolling div to the doc
	document.body.appendChild(scr);
 
	// Width of the inner div sans scrollbar
	wNoScroll = inn.offsetWidth;
	// Add the scrollbar
	scr.style.overflow = 'auto';
	// Width of the inner div width scrollbar
	wScroll = inn.offsetWidth;
 
	// Remove the scrolling div from the doc
	document.body.removeChild(
		document.body.lastChild);
 
	// Pixel width of the scroller
	return (wNoScroll - wScroll);
}

function preventPageShift() { 
  var root= document.compatMode=='BackCompat'? document.body : document.documentElement;
  var isVerticalScrollbar= root.scrollHeight>root.clientHeight;
  if (isVerticalScrollbar){
	var scrollWidth = getScrollerWidth(); //Returns '0' in IE7, which we want
	document.body.style.marginLeft = scrollWidth+"px"; //Have to use margin for webkit browsers

	$(".navbar").css("padding-left",scrollWidth+"px");
	$(".sub-navbar").css("margin-left",-scrollWidth+"px");        
	$(".sub-navbar").css("padding-left",scrollWidth+"px");   
	$("#footer").css("margin-left",-scrollWidth+"px");        
	$("#footer").css("padding-left",scrollWidth+"px");   			  
  }
  else{ 
	document.body.style.marginLeft = 0; //In case window is resized
	$(".navbar").css("padding-left","0px");
	$(".sub-navbar").css("margin-left","0px");  	
	$(".sub-navbar").css("padding-left","0px");  	
	$("#footer").css("margin-left","0px");  	
	$("#footer").css("padding-left","0px");  			
  }
}