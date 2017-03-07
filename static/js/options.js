
$(document).ready(function(){
    $('li#options_button').click(function(){
        var $this = $(this);

        if($this.hasClass('open')){
            close_options($this);
        } else {
            open_options($this);
        }
    })

    $('input[type="file"]').change(function(e){
        var $this = $(this);
        var target_id = $this.attr('for');
        $('input#'+target_id).val(e.target.files[0].path)
    })

    $('i.checkbox').click(function(){
        $this = $(this);
        if($this.attr('value') == 'true'){
            $this.attr('value', 'false');
            $this.removeClass('ion-android-checkbox-outline').addClass('ion-android-checkbox-outline-blank');
        } else {
            $this.attr('value', 'true');
            $this.removeClass('ion-android-checkbox-outline-blank').addClass('ion-android-checkbox-outline');
        }
    })

    $('span#save_options').click(function(){
        var config = {}
        $('div#options input').each(function(i, elem){
            var $elem = $(elem);
            config[$elem.attr('name')] = $elem.val();
        });

        $('div#options i.checkbox').each(function(i, elem){
            var $elem = $(elem);
            config[$elem.attr('name')] = $elem.attr('value');
        });

        if(Options.write_config(JSON.stringify(config))){
            toastr['success']('Options saved.')
        } else {
            toastr['error']('Something went horribly wrong.')
        }

    });

});

function open_options($this){
    conf = JSON.parse(Options.get_config());
    $this.addClass('open')

    $.each(conf, function(k, v){
        $('[name="'+k+'"]').attr('value', v);
    })

    var $options = $('div#options');
    var $library = $('ul#library');
    var $i = $this.find('i');

    $i.removeClass('ion-android-settings').addClass('ion-arrow-down-b')
    $('li#scan_library').fadeTo(250, 0.5).addClass('disabled');

    checkboxes();

    // style our buttons
    $('button._htmlpy_button').each(function(){
        $this = $(this);
        var props = $this.prop("attributes");
        var $icon = $('<i></i>')
        $.each(props, function(){
            $icon.attr(this.name, this.value)
        });
        $icon.attr('class', 'icon ion-android-folder')
        $this.html($icon)
    })

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


function checkboxes(){
    $('i.checkbox').each(function(i, elem){
        var $elem = $(elem);
        if($elem.attr('value') == 'true'){
            $elem.removeClass('ion-android-checkbox-outline-blank').addClass('ion-android-checkbox-outline')
        }
    })

}
