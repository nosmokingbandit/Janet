
$(document).ready(function(){

    init_checkboxes();

    $('li#options_button').click(function(){
        var $this = $(this);

        if($this.hasClass('open')){
            close_options($this);
        } else {
            open_options($this);
        }
    })

    $('i.checkbox').click(function(){
        $this = $(this);
        var key = $this.attr('name')
        if($this.attr('value') == 'true'){
            $this.attr('value', 'false');
            Janet.set_option(key, 'false');
            $this.removeClass('ion-android-checkbox-outline').addClass('ion-android-checkbox-outline-blank');
        } else {
            $this.attr('value', 'true');
            Janet.set_option(key, 'true');
            $this.removeClass('ion-android-checkbox-outline-blank').addClass('ion-android-checkbox-outline');
        }
    })

});

function open_options($this){
    $this.addClass('open')

    var $options = $('div#options');
    var $library = $('ul#library');
    var $i = $this.find('i');

    $i.removeClass('ion-android-settings').addClass('ion-arrow-down-b')
    $('li#scan_library').fadeTo(250, 0.5).addClass('disabled');

    $library.fadeOut();
    $options.fadeIn();
}


function close_options($this){
    $this.removeClass('open')

    var $options = $('div#options');
    var $library = $('ul#library');
    var $i = $this.find('i');

    $i.removeClass('ion-arrow-down-b').addClass('ion-android-settings')
    $('li#scan_library').fadeTo(250, 1).removeClass('disabled');

    $library.fadeIn();
    $options.fadeOut();
}


function init_checkboxes(){
    $('i.checkbox').each(function(i, elem){
        var $elem = $(elem);
        if($elem.attr('value') == 'true'){
            $elem.removeClass('ion-android-checkbox-outline-blank').addClass('ion-android-checkbox-outline');
        }
    })

}
