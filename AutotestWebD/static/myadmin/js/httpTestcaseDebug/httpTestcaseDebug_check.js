"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc,u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/httpTestcaseDebug/getHttpTestcaseDebugSubPage",async:false,type:"post",data:data});
        $("#httpTestcaseDebugSubPage").html(htmlobj.responseText);
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
        $("#addBy").attr("disabled", false);
        $("#addBy").html("");
        $("#caseId").val("");
        $("#title").val("");
        $("#casedesc").val("");
        $("#businessLineId").val("");
        $("#moduleId").val("");
        $("#sourceId").val("");
        $("#caselevel").val("");
        $("#status").val("2");
        $("#caseType").val("2");
        $("#businessLineId").html("");
        $("#execStatus").val("1");
        $("#httpConfKey").val("");
        $("#assertResult").val("");
        $("#testResult").val("");
        $("#moduleId").html("");
        $("#beforeExecuteTakeTime").val("");
        $("#afterExecuteTakeTime").val("");
        $("#executeTakeTime").val("");
        $("#totalTakeTime").val("");
        $("#version").val("0");
        $("#sourceId").html("");
        $("#httpConfKey").html("");


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

    context.addHttpTestcaseDebugBtn = function () {
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

        $("#submit").attr("onclick","addHttpTestcaseDebug()");
        context.openDiv('adminAddHttpTestcaseDebugSubPage','bgdiv','添加接口用例调试数据');
    };

    context.getPageHttpTestcaseDebugData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var httpTestcaseDebugData = {};
        httpTestcaseDebugData["caseId"] = $("#caseId").val().trim();
        httpTestcaseDebugData["title"] = $("#title").val().trim();
        httpTestcaseDebugData["casedesc"] = $("#casedesc").val().trim();
        httpTestcaseDebugData["businessLineId"] = $("#businessLineId").val().trim();
        httpTestcaseDebugData["moduleId"] = $("#moduleId").val().trim();
        httpTestcaseDebugData["sourceId"] = $("#sourceId").val().trim();
        httpTestcaseDebugData["caselevel"] = $("#caselevel").val().trim();
        httpTestcaseDebugData["stepCount"] = $("#stepCount").val().trim();
        httpTestcaseDebugData["status"] = $("#status").val().trim();
        httpTestcaseDebugData["caseType"] = $("#caseType").val().trim();
        httpTestcaseDebugData["execStatus"] = $("#execStatus").val().trim();
        httpTestcaseDebugData["httpConfKey"] = $("#httpConfKey").val().trim();
        httpTestcaseDebugData["assertResult"] = $("#assertResult").val().trim();
        httpTestcaseDebugData["testResult"] = $("#testResult").val().trim();
        httpTestcaseDebugData["beforeExecuteTakeTime"] = $("#beforeExecuteTakeTime").val().trim();
        httpTestcaseDebugData["afterExecuteTakeTime"] = $("#afterExecuteTakeTime").val().trim();
        httpTestcaseDebugData["executeTakeTime"] = $("#executeTakeTime").val().trim();
        httpTestcaseDebugData["totalTakeTime"] = $("#totalTakeTime").val().trim();
        httpTestcaseDebugData["version"] = $("#version").val().trim();
        httpTestcaseDebugData["addBy"] = $("#addBy").val().trim();

        return httpTestcaseDebugData;
    };


    context.addHttpTestcaseDebug = function () {
        var httpTestcaseDebugData = context.getPageHttpTestcaseDebugData();

        if(!httpTestcaseDebugData){
            return;
        }
        var ajaxRequest = $.ajax({
            url:"/myadmin/httpTestcaseDebug/addHttpTestcaseDebug",
            type:"post",
            data:{"httpTestcaseDebugData":JSON.stringify(httpTestcaseDebugData)},
            async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddHttpTestcaseDebugSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

   context.editHttpTestcaseDebugBtn = function (httpTestcaseDebugId) {
        var request = $.ajax({url:"/myadmin/httpTestcaseDebug/getHttpTestcaseDebugForId",data:{"httpTestcaseDebugId":httpTestcaseDebugId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("接口用例调试数据查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editHttpTestcaseDebug('"+httpTestcaseDebugId+"')");

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
        $("#moduleId").html("");
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

        context.openDiv('adminAddHttpTestcaseDebugSubPage','bgdiv','编辑接口用例调试数据');
        $("#caseId").val(requestBody["caseId"]);
        $("#title").val(requestBody["title"]);
        $("#casedesc").val(requestBody["casedesc"]);
        $("#caselevel").val(requestBody["caselevel"]);
        $("#stepCount").val(requestBody["stepCount"]);
        $("#status").val(requestBody["status"]);
        $("#caseType").val(requestBody["caseType"]);
        $("#execStatus").val(requestBody["execStatus"]);
        $("#assertResult").val(requestBody["assertResult"]);
        $("#testResult").val(requestBody["testResult"]);
        $("#beforeExecuteTakeTime").val(requestBody["beforeExecuteTakeTime"]);
        $("#afterExecuteTakeTime").val(requestBody["afterExecuteTakeTime"]);
        $("#executeTakeTime").val(requestBody["executeTakeTime"]);
        $("#totalTakeTime").val(requestBody["totalTakeTime"]);
        $("#version").val(requestBody["version"]);
        $("#addBy").attr("disabled", true);
    };

    context.editHttpTestcaseDebug = function (httpTestcaseDebugId) {
        var httpTestcaseDebugData = context.getPageHttpTestcaseDebugData();
        if(!httpTestcaseDebugData){
            return;
        }
        httpTestcaseDebugData["id"] = httpTestcaseDebugId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/httpTestcaseDebug/editHttpTestcaseDebug",
            type: "post",
            data: {"httpTestcaseDebugData": JSON.stringify(httpTestcaseDebugData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddHttpTestcaseDebugSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteHttpTestcaseDebugBtn = function (element, httpTestcaseDebugId) {
        if (!confirm("确认删除 [" + $("#caseId_"+httpTestcaseDebugId ).text() + "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/httpTestcaseDebug/delHttpTestcaseDebug",
            type: "post",
            data: {"httpTestcaseDebugId": httpTestcaseDebugId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetHttpTestcaseDebugBtn = function (element, httpTestcaseDebugId) {
        if (!confirm("确认启用 [" + $("#caseId_"+httpTestcaseDebugId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/httpTestcaseDebug/resetHttpTestcaseDebug",
            type: "post",
            data: {"httpTestcaseDebugId": httpTestcaseDebugId},
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
        checkArr.caseId = $("#queryCaseId").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            };
            var key = "";
            if  (index === "caseId"){
                key = "用例ID";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
            
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "caseId"){
            $("#queryCaseId").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();



$(function () {
    //Initialize Select2 Elements
    $('.select2').select2();

})