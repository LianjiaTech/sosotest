"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/standardEnv/getStandardEnvSubPage", async: false, type: "post", data: data});
        $("#standardEnvSubPage").html(htmlobj.responseText);
    };

    context.pageCall = function (pageNum) {
        page = pageNum;
        context.selected();
    };


    context.openDiv = function (show_div, bg_div, title) {
        $("#supPageTitle").text(title);
        $("body").attr("style", "overflow:scroll;overflow-y:hidden;overflow-x:hidden");
        //弹出详情层
        var obshowdiv = $('#' + show_div);
        var objclosediv = $('#' + show_div + '> label');
        var obbgdiv = $('#' + bg_div);
        var offtop = obshowdiv.offset().top;
        var offleft = obshowdiv.offset().left;
        obshowdiv.css("top", offtop + 160 + "px");
        objclosediv.css("top", "40px");
        objclosediv.css("left", "90%%");
        obshowdiv.show();
        obbgdiv.show();
        $("#fade").show();
        var docheight = $(document).height();
        obbgdiv.height(docheight);
        $('html,body').animate({scrollTop: offtop}, 800);
        // selected();
        // $("#userAddSubPage").css("display","block");
        obshowdiv.find("input").attr("required","required");
    };

    context.CloseDiv = function (close_div, bg_div) {
        //清空弹出层文本框和下拉框
        $("#httpConfKey").val("");
        $("#openApiKey").val("");
        $("#rmiKey").val("");
        $("#version").val("");
        $("#alias").val("");
        $("#actionIsShow").val("");
        $("#rmiIsShow").val("");
        $("#openapiIsShow").val("");
        $("#uiIsShow").val("");
        $("#lineSort").val("");
        $("#httpConfKey").attr("disabled", false);
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addStandardEnvBtn = function () {
        $("#submit").attr("onclick", "addStandardEnv()");
        context.openDiv('standardEnvAddSubPage', 'bgdiv', '添加standardEnv');
    };

    context.getPageStandardEnvData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var standardEnvData = {};
        standardEnvData["httpConfKey"] = $("#httpConfKey").val().trim();
        standardEnvData["openApiKey"] = $("#openApiKey").val().trim();
        standardEnvData["rmiKey"] = $("#rmiKey").val().trim();
        standardEnvData["version"] = $("#version").val().trim();
        standardEnvData["alias"] = $("#alias").val().trim();
        standardEnvData["actionIsShow"] = $("#actionIsShow").val().trim();
        standardEnvData["rmiIsShow"] = $("#rmiIsShow").val().trim();
        standardEnvData["openapiIsShow"] = $("#openapiIsShow").val().trim();
        standardEnvData["uiIsShow"] = $("#uiIsShow").val().trim();
        standardEnvData["lineSort"] = $("#lineSort").val().trim();
        return standardEnvData;
    };


    context.addStandardEnv = function () {
        var standardEnvData = context.getPageStandardEnvData();
        if (!standardEnvData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/standardEnv/addStandardEnv",
            type: "post",
            data: {"standardEnvData": JSON.stringify(standardEnvData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('standardEnvAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editStandardEnvBtn = function (standardEnvId) {
        var request = $.ajax({url: "/myadmin/standardEnv/getStandardEnvForId", data: {"standardEnvId": standardEnvId}, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("standardEnv查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editStandardEnv('" + standardEnvId + "')");

        context.openDiv('standardEnvAddSubPage', 'bgdiv', '编辑standardEnv');
        $("#httpConfKey").attr("disabled", true);
        $("#httpConfKey").val(requestBody["httpConfKey"]);
        $("#openApiKey").val(requestBody["openApiKey"]);
        $("#rmiKey").val(requestBody["rmiKey"]);
        $("#version").val(requestBody["version"]);
        $("#alias").val(requestBody["alias"]);
        $("#actionIsShow").val(requestBody["actionIsShow"]);
        $("#rmiIsShow").val(requestBody["rmiIsShow"]);
        $("#openapiIsShow").val(requestBody["openapiIsShow"]);
        $("#uiIsShow").val(requestBody["uiIsShow"]);
        $("#lineSort").val(requestBody["lineSort"]);
    };

    context.editStandardEnv = function (standardEnvId) {
        var standardEnvData = context.getPageStandardEnvData();
        if (!standardEnvData) {
            return;
        }
        standardEnvData["id"] = standardEnvId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/standardEnv/editStandardEnv",
            type: "post",
            data: {"standardEnvData": JSON.stringify(standardEnvData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('standardEnvAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteStandardEnvBtn = function (element, standardEnvId) {
        if (!confirm("确认删除 [" + $("#httpConfKey_" + standardEnvId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/standardEnv/deleteStandardEnv",
            type: "post",
            data: {"standardEnvId": standardEnvId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.ReloadPage = function(){
        location.reload();
    };

    context.resetStandardEnvBtn = function (element, standardEnvId) {
        if (!confirm("确认启用 [" + $("#httpConfKey_" + standardEnvId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/standardEnv/resetStandardEnv",
            type: "post",
            data: {"standardEnvId": standardEnvId},
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
        if (e.keyCode === 13) {
            context.queryRequest();
        }
    };

    context.queryRequest = function () {
        checkArr.httpConfKey = $("#queryHttpConfKey").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "httpConfKey") {
                key = "http服务的key";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };


    
    context.delQuery = function (condition) {
        if (condition === "httpConfKey") {
            $("#queryHttpConfKey").val("");
        }

        context.queryRequest();
    };


})(window);
// window.doubleBoxFunction();
window.selected();


