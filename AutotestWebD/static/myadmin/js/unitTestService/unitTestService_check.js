"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/unitTestService/getUnitTestServiceSubPage", async: false, type: "post", data: data});
        $("#unitTestServiceSubPage").html(htmlobj.responseText);
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
        $("#serviceName").val("");
        $("#serviceDesc").val("");
        $("#isShow").val("1");
        $("#level").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addUnitTestServiceBtn = function () {
        $("#submit").attr("onclick", "addUnitTestService()");
        context.openDiv('unitTestServiceAddSubPage', 'bgdiv', '添加unitTestService');
    };

    context.getPageUnitTestServiceData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var unitTestServiceData = {};
        unitTestServiceData["serviceName"] = $("#serviceName").val().trim();
        unitTestServiceData["serviceDesc"] = $("#serviceDesc").val().trim();
        unitTestServiceData["isShow"] = $("#isShow").val().trim();
        unitTestServiceData["level"] = $("#level").val().trim();
        return unitTestServiceData;
    };


    context.addUnitTestService = function () {
        var unitTestServiceData = context.getPageUnitTestServiceData();
        if (!unitTestServiceData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/unitTestService/addUnitTestService",
            type: "post",
            data: {"unitTestServiceData": JSON.stringify(unitTestServiceData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('unitTestServiceAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editUnitTestServiceBtn = function (unitTestServiceId) {
        var request = $.ajax({url: "/myadmin/unitTestService/getUnitTestServiceForId", data: {"unitTestServiceId": unitTestServiceId}, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("unitTestService查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editUnitTestService('" + unitTestServiceId + "')");

        context.openDiv('unitTestServiceAddSubPage', 'bgdiv', '编辑unitTestService');
        $("#serviceName").val(requestBody["serviceName"]);
        $("#serviceDesc").val(requestBody["serviceDesc"]);
        $("#isShow").val(requestBody["isShow"]);
        $("#level").val(requestBody["level"]);
    };

    context.editUnitTestService = function (unitTestServiceId) {
        var unitTestServiceData = context.getPageUnitTestServiceData();
        // delete teamData["teamKey"]
        if (!unitTestServiceData) {
            return;
        }
        unitTestServiceData["id"] = unitTestServiceId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/unitTestService/editUnitTestService",
            type: "post",
            data: {"unitTestServiceData": JSON.stringify(unitTestServiceData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('unitTestServiceAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteUnitTestServiceBtn = function (element, unitTestServiceId) {
        if (!confirm("确认删除 [" + $("#serviceName_" + unitTestServiceId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/unitTestService/deleteUnitTestService",
            type: "post",
            data: {"unitTestServiceId": unitTestServiceId},
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

    context.resetUnitTestServiceBtn = function (element, unitTestServiceId) {
        if (!confirm("确认启用 [" + $("#serviceName_" + unitTestServiceId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/unitTestService/resetUnitTestService",
            type: "post",
            data: {"unitTestServiceId": unitTestServiceId},
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
        checkArr.serviceName = $("#queryServiceName").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "serviceName") {
                key = "版本";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };


    
    context.delQuery = function (condition) {
        if (condition === "serviceName") {
            $("#queryServiceName").val("");
        }

        context.queryRequest();
    };


})(window);
// window.doubleBoxFunction();
window.selected();


