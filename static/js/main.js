$(document).ready(function(){
    cwd = $('meta[name="cwd"]').attr('content');

    var $close_window = $('ul#menu_bar li#close_window');

    if($('meta[name="start_fullscreen"]').attr('content') == "true"){
        $close_window.show();
    }

    $('ul#menu_bar li#toggle_fullscreen').click(function(){
        Gui.toggle_fullscreen();
        $close_window.toggle();
    })

    $close_window.click(function(){
        Gui.close_window();
    })

});
