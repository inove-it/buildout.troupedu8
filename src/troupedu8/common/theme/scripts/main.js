$('.carousel').carousel({
        interval: 5000 //changes the speed
    });

var delayTimer;
jQuery('div.faceted-text-widget').each(function(){
  var wid = jQuery(this).attr('id').split('_')[0];
  var input = jQuery("#" + wid);
  var widget = jQuery('#' + wid + '_widget');
  var button = jQuery('input[type=submit]', widget);
  button.hide();
  input.on('input', function() {
    clearTimeout(delayTimer);
    delayTimer = setTimeout(function() {input.change();}, 300);
  });
});
