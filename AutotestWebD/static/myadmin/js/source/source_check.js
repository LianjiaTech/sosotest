"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/source/getSourceSubPage",async:false,type:"post",data:data});
        $("#sourceSubPage").html(htmlobj.responseText);
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
        $("#sourceName").val("");
        $("#sourceDesc").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.addSourceBtn = function () {
        $("#sourceName").attr("disabled", false);
        $("#submit").attr("onclick", "addSource()");
        context.openDiv('adminAddSourceSubPage','bgdiv','添加来源');
    };

    context.getPageSourceData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var sourceData = {};
        sourceData["sourceName"] = $("#sourceName").val().trim();
        sourceData["sourceDesc"] = $("#sourceDesc").val().trim();

        return sourceData;
    };


    context.addSource = function () {
        var sourceData = context.getPageSourceData();

        if(!sourceData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/source/addSource",type:"post",data:{"sourceData":JSON.stringify(sourceData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddSourceSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editSourceBtn = function (sourceId) {
        var request = $.ajax({url:"/myadmin/source/getSourceForId",data:{"sourceId":sourceId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("来源查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editSource('"+sourceId+"')");

        context.openDiv('adminAddSourceSubPage','bgdiv','编辑来源');
        $("#sourceName").attr("disabled", true)
        $("#sourceName").val(requestBody["sourceName"]);
        $("#sourceDesc").val(requestBody["sourceDesc"]);
    };

    context.editSource = function (sourceId) {
        var sourceData = context.getPageSourceData();
        if(!sourceData){
            return;
        }
        sourceData["id"] = sourceId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/source/editSource",
            type: "post",
            data: {"sourceData": JSON.stringify(sourceData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddSourceSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteSourceBtn = function (sourceId) {
        if (!confirm("确认删除 [" + $("#sourceName_"+sourceId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/source/delSource",
            type: "post",
            data: {"sourceId": sourceId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };


    context.resetSourceBtn = function (sourceId) {
        if (!confirm("确认启用 [" + $("#sourceName_"+sourceId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/source/resetSource",
            type: "post",
            data: {"sourceId": sourceId},
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
        };
    };

    context.queryRequest = function () {
        checkArr.sourceName = $("#querySourceName").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            };
            var key = "";
            if  (index === "sourceName"){
                key = "模块名称";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }

        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "sourceName"){
            $("#querySourceName").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();


