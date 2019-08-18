"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc,u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/interfaceModule/getInterfaceModuleSubPage",async:false,type:"post",data:data});
        $("#interfaceModuleSubPage").html(htmlobj.responseText);
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
        $("#url").val("");
        $("#moduleName").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.addInterfaceModuleBtn = function () {
        $("#submit").attr("onclick","addInterfaceModule()");
        context.openDiv('adminAddInterfaceModuleSubPage','bgdiv','添加接口页面');
    };

    context.getPageInterfaceModuleData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var interfaceModuleData = {};
        interfaceModuleData["url"] = $("#url").val().trim();
        interfaceModuleData["moduleName"] = $("#moduleName").val().trim();
        return interfaceModuleData;
    };


    context.addInterfaceModule = function () {
        var interfaceModuleData = context.getPageInterfaceModuleData();

        if(!interfaceModuleData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/interfaceModule/addInterfaceModule",type:"post",data:{"interfaceModuleData":JSON.stringify(interfaceModuleData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddInterfaceModuleSubPage','bgdiv');
             context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editInterfaceModuleBtn = function (interfaceModuleId) {
        var request = $.ajax({url:"/myadmin/interfaceModule/getInterfaceModuleForId",data:{"interfaceModuleId":interfaceModuleId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("接口所属页面查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editInterfaceModule('"+interfaceModuleId+"')");

        context.openDiv('adminAddInterfaceModuleSubPage','bgdiv','编辑接口页面');
        $("#url").val(requestBody["url"]);
        $("#moduleName").val(requestBody["moduleName"]);
    };

    context.editInterfaceModule = function (interfaceModuleId) {
        var interfaceModuleData = context.getPageInterfaceModuleData();
        if(!interfaceModuleData){
            return;
        }
        interfaceModuleData["id"] = interfaceModuleId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/interfaceModule/editInterfaceModule",
            type: "post",
            data: {"interfaceModuleData": JSON.stringify(interfaceModuleData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddInterfaceModuleSubPage','bgdiv');
             context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteInterfaceModuleBtn = function (element, interfaceModuleId) {
        if (!confirm("确认删除 [" + $("#url_"+interfaceModuleId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/interfaceModule/delInterfaceModule",
            type: "post",
            data: {"interfaceModuleId": interfaceModuleId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetInterfaceModuleBtn = function (element, interfaceModuleId) {
        if (!confirm("确认启用 [" + $("#url_"+interfaceModuleId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/interfaceModule/resetInterfaceModule",
            type: "post",
            data: {"interfaceModuleId": interfaceModuleId},
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
        checkArr.url = $("#queryUrl").val();
        checkArr.moduleName = $("#queryModuleName").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            };
            var key = "";
            if  (index === "url"){
                key = "接口";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }

            if  (index === "moduleName"){
                key = "接口所属页面";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "url"){
            $("#queryUrl").val("");
        }

        if (condition === "moduleName"){
            $("#queryModuleName").val("");
        }
        context.queryRequest();
    };


})(window);
window.selected();


