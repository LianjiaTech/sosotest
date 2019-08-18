"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/uiMobileServer/getUiMobileServerSubPage", async: false, type: "post", data: data});
        $("#uiMobileServerSubPage").html(htmlobj.responseText);
    };

    context.pageCall = function (pageNum) {
        page = pageNum;
        context.selected();
    };

    context.ReloadPage = function(){
        location.reload();
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
        $("#serverName").attr("disabled", false);
        $("#serverName").val("");
        $("#serverDesc").val("");
        $("#serverType").val("1");
        $("#status").val("0");
        $("#executeTaskId").val("");
        $("#serverIp").val("");
        $("#serverPort").val("");
        $("#udid").val("");
        $("#deviceName").val("");
        $("#wdaLocalPort").val("8000");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addUiMobileServerBtn = function () {
        $("#serverName").attr("disabled", false);
        $("#submit").attr("onclick", "addUiMobileServer()");
        context.openDiv('uiMobileServerAddSubPage', 'bgdiv', '添加uiMobileServer');
    };

    context.getPageUiMobileServerData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var uiMobileServerData = {};
        uiMobileServerData["serverName"] = $("#serverName").val().trim();
        uiMobileServerData["serverDesc"] = $("#serverDesc").val().trim();
        uiMobileServerData["serverType"] = $("#serverType").val().trim();
        uiMobileServerData["status"] = $("#status").val().trim();
        uiMobileServerData["executeTaskId"] = $("#executeTaskId").val().trim();
        uiMobileServerData["serverIp"] = $("#serverIp").val().trim();
        uiMobileServerData["serverPort"] = $("#serverPort").val().trim();
        uiMobileServerData["udid"] = $("#udid").val().trim();
        uiMobileServerData["deviceName"] = $("#deviceName").val().trim();
        uiMobileServerData["wdaLocalPort"] = $("#wdaLocalPort").val().trim();
        return uiMobileServerData;
    };


    context.addUiMobileServer = function () {
        var uiMobileServerData = context.getPageUiMobileServerData();
        if (!uiMobileServerData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/uiMobileServer/addUiMobileServer",
            type: "post",
            data: {"uiMobileServerData": JSON.stringify(uiMobileServerData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('uiMobileServerAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editUiMobileServerBtn = function (uiMobileServerId) {
        var request = $.ajax({url: "/myadmin/uiMobileServer/getUiMobileServerForId", data: {"uiMobileServerId": uiMobileServerId}, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("uiMobileServer查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editUiMobileServer('" + uiMobileServerId + "')");

        context.openDiv('uiMobileServerAddSubPage', 'bgdiv', '编辑uiMobileServer');
         $("#serverName").attr("disabled", true);
        $("#serverName").val(requestBody["serverName"]);
        $("#serverDesc").val(requestBody["serverDesc"]);
        $("#serverType").val(requestBody["serverType"]);
        $("#status").val(requestBody["status"]);
        $("#executeTaskId").val(requestBody["executeTaskId"]);
        $("#serverIp").val(requestBody["serverIp"]);
        $("#serverPort").val(requestBody["serverPort"]);
        $("#udid").val(requestBody["udid"]);
        $("#deviceName").val(requestBody["deviceName"]);
        $("#wdaLocalPort").val(requestBody["wdaLocalPort"]);
    };

    context.editUiMobileServer = function (uiMobileServerId) {
        var uiMobileServerData = context.getPageUiMobileServerData();
        if (!uiMobileServerData) {
            return;
        }
        uiMobileServerData["id"] = uiMobileServerId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/uiMobileServer/editUiMobileServer",
            type: "post",
            data: {"uiMobileServerData": JSON.stringify(uiMobileServerData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('uiMobileServerAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteUiMobileServerBtn = function (element, uiMobileServerId) {
        if (!confirm("确认删除 [" + $("#serverName_" + uiMobileServerId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/uiMobileServer/deleteUiMobileServer",
            type: "post",
            data: {"uiMobileServerId": uiMobileServerId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetUiMobileServerBtn = function (element, uiMobileServerId) {
        if (!confirm("确认启用 [" + $("#serverName_" + uiMobileServerId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/uiMobileServer/resetUiMobileServer",
            type: "post",
            data: {"uiMobileServerId": uiMobileServerId},
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
        checkArr.serverName = $("#queryServerName").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "serverName") {
                key = "版本";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };


    
    context.delQuery = function (condition) {
        if (condition === "serverName") {
            $("#queryServerName").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();


