jQuery(document).ready(function() {
    jQuery("#calendar").datepicker({
        defaultDate: location.href.split('/').slice(4, 7).reverse().join('.'),
        onSelect: function(dateText, inst) {
            location = '/programm/' + dateText.split('.').reverse().join('/');
        }
    });
});
