"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/standardTask/getStandardTaskSubPage", async: false, type: "post", data: data});
        $("#standardTaskSubPage").html(htmlobj.responseText);
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
        $("#version").val("");
        $("#businessLine").val("");
        $("#team").val("");
        $("#head").val("");
        $("#taskId").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.CloseDivCopTask = function (close_div, bg_div) {
        //清空弹出层文本框和下拉框
        $("#nowVersion").html("");
        $("#goalVersion").html("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addStandardTaskBtn = function () {
        $("#submit").attr("onclick", "addStandardTask()");
        context.openDiv('standardTaskAddSubPage', 'bgdiv', '添加标准任务版本');
    };

    context.getAllVerions = function () {
        var allVersionsRequest = $.ajax({url:"/myadmin/standardTask/getAllVersions", async:false, type:"post"});
        var requestJSON = JSON.parse(allVersionsRequest.responseText);
        if (requestJSON["code"] != 10000){
            alert("标准版本查询错误，请联系管理员");
            return;
        }
        return requestJSON["body"];
    };

    context.copyTaskToOtherVersionBtn = function () {

        var allVersionsRequestBody = context.getAllVerions();
        for (var versionIndex in allVersionsRequestBody) {
            $("#goalVersion").append('<option value="' + allVersionsRequestBody[versionIndex] + '">' + allVersionsRequestBody[versionIndex] + '</option>');
        }

        for (var index in allVersionsRequestBody) {
            $("#nowVersion").append('<option value="' + allVersionsRequestBody[index] + '">' + allVersionsRequestBody[index] + '</option>');
        }

        $("#copyTask").attr("onclick", "copyTaskToOtherVersion()");

        context.openDiv('copyTaskToOtherVersionSubPage', 'bgdiv', '复制任务到其他版本');

    };
    
    context.getCopyStandardTaskData = function () {

        var standardTaskData = {};
        standardTaskData["nowVersion"] = $("#nowVersion").val().trim();
        standardTaskData["goalVersion"] = $("#goalVersion").val().trim();
        return standardTaskData;
    };
        
    context.copyTaskToOtherVersion = function () {
        var standardTaskData = context.getCopyStandardTaskData();
        if (!standardTaskData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/standardTask/copyTaskToOtherVersion",
            type: "post",
            data: {"standardTaskData": JSON.stringify(standardTaskData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDivCopTask('copyTaskToOtherVersionSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };



    context.getPageStandardTaskData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var standardTaskData = {};
        standardTaskData["version"] = $("#version").val().trim();
        standardTaskData["businessLine"] = $("#businessLine").val().trim();
        standardTaskData["team"] = $("#team").val().trim();
        standardTaskData["head"] = $("#head").val().trim();
        standardTaskData["taskId"] = $("#taskId").val().trim();
        return standardTaskData;
    };


    context.addStandardTask = function () {
        var standardTaskData = context.getPageStandardTaskData();
        // alert(teamData);
        if (!standardTaskData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/standardTask/addStandardTask",
            type: "post",
            data: {"standardTaskData": JSON.stringify(standardTaskData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('standardTaskAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editStandardTaskBtn = function (standardTaskId) {
        var request = $.ajax({url: "/myadmin/standardTask/getStandardTaskForId", data: {"standardTaskId": standardTaskId}, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("标准任务版本查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editStandardTask('" + standardTaskId + "')");

        context.openDiv('standardTaskAddSubPage', 'bgdiv', '编辑标准任务版本');
        $("#version").val(requestBody["version"]);
        $("#businessLine").val(requestBody["businessLine"]);
        $("#team").val(requestBody["team"]);
        $("#head").val(requestBody["head"]);
        $("#taskId").val(requestBody["taskId"]);
    };

    context.editStandardTask = function (standardTaskId) {
        var standardTaskData = context.getPageStandardTaskData();
        // delete teamData["teamKey"]
        if (!standardTaskData) {
            return;
        }
        standardTaskData["id"] = standardTaskId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/standardTask/editStandardTask",
            type: "post",
            data: {"standardTaskData": JSON.stringify(standardTaskData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('standardTaskAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteStandardTaskBtn = function (element, standardTaskId) {
        if (!confirm("确认删除 [" + $("#version_" + standardTaskId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/standardTask/delStandardTask",
            type: "post",
            data: {"standardTaskId": standardTaskId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetStandardTaskBtn = function (element, standardTaskId) {
        if (!confirm("确认启用 [" + $("#version_" + standardTaskId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/standardTask/resetStandardTask",
            type: "post",
            data: {"standardTaskId": standardTaskId},
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
        checkArr.version = $("#queryVersion").val();
        checkArr.businessLine = $("#queryBusinessLine").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "version") {
                key = "版本";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
            if (index === "businessLine") {
                key = "业务线";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }


        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };


    
    context.delQuery = function (condition) {
        if (condition === "businessLine") {
            $("#queryBusinessLine").val("");
        }

        if (condition === "version") {
            $("#queryVersion").val("");
        }
        context.queryRequest();
    };


})(window);
// window.doubleBoxFunction();
window.selected();
$(function () {
    //Initialize Select2 Elements
    $('.select2').select2();

});

