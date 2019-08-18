"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/jiraBusinessLine/getJiraBusinessLineSubPage", async: false, type: "post", data: data});
        $("#jiraBusinessLineSubPage").html(htmlobj.responseText);
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

    context.ReloadPage = function(){
        location.reload();
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

    context.addJiraBusinessLineBtn = function () {
        $("#businessLineName").attr("disabled", false);
        $("#submit").attr("onclick", "addJiraBusinessLine()");
        context.openDiv('jiraBusinessLineAddSubPage', 'bgdiv', '添加jira业务线');
    };

    context.getPageJiraBusinessLineData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var jiraBusinessLineData = {};
        jiraBusinessLineData["businessLineName"] = $("#businessLineName").val().trim();
        jiraBusinessLineData["businessLineDesc"] = $("#businessLineDesc").val().trim();
        return jiraBusinessLineData;
    };


    context.addJiraBusinessLine = function () {
        var jiraBusinessLineData = context.getPageJiraBusinessLineData();
        if (!jiraBusinessLineData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/jiraBusinessLine/addJiraBusinessLine",
            type: "post",
            data: {"jiraBusinessLineData": JSON.stringify(jiraBusinessLineData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('jiraBusinessLineAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editJiraBusinessLineBtn = function (jiraBusinessLineId) {
        var request = $.ajax({url: "/myadmin/jiraBusinessLine/getJiraBusinessLineForId", data: {"jiraBusinessLineId": jiraBusinessLineId}, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("jira业务线查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editJiraBusinessLine('" + jiraBusinessLineId + "')");

        context.openDiv('jiraBusinessLineAddSubPage', 'bgdiv', '编辑jiraBusinessLine');
        $("#businessLineName").attr("disabled", true);
        $("#businessLineName").val(requestBody["businessLineName"]);
        $("#businessLineDesc").val(requestBody["businessLineDesc"]);
    };

    context.editJiraBusinessLine = function (jiraBusinessLineId) {
        var jiraBusinessLineData = context.getPageJiraBusinessLineData();
        if (!jiraBusinessLineData) {
            return;
        }
        jiraBusinessLineData["id"] = jiraBusinessLineId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/jiraBusinessLine/editJiraBusinessLine",
            type: "post",
            data: {"jiraBusinessLineData": JSON.stringify(jiraBusinessLineData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('jiraBusinessLineAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteJiraBusinessLineBtn = function (element, jiraBusinessLineId) {
        if (!confirm("确认删除 [" + $("#businessLineName_" + jiraBusinessLineId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/jiraBusinessLine/delJiraBusinessLine",
            type: "post",
            data: {"jiraBusinessLineId": jiraBusinessLineId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetJiraBusinessLineBtn = function (element, jiraBusinessLineId) {
        if (!confirm("确认启用 [" + $("#businessLineName_" + jiraBusinessLineId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/jiraBusinessLine/resetJiraBusinessLine",
            type: "post",
            data: {"jiraBusinessLineId": jiraBusinessLineId},
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
                key = "jira业务线名称";
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




 $(function () {
         //Initialize Select2 Elements
     $('.select2').select2();

 })

