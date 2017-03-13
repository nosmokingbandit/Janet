$(document).ready(function(){
    cwd = $('meta[name="cwd"]').attr('content');
    window.$library = $('ul#library');
    window.$ligames = $('li.game');

    // Show close button if fullscreen
    var $close_window = $('ul#menu_bar li#close_window');
    if($('meta[name="start_fullscreen"]').attr('content') == "true"){
        $close_window.show();
    }

    $close_window.click(function(){
        Janet.exit();
    })

    $('ul#menu_bar li#toggle_fullscreen').click(function(){
        $this = $(this);
        if($this.attr('fullscreen') == 'true'){
            $this.attr('fullscreen', 'false')
            $this.find('i').removeClass('ion-android-contract').addClass('ion-android-expand')
            $close_window.hide();
        } else {
            $this.attr('fullscreen', 'true')
            $this.find('i').removeClass('ion-android-expand').addClass('ion-android-contract')
            $close_window.show();
        }

        Janet.toggle_fullscreen();
    })

    // Library Style Options //
    $library = $('ul#library');
    $library_wrapper = $('div#library_size_wrapper');
    library_size = Math.round(parseInt($library_wrapper.css('font-size')) / 1.6 ) * 10;

    // size slider
    $("#slider").slider({
        range: "min",
        max: 200,
        min: 60,
        value: library_size,
        step: 20,
        slide: function( event, ui ) {
            var ratio = ui.value;
            $library_wrapper.css('font-size', ratio+'%')
            Janet.set_option('game_image_size', ratio);
        }
    });

    $('li#toggle_display').click(function(){
        $this = $(this);
        $i = $this.find('i');
        if($library.hasClass('banner')){
            $i.removeClass('ion-ios-grid-view').addClass('ion-grid')
            $library.removeClass('banner').addClass('icon')
            Janet.set_option('library_style', 'icon')
        } else {
            $i.removeClass('ion-grid').addClass('ion-ios-grid-view')
            $library.removeClass('icon').addClass('banner')
            Janet.set_option('library_style', 'banner')
        }

    })

});

function gamepad_status(connected){
    $(document).ready(function(){
        var $icon = $('ul#ui_bar li#gamepad i');
        $ligames = $('li.game');
        if(connected){
            $icon.removeClass('ion-ios-game-controller-a-outline').addClass('ion-ios-game-controller-a')
            $('ul#library').css('cursor', 'none');
            $ligames.css('pointer-events', 'none');
            $ligames.first().addClass('active');
        } else {
            $icon.removeClass('ion-ios-game-controller-a').addClass('ion-ios-game-controller-a-outline')
            toastr.warning('Gamepad Disconnected');
            $('ul#library').css('cursor', 'default');
            $ligames.css('pointer-events', 'auto')
        }
    })
}

function gamepad_input(commands){
    var $active = $('li.game.active')
    var active_index = $ligames.index($active)
    var row = Math.floor($library.width() / $ligames.outerWidth(true))

    console.log(commands)

    if(active_index == -1){
        $($ligames.get(0)).addClass('active')
        return
    }

    if(commands['buttons'] > 0){
        $active.trigger('click');
        return
    }

    if(commands['dpad'] == 'left' && active_index > 0){
        move_game_focus(active_index, -1)
    } else if(commands['dpad'] == 'right' && active_index < ($ligames.length -1)){
        move_game_focus(active_index, 1)
    } else if(commands['dpad'] == 'up' && active_index >= row){
        move_game_focus(active_index, -row);
    } else if(commands['dpad'] == 'down' && active_index < ($ligames.length - row)){
        move_game_focus(active_index, row);
    }

}

function move_game_focus(current, distance){
    $($ligames.get(current + distance)).addClass('active');
    $($ligames.get(current)).removeClass('active');
}

function update_bg_image(image){
    $('body').css('background-image', `url(${image})`);
}
