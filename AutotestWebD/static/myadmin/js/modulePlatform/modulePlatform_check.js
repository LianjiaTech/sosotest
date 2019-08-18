"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/modulePlatform/getModulePlatform",async:false,type:"post",data:data});
        $("#modulePlatformSubPage").html(htmlobj.responseText);
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
            obbgdiv.height(docheight);
            $('html,body').animate({scrollTop:offtop}, 800);
            obshowdiv.find("input").attr("required","required");
        };

    context.CloseDiv = function (close_div,bg_div) {
        //清空弹出层文本框和下拉框
        $("#jiraModule").html("");
        $("#platform").html("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.getAllJiraModules = function () {
        var ajaxRequest = $.ajax({
            url: "/myadmin/modulePlatform/getAllJiraModules",
            type: "post",
            async: false
        });


        var requestJson = JSON.parse(ajaxRequest.responseText);
        if (requestJson["code"] === 10000){
            context.selected();
            return requestJson["body"];
        }else{
            alert("错误 " + request["code"] + ":" + request["message"]);
            return;
        }
    };

    context.getAllModuleNames = function () {
        var ajaxRequest = $.ajax({
            url: "/myadmin/businessLineModule/getAllModuleNames",
            type: "post",
            async: false
        });


        var requestJson = JSON.parse(ajaxRequest.responseText);
        if (requestJson["code"] === 10000){
            context.selected();
            return requestJson["body"];
        }else{
            alert("错误 " + request["code"] + ":" + request["message"]);
            return;
        }
    };

    context.addModulePlatformBtn = function () {
        var jiraModuleRequestBody = context.getAllJiraModules();
        var moduleNameRequestBody = context.getAllModuleNames();

         $('.select2').select2();

        for (var jiraModule in jiraModuleRequestBody){
            $("#jiraModule").append('<option value="'+jiraModuleRequestBody[jiraModule]+'"> '+jiraModuleRequestBody[jiraModule] +'</option>');
        }

        for (var moduleName in moduleNameRequestBody){
            $("#platform").append('<option value="'+ moduleNameRequestBody[moduleName]+'"> '+ moduleNameRequestBody[moduleName] +' </option>');
        }

        $("#submit").attr("onclick","addModulePlatform()");
        context.openDiv('adminAddModulePlatformSubPage','bgdiv','添加jira模块与平台模块关联关系');
    };


    context.getPageModulePlatformData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var modulePlatformData = {};
        modulePlatformData["jiraModule"] = $("#jiraModule").val().trim();
        modulePlatformData["platform"] = $("#platform").val().trim();

        return modulePlatformData;
    };


    context.addModulePlatform = function () {
        var modulePlatformData = context.getPageModulePlatformData();

        if(!modulePlatformData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/modulePlatform/addModulePlatform",type:"post",data:{"modulePlatformData":JSON.stringify(modulePlatformData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddModulePlatformSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editModulePlatformBtn = function (modulePlatformId) {
        var request = $.ajax({url:"/myadmin/modulePlatform/getModulePlatformForId",data:{"modulePlatformId":modulePlatformId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("数据查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editModulePlatform('"+modulePlatformId+"')");

         var jiraModuleRequestBody = context.getAllJiraModules();

        var moduleNamesRequestBody = context.getAllModuleNames();

        for (var jiraModuleIndex in jiraModuleRequestBody) {
                    $("#jiraModule").append('<option value="' + jiraModuleRequestBody[jiraModuleIndex] + '">' + jiraModuleRequestBody[jiraModuleIndex] + '</option>');
                }

        var htmlobj = $("#jiraModule").find("option");
        htmlobj.each(function () {
            if($(this).text() === requestBody["jiraModule"]){
                $(this).attr("selected",true);
            }
        });

        $('.select2').select2();



        for (var moduleNameIndex in moduleNamesRequestBody) {
            $("#platform").append('<option value="' + moduleNamesRequestBody[moduleNameIndex] + '">' + moduleNamesRequestBody[moduleNameIndex] + '</option>');
        }
        var htmlobjModuleName = $("#platform").find("option");
        htmlobjModuleName.each(function () {
            if($(this).text() === requestBody["platform"]){
                $(this).attr("selected",true);
            }
        });
        $('.select2').select2();


        context.openDiv('adminAddModulePlatformSubPage','bgdiv','编辑jira模块与平台模块关联关系');
    };

    context.editModulePlatform = function (modulePlatformId) {
        var modulePlatformData = context.getPageModulePlatformData();
        if(!modulePlatformData){
            return;
        }
        modulePlatformData["id"] = modulePlatformId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/modulePlatform/editModulePlatform",
            type: "post",
            data: {"modulePlatformData": JSON.stringify(modulePlatformData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddModulePlatformSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteModulePlatformBtn = function (element, modulePlatformId) {
        if (!confirm("确认删除 [" + $("#jiraModule_"+modulePlatformId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/modulePlatform/deleteModulePlatform",
            type: "post",
            data: {"modulePlatformId": modulePlatformId},
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

    context.getJiraModuleId = function () {
         var jiraModule = $("#queryJiraModule").val();
         if(jiraModule !=""){
                 var ajaxRequest = $.ajax({
                url: "/myadmin/modulePlatform/getJiraModuleId",
                type: "post",
                data: {"jiraModule": jiraModule},
                async: false
            });
            var request = JSON.parse(ajaxRequest.responseText);
            if (request["code"] === 10000) {
                context.selected();
                return request["body"][0];
            } else {
                alert("错误 " + request["code"] + ":" + request["message"]);
            }
         }else{
             return "";
         }

    };

    context.getModuleId = function () {
        var moduleName = $("#queryModule").val();
         var ajaxRequestModulName = $.ajax({
            url: "/myadmin/businessLineModule/getModuleId",
            type: "post",
            data: {"moduleName": moduleName},
            async: false
        });
        var requestModuleName = JSON.parse(ajaxRequestModulName.responseText);
        if (requestModuleName["code"] === 10000) {
            context.selected();
            return requestModuleName["body"][0];
        } else {
            alert("错误 " + requestModuleName["code"] + ":" + requestModuleName["message"]);
        }
    };


    context.queryRequest = function () {

        checkArr.jiraModuleId = context.getJiraModuleId();
        // checkArr.moduleId = context.getModuleId();


        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            }
            var key = "";
            if  (index === "jiraModuleId"){

                key = "jira模块";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + $("#queryJiraModule").val() + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "jiraModuleId"){
            $("#queryJiraModule").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();


$(function () {
    //Initialize Select2 Elements
    $('.select2').select2();

})