"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc,u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/configHttp/getConfigHttpSubPage",async:false,type:"post",data:data});
        $("#configHttpSubPage").html(htmlobj.responseText);
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
            obbgdiv.height(docheight);
            $('html,body').animate({scrollTop:offtop}, 800);
            obshowdiv.find("input").attr("required","required");
        };

    context.ReloadPage = function(){
        location.reload();
    };

    context.CloseDiv = function (close_div,bg_div) {
        //清空弹出层文本框和下拉框
        $("#httpConfKey").val("");
        $("#alias").val("");
        $("#serviceConfKey").html("");
        $("#httpConfDesc").val("");
        // $("#httpConf").val("");
        $("#apiRunState").val("1");
        $("#uiRunState").val("0");
        $("#dubboRunState").val("0");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.addConfigHttpBtn = function () {
        $("#httpConfKey").attr("disabled", false);
        $("#alias").attr("disabled", false);
        var serviceConfKeys = context.getAllServiceConfKeys();
        for (var serviceConfKeyIndex in serviceConfKeys){
            $("#serviceConfKey").append('<option value="' + serviceConfKeys[serviceConfKeyIndex] + '"> ' + serviceConfKeys[serviceConfKeyIndex] + '</option>');
        }

        $("#submit").attr("onclick","addConfigHttp()");
        context.openDiv('adminAddConfigHttpSubPage','bgdiv','添加环境配置');
    };

    context.getPageConfigHttpData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var configHttpData = {};
        configHttpData["httpConfKey"] = $("#httpConfKey").val().trim();
        configHttpData["serviceConfKey"] = $("#serviceConfKey").val().trim();
        configHttpData["alias"] = $("#alias").val().trim();
        configHttpData["httpConfDesc"] = $("#httpConfDesc").val().trim();
        // configHttpData["httpConf"] = $("#httpConf").val().trim();
        configHttpData["apiRunState"] = $("#apiRunState").val().trim();
        try{
            configHttpData["uiRunState"] = $("#uiRunState").val().trim();
        }catch(err){
            configHttpData["uiRunState"] = 0
        }
        try {
            configHttpData["dubboRunState"] = $("#dubboRunState").val().trim();
        }catch(err){
            configHttpData["dubboRunState"] = 0
        }

        return configHttpData;
    };

    context.getAllServiceConfKeys = function () {
        var ajaxRequest = $.ajax({
            url:"/myadmin/configHttp/getAllServiceConfKeys",
            type:"post",
            async:false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if(request["code"] === 10000){
            context.selected();
            return request["body"];
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
            return;
        }
    };

    context.addConfigHttp = function () {
        var configHttpData = context.getPageConfigHttpData();

        if(!configHttpData){
            return;
        }
        var ajaxRequest = $.ajax({
            url:"/myadmin/configHttp/addConfigHttp",
            type:"post",
            data:{"configHttpData":JSON.stringify(configHttpData)},
            async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddConfigHttpSubPage','bgdiv');
             context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editConfigHttpBtn = function (configHttpId) {
        var request = $.ajax({url:"/myadmin/configHttp/getConfigHttpForId",data:{"configHttpId":configHttpId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("环境配置查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editConfigHttp('"+configHttpId+"')");

        var serviceConfKeys = context.getAllServiceConfKeys();
        $("#serviceConfKey").html("");
        for (var serviceConfKeyIndex in serviceConfKeys){
            if (serviceConfKeys[serviceConfKeyIndex] === requestBody["serviceConfKey"]){
                $("#serviceConfKey").append('<option value="' + serviceConfKeys[serviceConfKeyIndex] + '" selected="selected">' + serviceConfKeys[serviceConfKeyIndex] + '</option>');
            }
            else {
                $("#serviceConfKey").append('<option value="' + serviceConfKeys[serviceConfKeyIndex] + '">' + serviceConfKeys[serviceConfKeyIndex] + '</option>');

            }
        }

        $('.select2').select2();

        $("#httpConfKey").attr("disabled", true);
        $("#httpConfKey").val(requestBody["httpConfKey"]);
        $("#alias").attr("disabled", true);
        $("#alias").val(requestBody["alias"]);
        $("#httpConfDesc").val(requestBody["httpConfDesc"]);
        // $("#httpConf").val(requestBody["httpConf"]);
        $("#apiRunState").val(requestBody["apiRunState"]);
        $("#uiRunState").val(requestBody["uiRunState"]);
        $("#dubboRunState").val(requestBody["dubboRunState"]);
        context.openDiv('adminAddConfigHttpSubPage','bgdiv','编辑环境配置');

    };

    context.editConfigHttp = function (configHttpId) {
        var configHttpData = context.getPageConfigHttpData();
        if(!configHttpData){
            return;
        }
        configHttpData["id"] = configHttpId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/configHttp/editConfigHttp",
            type: "post",
            data: {"configHttpData": JSON.stringify(configHttpData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddConfigHttpSubPage','bgdiv');
             context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteConfigHttpBtn = function (element, configHttpId) {
        if (!confirm("确认删除 [" + $("#httpConfKey_"+configHttpId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/configHttp/delConfigHttp",
            type: "post",
            data: {"configHttpId": configHttpId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetConfigHttpBtn = function (element, configHttpId) {
        if (!confirm("确认启用 [" + $("#httpConfKey_"+configHttpId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/configHttp/resetConfigHttp",
            type: "post",
            data: {"configHttpId": configHttpId},
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
        checkArr.alias = $("#queryAlias").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            };
            var key = "";
            if  (index === "alias"){
                key = "环境配置名称";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
            
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "alias"){
            $("#queryAlias").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();



$(function () {
    //Initialize Select2 Elements
    $('.select2').select2();

})