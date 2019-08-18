"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/openApiBusinessLine/getOpenApiBusinessLineSubPage", async: false, type: "post", data: data});
        $("#openApiBusinessLineSubPage").html(htmlobj.responseText);
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
        $("#businessLineName").val("");
        $("#businessLineDesc").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addOpenApiBusinessLineBtn = function () {
        $("#submit").attr("onclick", "addOpenApiBusinessLine()");
        context.openDiv('openApiBusinessLineAddSubPage', 'bgdiv', '添加openApi业务线');
    };

    context.getPageOpenApiBusinessLineData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var openApiBusinessLineData = {};
        openApiBusinessLineData["businessLineName"] = $("#businessLineName").val().trim();
        openApiBusinessLineData["businessLineDesc"] = $("#businessLineDesc").val().trim();
        return openApiBusinessLineData;
    }


    context.addOpenApiBusinessLine = function () {
        var openApiBusinessLineData = context.getPageOpenApiBusinessLineData();
        // alert(teamData);
        if (!openApiBusinessLineData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/openApiBusinessLine/addOpenApiBusinessLine",
            type: "post",
            data: {"openApiBusinessLineData": JSON.stringify(openApiBusinessLineData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('openApiBusinessLineAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editOpenApiBusinessLineBtn = function (openApiBusinessLineId) {
        var request = $.ajax({url: "/myadmin/openApiBusinessLine/getOpenApiBusinessLineForId", data: {"openApiBusinessLineId": openApiBusinessLineId}, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("openApi业务线查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editOpenApiBusinessLine('" + openApiBusinessLineId + "')");

        context.openDiv('openApiBusinessLineAddSubPage', 'bgdiv', '编辑openApi业务线');
        $("#businessLineName").val(requestBody["businessLineName"]);
        $("#businessLineDesc").val(requestBody["businessLineDesc"]);
    };

    context.editOpenApiBusinessLine = function (openApiBusinessLineId) {
        var openApiBusinessLineData = context.getPageOpenApiBusinessLineData();
        // delete teamData["teamKey"]
        if (!openApiBusinessLineData) {
            return;
        }
        openApiBusinessLineData["id"] = openApiBusinessLineId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/openApiBusinessLine/editOpenApiBusinessLine",
            type: "post",
            data: {"openApiBusinessLineData": JSON.stringify(openApiBusinessLineData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('openApiBusinessLineAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteOpenApiBusinessLineBtn = function (element, openApiBusinessLineId) {
        if (!confirm("确认删除 [" + $("#businessLineName_" + openApiBusinessLineId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/openApiBusinessLine/delOpenApiBusinessLine",
            type: "post",
            data: {"openApiBusinessLineId": openApiBusinessLineId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetOpenApiBusinessLineBtn = function (element, openApiBusinessLineId) {
        if (!confirm("确认启用 [" + $("#businessLineName_" + openApiBusinessLineId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/openApiBusinessLine/resetOpenApiBusinessLine",
            type: "post",
            data: {"openApiBusinessLineId": openApiBusinessLineId},
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
        checkArr.businessLineName = $("#queryBusinessLineName").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "businessLineName") {
                key = "版本";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };


    
    context.delQuery = function (condition) {
        if (condition === "businessLineName") {
            $("#queryBusinessLineName").val("");
        }

        context.queryRequest();
    };


})(window);
// window.doubleBoxFunction();
window.selected();


