"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc,u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/task/getTaskSubPage",async:false,type:"post",data:data});
        $("#taskSubPage").html(htmlobj.responseText);
    };

    context.pageCall = function (pageNum) {
        page = pageNum;
        context.selected();
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
        $("#taskId").attr("disabled", true);
        $("#taskId").val("");
        $("#title").val("");
        $("#taskdesc").val("");
        $("#protocol").val("");
        $("#businessLineGroup").val("");
        $("#modulesGroup").val("");
        $("#sourceGroup").val("['电脑Web']");
        $("#emailList").val("");
        $("#taskLevel").val("5");
        $("#highPriorityVARS").val("");
        $("#status").val("2");
        $("#interfaceCount").val("");
        $("#taskInterfaces").val("");
        $("#caseCount").val("");
        $("#taskTestcases").val("");
        $("#interfaceNum").val("");
        $("#isCI").val("1");

        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.getAllUsers = function () {
        var ajaxRequest = $.ajax({
            url:"/myadmin/task/getAllUsers",
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

    context.addTaskBtn = function () {
        var userNames = context.getAllUsers();
        for (var userNameIndex in userNames){
            $("#addBy").append('<option value="' + userNames[userNameIndex] + '">' + userNames[userNameIndex] + '</option>');
        }

         $("#submit").attr("onclick","addTask()");
        context.openDiv('adminAddTaskSubPage','bgdiv','添加任务');
    };

    context.getPageTaskData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var taskData = {};
        taskData["taskId"] = $("#taskId").val().trim();
        taskData["title"] = $("#title").val().trim();
        taskData["taskdesc"] = $("#taskdesc").val().trim();
        taskData["protocol"] = $("#protocol").val().trim();
        taskData["businessLineGroup"] = $("#businessLineGroup").val().trim();
        taskData["modulesGroup"] = $("#modulesGroup").val().trim();
        taskData["sourceGroup"] = $("#sourceGroup").val().trim();
        taskData["emailList"] = $("#emailList").val().trim();
        taskData["taskLevel"] = $("#taskLevel").val().trim();
        taskData["highPriorityVARS"] = $("#highPriorityVARS").val().trim();
        taskData["status"] = $("#status").val().trim();
        taskData["interfaceCount"] = $("#interfaceCount").val().trim();
        taskData["taskInterfaces"] = $("#taskInterfaces").val().trim();
        taskData["caseCount"] = $("#caseCount").val().trim();
        taskData["taskTestcases"] = $("#taskTestcases").val().trim();
        taskData["interfaceNum"] = $("#interfaceNum").val().trim();
        taskData["isCI"] = $("#isCI").val().trim();
        taskData["addBy"] = $("#addBy").val().trim();

        return taskData;
    };


    context.addTask = function () {
        var taskData = context.getPageTaskData();

        if(!taskData){
            return;
        }
        var ajaxRequest = $.ajax({
            url:"/myadmin/task/addTask",
            type:"post",
            data:{"taskData":JSON.stringify(taskData)},
            async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddTaskSubPage','bgdiv');
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editTaskBtn = function (taskId) {
        var request = $.ajax({url:"/myadmin/task/taskId",data:{"taskId":taskId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("任务查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editTask('"+taskId+"')");

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

        context.openDiv('adminAddTaskSubPage','bgdiv','编辑任务');
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