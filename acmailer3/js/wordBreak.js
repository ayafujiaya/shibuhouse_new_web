$(function(){
    var $targetElement = '.wordBreak';
    if($.browser.msie) {
        $($targetElement).css('word-break', 'break-all');
    } else {
        $($targetElement).each(function(){
            if(navigator.userAgent.indexOf('Firefox/2') != -1) {
                $(this).html($(this).text().split('').join('<wbr />'));
            } else {
                $(this).html($(this).text().split('').join(String.fromCharCode(8203)));
            }
        });
    }
});
