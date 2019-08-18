"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc,u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/httpInterfaceDebug/getHttpInterfaceDebugSubPage",async:false,type:"post",data:data});
        $("#httpInterfaceDebugSubPage").html(htmlobj.responseText);
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
            // obbgdiv.height(docheight);
            obbgdiv.height(700);
            $('html,body').animate({scrollTop:offtop}, 800);
            obshowdiv.find("input").attr("required","required");
        };

    context.CloseDiv = function (close_div,bg_div) {
        //清空弹出层文本框和下拉框
        $("#interfaceId").val("");
        $("#title").val("");
        $("#casedesc").val("");
        $("#businessLineId").html("");
        $("#moduleId").html("");
        $("#sourceId").html("");
        $("#caselevel").val("");
        $("#status").val("2");
        $("#caseType").val("2");
        $("#varsPre").val("");
        $("#dataInit").val("");
        $("#uri").val("");
        $("#method").val("");
        $("#header").val("");
        $("#url").val("");
        $("#params").val("");
        $("#bodyType").val("0");
        $("#bodyContent").val("");
        $("#timeout").val("");
        $("#varsPost").val("");
        $("#expectResult").val("");
        $("#dataRecover").val("");
        $("#performanceTime").val("");
        $("#execStatus").val("");
        $("#httpConfKey").html("");
        $("#actualResult").val("");
        $("#assertResult").val("");
        $("#testResult").val("");
        $("#beforeExecuteTakeTime").val("");
        $("#afterExecuteTakeTime").val("");
        $("#executeTakeTime").val("");
        $("#totalTakeTime").val("");
        $("#CurrentVersion").val("");
        $("#addBy").attr("disabled", false);
        $("#addBy").html("");

        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.getAllBusinessLines = function () {
        var ajaxRequest = $.ajax({
            url:"/myadmin/httpInterfaceDebug/getAllBusinessLines",
            type:"post",
            async:false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.selected();
            return request["body"];
        }else{
            alert("错误" + request["code"] + ":" + request["message"]);
            return;
        }
    };

    context.getAllModuleNames = function () {
        var ajaxRequest = $.ajax({
            url:"/myadmin/httpInterfaceDebug/getAllModuleNames",
            type:"post",
            async:false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.selected();
            return request["body"];
        }else {
            alert("错误" + request["code"] + ":" + request["message"]);
            return;
        }
    };

    context.getAllSourceNames = function () {
        var ajaxRequest = $.ajax({
            url:"/myadmin/httpInterfaceDebug/getAllSourceNames",
            type:"post",
            async:false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.selected();
            return request["body"];
        }else {
            alert("错误" + request["code"] + ":" + request["message"]);
            return;
        }
    };

    context.getAllHttpConfKeys = function () {
        var ajaxRequest = $.ajax({
            url:"/myadmin/httpInterfaceDebug/getAllHttpConfKeys",
            type:"post",
            async:false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.selected();
            return request["body"];
        }else {
            alert("错误" + request["code"] + ":" + request["message"]);
            return;
        }
    };

    context.getAllUsers = function () {
        var ajaxRequest = $.ajax({
            url:"/myadmin/httpInterfaceDebug/getAllUsers",
            type:"post",
            async:false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.selected();
            return request["body"];
        }else {
            alert("错误" + request["code"] + ":" + request["message"]);
            return;
        }
    };

    context.addHttpInterfaceDebugBtn = function () {
        var businessLines = context.getAllBusinessLines();
        for (var businessLineIndex in businessLines){
            $("#businessLineId").append('<option value="' + businessLines[businessLineIndex] + '"> ' + businessLines[businessLineIndex] + '</option>');
        }

        var moduleNames = context.getAllModuleNames();
        for (var moduleNameIndex in moduleNames){
            $("#moduleId").append('<option value="' + moduleNames[moduleNameIndex] + '">' + moduleNames[moduleNameIndex] + '</option>');
        }

        var sourceNames = context.getAllSourceNames();
        for (var sourceNameIndex in sourceNames){
            $("#sourceId").append('<option value="' + sourceNames[sourceNameIndex] + '">' + sourceNames[sourceNameIndex] + '</option>');
        }

        var httpConfKeys = context.getAllHttpConfKeys();
        for (var httpConfKeyIndex in httpConfKeys){
            $("#httpConfKey").append('<option value="' + httpConfKeys[httpConfKeyIndex] + '">' + httpConfKeys[httpConfKeyIndex] + '</option>');
        }

        var userNames = context.getAllUsers();
        for (var userNameIndex in userNames){
            $("#addBy").append('<option value="' + userNames[userNameIndex] + '">' + userNames[userNameIndex] + '</option>');
        }

        $("#submit").attr("onclick","addHttpInterfaceDebug()");
        context.openDiv('adminAddHttpInterfaceDebugSubPage','bgdiv','添加接口调试数据');
    };

    context.getPageHttpInterfaceDebugData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var httpInterfaceDebugData = {};
        httpInterfaceDebugData["interfaceId"] = $("#interfaceId").val().trim();
        httpInterfaceDebugData["title"] = $("#title").val().trim();
        httpInterfaceDebugData["casedesc"] = $("#casedesc").val().trim();
        httpInterfaceDebugData["businessLineId"] = $("#businessLineId").val().trim();
        httpInterfaceDebugData["moduleId"] = $("#moduleId").val().trim();
        httpInterfaceDebugData["sourceId"] = $("#sourceId").val().trim();
        httpInterfaceDebugData["caselevel"] = $("#caselevel").val().trim();
        httpInterfaceDebugData["status"] = $("#status").val().trim();
        httpInterfaceDebugData["caseType"] = $("#caseType").val().trim();
        httpInterfaceDebugData["varsPre"] = $("#varsPre").val().trim();
        httpInterfaceDebugData["dataInit"] = $("#dataInit").val().trim();
        httpInterfaceDebugData["uri"] = $("#uri").val().trim();
        httpInterfaceDebugData["method"] = $("#method").val().trim();
        httpInterfaceDebugData["header"] = $("#header").val().trim();
        httpInterfaceDebugData["url"] = $("#url").val().trim();
        httpInterfaceDebugData["params"] = $("#params").val().trim();
        httpInterfaceDebugData["bodyType"] = $("#bodyType").val().trim();
        httpInterfaceDebugData["bodyContent"] = $("#bodyContent").val().trim();
        httpInterfaceDebugData["timeout"] = $("#timeout").val().trim();
        httpInterfaceDebugData["varsPost"] = $("#varsPost").val().trim();
        httpInterfaceDebugData["expectResult"] = $("#expectResult").val().trim();
        httpInterfaceDebugData["dataRecover"] = $("#dataRecover").val().trim();
        httpInterfaceDebugData["performanceTime"] = $("#performanceTime").val().trim();
        httpInterfaceDebugData["execStatus"] = $("#execStatus").val().trim();
        httpInterfaceDebugData["httpConfKey"] = $("#httpConfKey").val().trim();
        httpInterfaceDebugData["actualResult"] = $("#actualResult").val().trim();
        httpInterfaceDebugData["assertResult"] = $("#assertResult").val().trim();
        httpInterfaceDebugData["testResult"] = $("#testResult").val().trim();
        httpInterfaceDebugData["beforeExecuteTakeTime"] = $("#beforeExecuteTakeTime").val().trim();
        httpInterfaceDebugData["afterExecuteTakeTime"] = $("#afterExecuteTakeTime").val().trim();
        httpInterfaceDebugData["executeTakeTime"] = $("#executeTakeTime").val().trim();
        httpInterfaceDebugData["totalTakeTime"] = $("#totalTakeTime").val().trim();
        httpInterfaceDebugData["version"] = $("#version").val().trim();
        httpInterfaceDebugData["addBy"] = $("#addBy").val().trim();

        return httpInterfaceDebugData;
    };


    context.addHttpInterfaceDebug = function () {
        var httpInterfaceDebugData = context.getPageHttpInterfaceDebugData();

        if(!httpInterfaceDebugData){
            return;
        }
        var ajaxRequest = $.ajax({
            url:"/myadmin/httpInterfaceDebug/addHttpInterfaceDebug",
            type:"post",
            data:{"httpInterfaceDebugData":JSON.stringify(httpInterfaceDebugData)},
            async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddHttpInterfaceDebugSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editHttpInterfaceDebugBtn = function (httpInterfaceDebugId) {
        var request = $.ajax({url:"/myadmin/httpInterfaceDebug/getHttpInterfaceDebugForId",data:{"httpInterfaceDebugId":httpInterfaceDebugId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("接口调试数据查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editHttpInterfaceDebug('"+httpInterfaceDebugId+"')");

        var businessLines = context.getAllBusinessLines();
        $("#businessLineId").html("");
        for (var businessLineIndex in businessLines){
            if (businessLines[businessLineIndex] === requestBody["businessLineId"]){
                $("#businessLineId").append('<option value="' + businessLines[businessLineIndex]  + '" selected="selected">' + businessLines[businessLineIndex]  + '</option>');
            }
            else {
                $("#businessLineId").append('<option value="' + businessLines[businessLineIndex]  + '">' + businessLines[businessLineIndex]  + '</option>');

            }
        }

        $('.select2').select2();

        var moduleNames = context.getAllModuleNames();
        $("#moduleId").html("")
        for (var moduleNameIndex in moduleNames){
            if (moduleNames[moduleNameIndex] === requestBody["moduleId"]){
                $("#moduleId").append('<option value="' + moduleNames[moduleNameIndex] + '" selected="selected">' + moduleNames[moduleNameIndex] + '</option>');
            }
            else {
                $("#moduleId").append('<option value="' + moduleNames[moduleNameIndex]  + '">' + moduleNames[moduleNameIndex] + '</option>');

            }
        }

        $('.select2').select2();

        var sourceNames = context.getAllSourceNames();
        $("#sourceId").html("");
        for (var sourceNameIndex in sourceNames){
            if (sourceNames[sourceNameIndex] === requestBody["sourceId"]){
                $("#sourceId").append('<option value="' + sourceNames[sourceNameIndex] + '" selected="selected">' + sourceNames[sourceNameIndex] + '</option>');
            }
            else {
                $("#sourceId").append('<option value="' + sourceNames[sourceNameIndex] + '">' + sourceNames[sourceNameIndex] + '</option>');

            }
        }

        $('.select2').select2();


        var httpConfKeys = context.getAllHttpConfKeys();
        $("#httpConfKey").html("");
        for (var httpConfKeyIndex in httpConfKeys){
            if (httpConfKeys[httpConfKeyIndex] === requestBody["httpConfKey"]){
                $("#httpConfKey").append('<option value="' + httpConfKeys[httpConfKeyIndex] + '" selected="selected">' + httpConfKeys[httpConfKeyIndex] + '</option>');
            }
            else {
                $("#httpConfKey").append('<option value="' + httpConfKeys[httpConfKeyIndex] + '">' + httpConfKeys[httpConfKeyIndex] + '</option>');

            }
        }

        $('.select2').select2();
        var userNames = context.getAllUsers();
        $("#addBy").html("");
        for (var userNameIndex in userNames){
            if (userNames[userNameIndex] === requestBody["addBy"]){
                $("#addBy").append('<option value="' + userNames[userNameIndex] + '" selected="selected">' + userNames[userNameIndex] + '</option>');
            }
            else {
                $("#addBy").append('<option value="' + userNames[userNameIndex] + '">' + userNames[userNameIndex] + '</option>');

            }
        }
        $('.select2').select2();

        context.openDiv('adminAddHttpInterfaceDebugSubPage','bgdiv','编辑接口调试数据');
        $("#interfaceId").val(requestBody["interfaceId"]);
        $("#title").val(requestBody["title"]);
        $("#casedesc").val(requestBody["casedesc"]);
        $("#caselevel").val(requestBody["caselevel"]);
        $("#status").val(requestBody["status"]);
        $("#caseType").val(requestBody["caseType"]);
        $("#varsPre").val(requestBody["varsPre"]);
        $("#dataInit").val(requestBody["dataInit"]);
        $("#uri").val(requestBody["uri"]);
        $("#method").val(requestBody["method"]);
        $("#header").val(requestBody["header"]);
        $("#url").val(requestBody["url"]);
        $("#params").val(requestBody["params"]);
        $("#bodyType").val(requestBody["bodyType"]);
        $("#bodyContent").val(requestBody["bodyContent"]);
        $("#timeout").val(requestBody["timeout"]);
        $("#varsPost").val(requestBody["varsPost"]);
        $("#expectResult").val(requestBody["expectResult"]);
        $("#dataRecover").val(requestBody["dataRecover"]);
        $("#performanceTime").val(requestBody["performanceTime"]);
        $("#execStatus").val(requestBody["execStatus"]);
        $("#actualResult").val(requestBody["actualResult"]);
        $("#assertResult").val(requestBody["assertResult"]);
        $("#testResult").val(requestBody["testResult"]);
        $("#beforeExecuteTakeTime").val(requestBody["beforeExecuteTakeTime"]);
        $("#afterExecuteTakeTime").val(requestBody["afterExecuteTakeTime"]);
        $("#executeTakeTime").val(requestBody["executeTakeTime"]);
        $("#totalTakeTime").val(requestBody["totalTakeTime"]);
        $("#version").val(requestBody["version"]);
        $("#addBy").attr("disabled", true);
    };

    context.editHttpInterfaceDebug = function (httpInterfaceDebugId) {
        var httpInterfaceDebugData = context.getPageHttpInterfaceDebugData();
        if(!httpInterfaceDebugData){
            return;
        }
        httpInterfaceDebugData["id"] = httpInterfaceDebugId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/httpInterfaceDebug/editHttpInterfaceDebug",
            type: "post",
            data: {"httpInterfaceDebugData": JSON.stringify(httpInterfaceDebugData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddHttpInterfaceDebugSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteHttpInterfaceDebugBtn = function (element, httpInterfaceDebugId) {
        if (!confirm("确认删除 [" + $("#interfaceId_"+httpInterfaceDebugId ).text() + "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/httpInterfaceDebug/delHttpInterfaceDebug",
            type: "post",
            data: {"httpInterfaceDebugId": httpInterfaceDebugId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetHttpInterfaceDebugBtn = function (element, httpInterfaceDebugId) {
        if (!confirm("确认启用 [" + $("#interfaceId_"+httpInterfaceDebugId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/httpInterfaceDebug/resetHttpInterfaceDebug",
            type: "post",
            data: {"httpInterfaceDebugId": httpInterfaceDebugId},
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
        checkArr.interfaceId = $("#queryInterfaceId").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            };
            var key = "";
            if  (index === "interfaceId"){
                key = "接口ID";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
            
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "interfaceId"){
            $("#queryInterfaceId").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();



$(function () {
    //Initialize Select2 Elements
    $('.select2').select2();

})