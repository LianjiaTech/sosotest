"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/moduleManage/getModuleManageSubPage",async:false,type:"post",data:data});
        $("#moduleManageSubPage").html(htmlobj.responseText);
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
        $("#moduleName").val("");
        $("#moduleDesc").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.addModuleManageBtn = function () {
        $("#moduleName").attr("disabled", false);
        $("#submit").attr("onclick","addModuleManage()");
        context.openDiv('adminAddModuleManageSubPage','bgdiv','添加模块');
    };

    context.getPageModuleManageData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var moduleManageData = {};
        moduleManageData["moduleName"] = $("#moduleName").val().trim();
        moduleManageData["moduleDesc"] = $("#moduleDesc").val().trim();

        return moduleManageData;
    };


    context.addModuleManage= function () {
        var moduleManageData = context.getPageModuleManageData();

        if(!moduleManageData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/moduleManage/addModuleManage",type:"post",data:{"moduleManageData":JSON.stringify(moduleManageData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddModuleManageSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editModuleManageBtn = function (moduleId) {
        var request = $.ajax({url:"/myadmin/moduleManage/getModuleManageForId",data:{"moduleId":moduleId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("模块查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editModuleManage('"+moduleId+"')");

        context.openDiv('adminAddModuleManageSubPage','bgdiv','编辑模块');
        $("#moduleName").attr("disabled", true)
        $("#moduleName").val(requestBody["moduleName"]);
        $("#moduleDesc").val(requestBody["moduleDesc"]);
    };

    context.editModuleManage = function (moduleId) {
        var moduleManageData = context.getPageModuleManageData();
        if(!moduleManageData){
            return;
        }
        moduleManageData["id"] = moduleId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/moduleManage/editModuleManage",
            type: "post",
            data: {"moduleManageData": JSON.stringify(moduleManageData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddModuleManageSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteModuleManageBtn = function (moduleId) {
        if (!confirm("确认删除 [" + $("#moduleName_"+moduleId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/moduleManage/delModuleManage",
            type: "post",
            data: {"moduleId": moduleId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetModuleManageBtn = function (moduleId) {
        if (!confirm("确认启用 [" + $("#moduleName_"+moduleId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/moduleManage/resetModuleManage",
            type: "post",
            data: {"moduleId": moduleId},
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
        checkArr.moduleName = $("#queryModuleName").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            };
            var key = "";
            if  (index === "moduleName"){
                key = "模块名称";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }

        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "moduleName"){
            $("#queryModuleName").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();


