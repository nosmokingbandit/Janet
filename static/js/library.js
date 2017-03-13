$(document).ready(function(){
    // window.$library = $('ul#library'); declared in main.js
    cwd = $('meta[name="cwd"]').attr('content');
    $title_display = $('div#title_display');

    if($('ul#library').attr('scan') == 'true'){
        scan_library();
    } else {
        Janet.get_library();
    }

    $('li#scan_library').click(scan_library);

});


function scan_library(){
    $library.find('li').fadeOut(500, function(li){$library.empty()})
    $('div#loading').fadeIn(500, function(){
        Janet.scan_library();
    });
}

function render_library(game_data){
    $.each(game_data, function(index, game){
        var li = `
            <li class='game' rpx='${game["binary"]}' onClick='launch_game(this)'>
                <div class='img_container'>
                    <img src='file:\\${cwd}\\game_images\\${game['game_id']}.jpg' onload=ImgLoad(this) onError=ImgError(this) class='banner'/>
                    <img src='file:\\${cwd}\\game_images\\${game['game_id']}_icon.jpg' onload=ImgLoad(this) onError=ImgError(this) class='icon'/>
                </div>
                <span class='tooltiptext'>${game["title"]}</span>
            </li>`
        $library.append($(li))

    });

    window.$ligames = $('li.game')
    $ligames.each(function(i, li){
        if($library.hasClass('banner')){
            $(li).find('img.banner').show();
        } else {
            $(li).find('img.icon').show();
        }


        setTimeout(function(){
            $(li).animate({opacity: 1})
        }, 100 * i)

    });

    $('div#loading').fadeOut();
}


function launch_game(elem){
    Janet.launch_game($(elem).attr('rpx'))
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
    $image = $(image);
    if($library.hasClass('banner') && !$image.hasClass('banner')){
        $image.attr('style', '')
    } else if($library.hasClass('icon') && !$image.hasClass('icon')){
        $image.attr('style', '')
    }

}
