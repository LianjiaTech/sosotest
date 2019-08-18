(function (context) {


    context.openDiv =  function(show_div,bg_div,title){
            $("#supPageTitleChangePassword").text(title);
            $("body").attr("style","overflow:scroll;overflow-y:hidden;overflow-x:hidden");
            //弹出详情层
            var obshowdiv =  $('#'+show_div);
            var objclosediv = $('#'+show_div+'> label');
            var obbgdiv = $('#'+bg_div);
            var offtop=obshowdiv.offset().top;
            var offleft=obshowdiv.offset().left;
            obshowdiv.css("top",offtop+160+"px");
            objclosediv.css("top","40px");
            objclosediv.css("left","90%%");
            obshowdiv.show();
            obbgdiv.show();
            $("#fade").show();
            var docheight = $(document).height();
            obbgdiv.height(docheight);
            $('html,body').animate({scrollTop:offtop}, 800);
            obshowdiv.find("text").attr("required","required");

        };

    context.CloseDiv = function (close_div,bg_div) {
        //清空弹出层文本框和下拉框
        $("#password").val("");
        $("#password1").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };


    context.changePasswordBtn = function () {
        $("#password").val("");
        $("#password1").val("");
        context.openDiv('changePasswordSubPage', 'bgdiv', '修改密码');
    };

    context.changePassword = function () {
        var userData = {};
        userData["password"] = $("#password").val().trim();
        userData["password1"] = $("#password1").val().trim();


        if(!userData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/changePassword",type:"post",data:{"userData":JSON.stringify(userData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        console.log(request)
        if (request["code"] === 10000){
            context.CloseDiv('changePasswordSubPage','bgdiv');

        }else {
            alert("错误 " + request["code"] + ":" + request["body"]);
        }
    };





})(window);



