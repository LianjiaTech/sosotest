"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/jiraBusinessLinePlatform/getJiraBusinessLinePlatform",async:false,type:"post",data:data});
        $("#jiraBusinessLinePlatformSubPage").html(htmlobj.responseText);
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
        $("#jiraBusinessLine").html("");
        $("#platformBusinessLine").html("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.getAllJiraBusinessLines = function () {
        var ajaxRequest = $.ajax({
            url: "/myadmin/jiraBusinessLinePlatform/getAllJiraBusinessLines",
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

    context.getAllPlatformBusinessLines = function () {
        var ajaxRequest = $.ajax({
            url: "/myadmin/jiraBusinessLinePlatform/getAllPlatformBusinessLines",
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

    context.addJiraBusinessLinePlatformBtn = function () {
        var jiraBusinessLineRequestBody = context.getAllJiraBusinessLines();
        var platformBusinessLineRequestBody = context.getAllPlatformBusinessLines();

         $('.select2').select2();

        for (var jiraBusinessLine in jiraBusinessLineRequestBody){
            $("#jiraBusinessLine").append('<option value="'+jiraBusinessLineRequestBody[jiraBusinessLine]+'"> '+jiraBusinessLineRequestBody[jiraBusinessLine] +'</option>');
        }

        for (var platformBusinessLine in platformBusinessLineRequestBody){
            $("#platformBusinessLine").append('<option value="'+ platformBusinessLineRequestBody[platformBusinessLine]+'"> '+ platformBusinessLineRequestBody[platformBusinessLine] +' </option>');
        }

        $("#submit").attr("onclick","addJiraBusinessLinePlatform()");
        context.openDiv('adminAddJiraBusinessLinePlatformSubPage','bgdiv','添加jira业务线与平台关联关系');
    };


    context.getPageJiraBusinessLinePlatformData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var jiraBusinessLinePlatformData = {};
        jiraBusinessLinePlatformData["jiraBusinessLine"] = $("#jiraBusinessLine").val().trim();
        jiraBusinessLinePlatformData["platformBusinessLine"] = $("#platformBusinessLine").val().trim();

        return jiraBusinessLinePlatformData;
    };


    context.addJiraBusinessLinePlatform = function () {
        var jiraBusinessLinePlatformData = context.getPageJiraBusinessLinePlatformData();

        if(!jiraBusinessLinePlatformData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/jiraBusinessLinePlatform/addJiraBusinessLinePlatform",type:"post",data:{"jiraBusinessLinePlatformData":JSON.stringify(jiraBusinessLinePlatformData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddJiraBusinessLinePlatformSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editJiraBusinessLinePlatformBtn = function (jiraBusinessLinePlatformId) {
        var request = $.ajax({url:"/myadmin/jiraBusinessLinePlatform/getJiraBusinessLinePlatformForId",data:{"jiraBusinessLinePlatformId":jiraBusinessLinePlatformId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("数据查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editJiraBusinessLinePlatform('"+jiraBusinessLinePlatformId+"')");

         var platformBusinessLineRequestBody = context.getAllPlatformBusinessLines();

        var jiraBusinessLineRequestBody = context.getAllJiraBusinessLines();

        for (var jiraBusinessLineIndex in jiraBusinessLineRequestBody) {
                    $("#jiraBusinessLine").append('<option value="' + jiraBusinessLineRequestBody[jiraBusinessLineIndex] + '">' + jiraBusinessLineRequestBody[jiraBusinessLineIndex] + '</option>');
                }

        var htmlobj = $("#jiraBusinessLine").find("option");
        htmlobj.each(function () {
            if($(this).text() === requestBody["jiraBusinessLine"]){
                $(this).attr("selected",true);
            }
        });

        $('.select2').select2();



        for (var platformBusinessLineIndex in platformBusinessLineRequestBody) {
            $("#platformBusinessLine").append('<option value="' + platformBusinessLineRequestBody[platformBusinessLineIndex] + '">' + platformBusinessLineRequestBody[platformBusinessLineIndex] + '</option>');
        }
        var htmlobjPlatformBusinessLine = $("#platformBusinessLine").find("option");
        htmlobjPlatformBusinessLine.each(function () {
            if($(this).text() === requestBody["platformBusinessLine"]){
                $(this).attr("selected",true);
            }
        });
        $('.select2').select2();


        context.openDiv('adminAddJiraBusinessLinePlatformSubPage','bgdiv','编辑jira业务线与平台关联关系');
    };

    context.editJiraBusinessLinePlatform = function (jiraBusinessLinePlatformId) {
        var jiraBusinessLinePlatformData = context.getPageJiraBusinessLinePlatformData();
        if(!jiraBusinessLinePlatformData){
            return;
        }
        jiraBusinessLinePlatformData["id"] = jiraBusinessLinePlatformId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/jiraBusinessLinePlatform/editJiraBusinessLinePlatform",
            type: "post",
            data: {"jiraBusinessLinePlatformData": JSON.stringify(jiraBusinessLinePlatformData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddJiraBusinessLinePlatformSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteJiraBusinessLinePlatformBtn = function (element, jiraBusinessLinePlatformId) {
        if (!confirm("确认删除 [" + $("#jiraBusinessLine_"+jiraBusinessLinePlatformId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/jiraBusinessLinePlatform/deleteJiraBusinessLinePlatform",
            type: "post",
            data: {"jiraBusinessLinePlatformId": jiraBusinessLinePlatformId},
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

    context.getJiraBusinessLineId = function () {
         var jiraBusinessLine = $("#queryJiraBusinessLine").val();
         if(jiraBusinessLine !=""){
                 var ajaxRequest = $.ajax({
                url: "/myadmin/jiraBusinessLinePlatform/getJiraBusinessLineId",
                type: "post",
                data: {"jiraBusinessLine": jiraBusinessLine},
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



    context.queryRequest = function () {

        checkArr.jiraBusinessLineId = context.getJiraBusinessLineId();


        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            }
            var key = "";
            if  (index === "jiraBusinessLineId"){

                key = "jira业务线";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + $("#queryJiraBusinessLine").val() + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "jiraBusinessLineId"){
            $("#queryJiraBusinessLine").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();


$(function () {
    //Initialize Select2 Elements
    $('.select2').select2();

})