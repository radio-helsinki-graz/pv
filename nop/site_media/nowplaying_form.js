jQuery(document).ready(function() {
    /*jQuery("#nop_date").dateinput({
        format: 'yyyy-mm-dd',
        firstDay: 1
    });*/
    jQuery("#nop_time").AnyTime_picker({
        format: "%H:%i",
        labelTitle: "Zeit",
        labelHour: "Stunde",
        labelMinute: "Minute"
    });
});
