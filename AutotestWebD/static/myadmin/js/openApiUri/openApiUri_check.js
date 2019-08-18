"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/openApiUri/getOpenApiUriSubPage", async: false, type: "post", data: data});
        $("#openApiUriSubPage").html(htmlobj.responseText);
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
        $("#summaryUri").val("");
        $("#summaryUrl").val("");
        $("#interfaceTestUri").val("");
        $("#interfaceTestUrl").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addOpenApiUriBtn = function () {
        $("#submit").attr("onclick", "addOpenApiUri()");
        context.openDiv('openApiUriAddSubPage', 'bgdiv', '添加openApi_Uri');
    };

    context.getPageOpenApiUriData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var openApiUriData = {};
        openApiUriData["summaryUri"] = $("#summaryUri").val().trim();
        openApiUriData["summaryUrl"] = $("#summaryUrl").val().trim();
        openApiUriData["interfaceTestUri"] = $("#interfaceTestUri").val().trim();
        openApiUriData["interfaceTestUrl"] = $("#interfaceTestUrl").val().trim();
        return openApiUriData;
    }


    context.addOpenApiUri = function () {
        var openApiUriData = context.getPageOpenApiUriData();
        // alert(teamData);
        if (!openApiUriData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/openApiUri/addOpenApiUri",
            type: "post",
            data: {"openApiUriData": JSON.stringify(openApiUriData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('openApiUriAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editOpenApiUriBtn = function (openApiUriId) {
        var request = $.ajax({url: "/myadmin/openApiUri/getOpenApiUriForId", data: {"openApiUriId": openApiUriId}, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("openApi_Uri查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editOpenApiUri('" + openApiUriId + "')");

        context.openDiv('openApiUriAddSubPage', 'bgdiv', '编辑openApi_Uri');
        $("#summaryUri").val(requestBody["summaryUri"]);
        $("#summaryUrl").val(requestBody["summaryUrl"]);
        $("#interfaceTestUri").val(requestBody["interfaceTestUri"]);
        $("#interfaceTestUrl").val(requestBody["interfaceTestUrl"]);
    };

    context.editOpenApiUri = function (openApiUriId) {
        var openApiUriData = context.getPageOpenApiUriData();
        if (!openApiUriData) {
            return;
        }
        openApiUriData["id"] = openApiUriId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/openApiUri/editOpenApiUri",
            type: "post",
            data: {"openApiUriData": JSON.stringify(openApiUriData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('openApiUriAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteOpenApiUriBtn = function (element, openApiUriId) {
        if (!confirm("确认删除 [" + $("#summaryUri_" + openApiUriId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/openApiUri/deleteOpenApiUri",
            type: "post",
            data: {"openApiUriId": openApiUriId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetOpenApiUriBtn = function (element, openApiUriId) {
        if (!confirm("确认启用 [" + $("#summaryUri_" + openApiUriId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/openApiUri/resetOpenApiUri",
            type: "post",
            data: {"openApiUriId": openApiUriId},
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
        checkArr.summaryUri = $("#querySummaryUri").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "summaryUri") {
                key = "获取概况数据的URI";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };


    
    context.delQuery = function (condition) {
        if (condition === "summaryUri") {
            $("#querySummaryUri").val("");
        }

        context.queryRequest();
    };


})(window);
// window.doubleBoxFunction();
window.selected();


