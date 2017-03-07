$(document).ready(function(){
    cwd = $('meta[name="cwd"]').attr('content');


    if($('ul#library').attr('data-scan') == 'true'){
        scan_library();
    } else {
        get_existing_library();
    }

    $('li#scan_library').click(scan_library);

    // Launch a title
    $('li.game').click(function(){
        var rpx = $(this).attr('data-rpx');
        if(Library.launch_game(rpx)){
            toastr.success('Launched '+rpx+'.')
        } else {
            toastr.error('Something went horribly wrong.')
        }
    });
});


function scan_library(){
    var $library = $('ul#library');
    $library.find('li').fadeOut(500, function(li){$(li).remove()})
    $('div#loading').fadeIn(500, function(){
        game_data = JSON.parse(Library.scan());

        game_data_interval = setInterval(wait_for_game_data, 1000);
    });
}

function wait_for_game_data() {
        if (game_data !== undefined) {
        clearInterval(game_data_interval)
        render_library(game_data)
    }
}

function get_existing_library(){
    if((game_data = JSON.parse(Library.get_library())) !== ""){
        render_library(game_data)
    }
}

function render_library(game_data){
    var $library = $('ul#library');
    $.each(game_data, function(index, game){
        var li = "<li class='game' title='"+game['title']+"'data-rpx='"+game['binary']+"'><div class='img_container'><img src='file:\\"+cwd+'\\game_covers\\'+game['game_id']+".jpg' onload=ImgLoad(this) onError=ImgError(this) /></div><div class='title'>"+game['title']+"</div></li>"
        $library.append($(li))
    });

    $('div#loading').fadeOut();

    $('li.game').each(function(i, li){
        setTimeout(function(){
            $(li).animate({opacity: 1})
        }, 100 * i)

    });
}

function ImgError(image) {
    var $image = $(image)
    var src = $image.attr('src').split('?')[0]
    var attempts = $image.attr('data-attempts') || 0;

    $image.css('display', 'none')

    if(attempts > 2){
        image.onerror = null;
    } else {
        $image.attr('data-attempts', ++attempts)

        setTimeout(function (){
            $image.attr('src', src += '?' + +new Date).show();
        }, 2000);

    }
}

function ImgLoad(image){
    $(image).animate({opacity: 1})
}
