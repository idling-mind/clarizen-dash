$(document).ready(function(){
    setTimeout(function(){
        var dd = $('.ticker').easyTicker({
            direction: 'down',
            speed: 'slow',
            interval: 5000,
            height: 'auto',
            visible: 4,
            mousePause: 0,
        }).data('easyTicker');
        $('.ticker').show();
    }, 4000)
});