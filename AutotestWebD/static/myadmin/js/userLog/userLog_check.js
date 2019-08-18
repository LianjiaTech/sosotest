"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({
            url: "/myadmin/userLog/getUserLogSubPage",
            async: false,
            type: "post",
            data: data
        });
        $("#userLogSubPage").html(htmlobj.responseText);
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
        $("#loginName").val("");
        $("#userName").val("");
        $("#operationUrl").val("");
        $("#operationDesc").val("");
        $("#operationResult").val("");
        $("#fromHostIp").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addUserLogBtn = function () {
        $("#submit").attr("onclick", "addUserLog()");
        context.openDiv('userLogAddSubPage', 'bgdiv', '添加用户操作日志');
    };

    context.getPageUserLogData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var userLogData = {};
        userLogData["loginName"] = $("#loginName").val().trim();
        userLogData["userName"] = $("#userName").val().trim();
        userLogData["operationUrl"] = $("#operationUrl").val().trim();
        userLogData["operationDesc"] = $("#operationDesc").val().trim();
        userLogData["operationResult"] = $("#operationResult").val().trim();
        userLogData["fromHostIp"] = $("#fromHostIp").val().trim();
        return userLogData;
    };


    context.addUserLog = function () {
        var userLogData = context.getPageUserLogData();
        if (!userLogData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/userLog/addUserLog",
            type: "post",
            data: {"userLogData": JSON.stringify(userLogData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('userLogAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editUserLogBtn = function (userLogId) {
          var request = $.ajax({
            url: "/myadmin/userLog/getUserLogForId",
            type: "post",
            data: {"userLogId": JSON.stringify(userLogId)},
            async: false
        });

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("userLog查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editUserLog('" + userLogId + "')");

        context.openDiv('userLogAddSubPage', 'bgdiv', '编辑用户操作日志');
        $("#loginName").val(requestBody["loginName"]);
        $("#userName").val(requestBody["userName"]);
        $("#operationUrl").val(requestBody["operationUrl"]);
        $("#operationDesc").val(requestBody["operationDesc"]);
        $("#operationResult").val(requestBody["operationResult"]);
        $("#fromHostIp").val(requestBody["fromHostIp"]);
    };

    context.editUserLog = function (userLogId) {
        var userLogData = context.getPageUserLogData();
        if (!userLogData) {
            return;
        }
        userLogData["id"] = userLogId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/userLog/editUserLog",
            type: "post",
            data: {"userLogData": JSON.stringify(userLogData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('userLogAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteUserLogBtn = function (element, userLogId) {
        if (!confirm("确认删除 [" + userLogId + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/userLog/deleteUserLog",
            type: "post",
            data: {"userLogId": userLogId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetUserLogBtn = function (element, userLogId) {
        if (!confirm("确认启用 [" + userLogId + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/userLog/resetUserLog",
            type: "post",
            data: {"userLogId": userLogId},
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
        checkArr.userName = $("#queryUserName").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "userName") {
                key = "用户名";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };


    
    context.delQuery = function (condition) {
        if (condition === "userName") {
            $("#queryUserName").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();


