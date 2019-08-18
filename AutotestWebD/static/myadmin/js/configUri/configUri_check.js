"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/configUri/getConfigUriSubPage",async:false,type:"post",data:data});
        $("#configURISubPage").html(htmlobj.responseText);
    };

    context.pageCall = function (pageNum) {
        page = pageNum;
        context.selected();
    };

    context.ReloadPage = function(){
        location.reload();
    };

    context.openDiv =  function(show_div,bg_div,title){
            $("#supPageTitle").text(title);
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
            obshowdiv.find("input").attr("required","required");
        };

    context.CloseDiv = function (close_div,bg_div) {
        //清空弹出层文本框和下拉框
        $("#uriKey").val("");
        $("#alias").val("");
        $("#uriDesc").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.addUriBtn = function () {
        $("#uriKey").attr("disabled", false);
        $("#alias").attr("disabled", false);

        $("#submit").attr("onclick","addUri()");
        context.openDiv('adminAddConfigUriSubPage','bgdiv','添加Uri');
    };

    context.getPageUriData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var uriData = {};
        uriData["uriKey"] = $("#uriKey").val().trim();
        uriData["alias"] = $("#alias").val().trim();
        uriData["uriDesc"] = $("#uriDesc").val().trim();
        uriData["level"] = $("#level").val().trim();
        uriData["protocol"] = $("#protocol").val().trim();

        return uriData;
    };


    context.addUri = function () {
        var uriData = context.getPageUriData();

        if(!uriData){
            return;
        }
        var ajaxRequest = $.ajax({
            url:"/myadmin/configUri/addConfigUri",
            type:"post",
            data:{"uriData":JSON.stringify(uriData)},
            async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddConfigUriSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editConfigUriBtn = function (uriKey) {
        var request = $.ajax({url:"/myadmin/configUri/getConfigUriForId",data:{"uriKey":uriKey},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("uri查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editConfigUri('"+uriKey+"')");

        context.openDiv('adminAddConfigUriSubPage','bgdiv','编辑uri');
        $("#uriKey").attr("disabled", true);
        $("#uriKey").val(requestBody["uriKey"]);
        $("#alias").attr("disabled", true);
        $("#alias").val(requestBody["alias"]);
        $("#uriDesc").val(requestBody["uriDesc"]);
        $("#level").val(requestBody["level"]);
        $("#protocol").val(requestBody["protocol"]);
    };

    context.editConfigUri = function (uriKey) {
        var uriData = context.getPageUriData();
        if(!uriData){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/configUri/editConfigUri",
            type: "post",
            data: {"uriData": JSON.stringify(uriData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddConfigUriSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteConfigUriBtn = function (element, uriKey) {
        if (!confirm("确认删除 [" + uriKey+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/configUri/delConfigUri",
            type: "post",
            data: {"uriKey": uriKey},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetConfigUriBtn = function (element, uriKey) {
        if (!confirm("确认启用 [" + uriKey+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/configUri/resetConfigUri",
            type: "post",
            data: {"uriKey": uriKey},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.EnterPress = function () {
        var e = event || window.event;
        if(e.keyCode === 13){
            context.queryRequest();
        }
    };

    context.queryRequest = function () {
        checkArr.alias = $("#queryAlias").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            };
            var key = "";
            if  (index === "alias"){
                key = "uri名称";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
            
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "alias"){
            $("#queryAlias").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();


