/**
 * Created by sergio on 14/06/14.
 */

function updateScrollContentHeight(elementId){

    if($(elementId)!=undefined){
        hh = $(elementId).attr("data-remove-height")

        if(!isNaN(hh) || hh!=undefined){
            height = getHeight()-hh;
            $(".scroll-content").height(height);
        }
    }
}

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

function getHeight(){
    var myWidth;
    var myHeight;

    if( typeof( window.innerWidth ) == 'number' ) {

    //Non-IE

    myWidth = window.innerWidth;
    myHeight = window.innerHeight;

    } else if( document.documentElement &&

    ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {

    //IE 6+ in 'standards compliant mode'

    myWidth = document.documentElement.clientWidth;
    myHeight = document.documentElement.clientHeight;

    } else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {

    //IE 4 compatible

    myWidth = document.body.clientWidth;
    myHeight = document.body.clientHeight;

    }
    return myHeight;
}

function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
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