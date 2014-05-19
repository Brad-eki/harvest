/**
 * Created by sergio on 31/03/14.
 */

$(function () {

    var startDate = new Date(2012,1,20);
	var endDate = new Date(2012,1,25);
	$('#datePicker').datepicker()
				.on('changeDate', function(ev){
					if (ev.date.valueOf() > endDate.valueOf()){
						$('#alert').show().find('strong').text('The start date can not be greater then the end date');
					} else {
						$('#alert').hide();
						startDate = new Date(ev.date);
						$('#startDate').text($('#dp4').data('date'));
					}
					$('#datePicker').datepicker('hide');
				});


    $("#edit-time").popover();
    $("#new-time").popover();

    $('#edit-entry-modal').on('hidden.bs.modal', function (e) {
      $('#edit-time').popover('hide')
    })

    $('#new-entry-modal').on('hidden.bs.modal', function (e) {
      $('#new-time').popover('hide')
    })

});