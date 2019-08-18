$(document).ready(function() {
    // 手机导航
    $('.menuBtn').append('<b></b><b></b><b></b>');
    $('.menuBtn').click(function(event) {
        $(this).toggleClass('open');
        var _winw = $(window).width();
        var _winh = $(window).height();
        if ($(this).hasClass('open')) {
            $('body').addClass('open');
            if (_winw <= 768) {
                $('.nav-m').stop().slideDown();
            }
        } else {
            $('body').removeClass('open');
            if (_winw <= 768) {
                $('.nav-m').stop().slideUp();
            }
        }
    });
    $(window).on('resize', function(e) {
        if ($(window).width() > 768) {
            $('.menuBtn').removeClass('open');
            $('.nav').css('display', '');
        }
    });
    $('.nav li').bind('mouseenter', function() {
        $(this).find('.box').stop().slideDown("fast");
        // if( $(this).find('.box').length ){
        //     $(this).addClass('on');
        // };
    });
    $('.nav li').bind('mouseleave', function() {
        // $(this).removeClass('on');
        $(this).find('.box').stop().slideUp("fast");
    });

    // 选项卡 鼠标经过切换
    $(".TAB li").mousemove(function() {
        var tab = $(this).parent(".TAB");
        var con = tab.attr("id");
        var on = tab.find("li").index(this);
        $(this).addClass('hover').siblings(tab.find("li")).removeClass('hover');
        $(con).eq(on).show().siblings(con).hide();
    });
    //弹窗
    $('.myfancy').click(function() {
        var _id = $(this).attr('href');
        $(_id).fadeIn("normal");
    });
    $('.pop-bg,.g-close,.mob-pop1 .btn,.close').click(function() {
        $(this).parents('.m-pop').fadeOut("normal");
    });
    // 多个选项卡 鼠标经过切换
    $(".TAB2 li").mousemove(function() {
        var tab = $(this).parent(".TAB2");
        var con = tab.attr("id");
        var on = tab.find("li").index(this);
        var mkt = $(this).parents('.mkt')
        $(this).addClass('hover').siblings(tab.find("li")).removeClass('hover');
        $(mkt).find(con).removeClass('ok');
        $(mkt).find('.pic-scr').find(con).eq(on).addClass('ok');
        $(mkt).find('.txt-mkt').find(con).eq(on).addClass('ok');
    });
    $(".TAB3 li").mousemove(function() {
        var tab = $(this).parent(".TAB3");
        var con = tab.attr("id");
        var on = tab.find("li").index(this);
        var mkt = $(this).parents('.fifth')
        $(this).addClass('hover').siblings(tab.find("li")).removeClass('hover');
        $(mkt).find(con).removeClass('ok');
        $(mkt).find('.right').find(con).eq(on).addClass('ok');
        $(mkt).find('.txt').find(con).eq(on).addClass('ok');
    });
    // 锚点跳转

    //外卖系统二级导航吸顶
    var win_w = $(window).width();
    $(window).scroll(function() {
        if (win_w > 768) {
            var h1 = $(window).scrollTop();
            var header = $('body.erji .header');
            var menu = $('body.erji .m-menu');
            if (h1 > 1) {
                header.hide();
                menu.addClass('fixedTop');

            } else {
                header.show();
                menu.removeClass('fixedTop');
            }
        }
    })



});