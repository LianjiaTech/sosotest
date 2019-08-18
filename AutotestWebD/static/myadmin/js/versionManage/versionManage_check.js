"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/versionManage/getVersionManageSubPage", async: false, type: "post", data: data});
        $("#versionManageSubPage").html(htmlobj.responseText);
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
        $("#versionName").attr("disabled", false);
        $("#versionName").val("");
        $("#versionDesc").val("");
        $("#type").val("3");
        $("#closeTime").val("2018-02-23T11:24");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addVersionManageBtn = function () {
        $("#versionName").attr("disabled", false);
        $("#submit").attr("onclick", "addVersionManage()");
        context.openDiv('versionManageAddSubPage', 'bgdiv', '添加版本');
    };

    context.getPageVersionManageData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var versionManageData = {};
        versionManageData["versionName"] = $("#versionName").val().trim();
        versionManageData["versionDesc"] = $("#versionDesc").val().trim();
        versionManageData["type"] = $("#type").val().trim();
        versionManageData["closeTime"] = $("#closeTime").val().trim();
        return versionManageData;
    };


    context.addVersionManage = function () {
        var versionManageData = context.getPageVersionManageData();
        if (!versionManageData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/versionManage/addVersionManage",
            type: "post",
            data: {"versionManageData": JSON.stringify(versionManageData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('versionManageAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editVersionManageBtn = function (versionManageId) {
        var request = $.ajax({url: "/myadmin/versionManage/getVersionManageForId", data: {"versionManageId": versionManageId}, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("version查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editVersionManage('" + versionManageId + "')");

        context.openDiv('versionManageAddSubPage', 'bgdiv', '编辑版本');
        $("#versionName").attr("disabled", true);
        $("#versionName").val(requestBody["versionName"]);
        $("#versionDesc").val(requestBody["versionDesc"]);
        $("#type").val(requestBody["type"]);
        $("#closeTime").val(requestBody["closeTime"]);
    };

    context.editVersionManage = function (versionManageId) {
        var versionManageData = context.getPageVersionManageData();
        if (!versionManageData) {
            return;
        }
        versionManageData["id"] = versionManageId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/versionManage/editVersionManage",
            type: "post",
            data: {"versionManageData": JSON.stringify(versionManageData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('versionManageAddSubPage', 'bgdiv');
             context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteVersionManageBtn = function (element, versionManageId) {
        if (!confirm("确认删除 [" + $("#versionName_" + versionManageId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/versionManage/deleteVersionManage",
            type: "post",
            data: {"versionManageId": versionManageId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetVersionManageBtn = function (element, versionManageId) {
        if (!confirm("确认启用 [" + $("#versionName_" + versionManageId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/versionManage/resetVersionManage",
            type: "post",
            data: {"versionManageId": versionManageId},
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
        checkArr.versionName = $("#queryVersionName").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "versionName") {
                key = "版本";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };


    
    context.delQuery = function (condition) {
        if (condition === "versionName") {
            $("#queryVersionName").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();


