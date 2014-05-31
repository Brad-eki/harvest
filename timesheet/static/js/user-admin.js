/**
 * Created by sergio on 27/03/14.
 */

function archiveUser(userId, archive){
    $("#"+userId).remove();

    var count = $(".manage-list").children().length - 1;
    if(count>0)
        $("#users-count").text("Users ("+count+")");
    else $("#users-count").text("Users (0)");

    $.ajax({
        url : '/manage/users/archive/'+userId+"?archive="+archive,
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
       window.location="/manage/user/edit/"+$(this).attr('id');
    });



    $("#assign-rojects").click(function(){
        var array = $(".chosen-select").val();

        for(var i=0; i < array.length; i++){
            var projectName = $(".chosen-select option[value='"+array[i]+"']").text();
            addProject(array[i],projectName);
            $(".chosen-select option[value='"+array[i]+"']").remove();
        }

        $('.chosen-select').chosen("destroy");
        $('.chosen-select').chosen();

    });

    function addProject(projectId,projectName){
        var newRow = "<tr><td><a href=\"#"+projectId+"\" class=\"remove\"><span class=\"glyphicon glyphicon-remove\"></span></a><a href=\"#"+projectId+"\" class=\"proyect-link\">"+projectName+"</a></td></tr>";
        $( ".proyect-list .table" ).append( newRow );
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
    });

    $("#navigation_profile_base").click(function(){
        $(".menu-items li").removeClass("selected");
        $(this).addClass("selected");
        $("#content_profile_projects").fadeOut(0);
        $("#content_profile_base").fadeIn(300);
        $("#content_profile_password").fadeOut(0);
    });

    $("#navigation_profile_password").click(function(){
        $(".menu-items li").removeClass("selected");
        $(this).addClass("selected");
        $("#content_profile_projects").fadeOut(0);
        $("#content_profile_base").fadeOut(0);
        $("#content_profile_password").fadeIn(300);
    });

    $("#password").keyup(function() {
        password_validation.check_strength($(this).val());
        notifyIfPasswordsMach();
    });

    $("#password_confirmation").keyup(function() {
        notifyIfPasswordsMach();
    });

    function isEmail(email) {
      var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
      return regex.test(email);
    }

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
            //TODO: Llamar al WS de cambio de password
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
