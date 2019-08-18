"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc,u.id desc";
(function (context) {

    context.isObjectValueEqual = function (a, b) {
        // Of course, we can do it use for in
        // Create arrays of property names
        var aProps = Object.getOwnPropertyNames(a);
        var bProps = Object.getOwnPropertyNames(b);

        // If number of properties is different,
        // objects are not equivalent
        if (aProps.length != bProps.length) {
            return false;
        }

        for (var i = 0; i < aProps.length; i++) {
            var propName = aProps[i];

            // If values of same property are not equal,
            // objects are not equivalent
            if (a[propName] !== b[propName]) {
                return false;
            }
        }

        // If we made it this far, objects
        // are considered equivalent
        return true;
    }

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/configService/getConfigServiceSubPage",async:false,type:"post",data:data});
        $("#configServiceSubPage").html(htmlobj.responseText);
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
        $("#serviceConfKey").val("");
        $("#alias").val("");
        $("#serviceConfDesc").val("");
        $("#serviceConf").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.addConfigServiceBtn = function () {
        $("#serviceConf").val('{\n' +
            '    "DB": {\n' +
            '        "default": {\n' +
            '            "comment": "",\n' +
            '            "host": "",\n' +
            '            "port": "",\n' +
            '            "username": "",\n' +
            '            "password": ""\n' +
            '        },\n' +
            '        "test": {\n' +
            '            "comment": "",\n' +
            '            "host": "",\n' +
            '            "port": "",\n' +
            '            "username": "",\n' +
            '            "password": ""\n' +
            '        }\n' +
            '    },\n' +
            '    "REDIS": {\n' +
            '        "default": {\n' +
            '            "comment": "",\n' +
            '            "host": "",\n' +
            '            "port": "",\n' +
            '            "password": ""\n' +
            '        }\n' +
            '    }\n' +
            '}');
        $("#serviceConfKey").attr("disabled", false);
        $("#alias").attr("disabled", false);
        $("#submit").attr("onclick","addConfigService()");
        context.openDiv('adminAddConfigServiceSubPage','bgdiv','添加数据服务器');
    };

    context.getPageConfigServiceData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var configServiceData = {};
        configServiceData["serviceConfKey"] = $("#serviceConfKey").val().trim();
        configServiceData["alias"] = $("#alias").val().trim();
        configServiceData["serviceConfDesc"] = $("#serviceConfDesc").val().trim();
        configServiceData["serviceConf"] = $("#serviceConf").val().trim();

        return configServiceData;
    };


    context.addConfigService = function () {
        var configServiceData = context.getPageConfigServiceData();

        if(!configServiceData){
            return;
        }
        var ajaxRequest = $.ajax({
            url:"/myadmin/configService/addConfigService",
            type:"post",
            data:{"configServiceData":JSON.stringify(configServiceData)},
            async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddConfigServiceSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };
    
    context.getConfigData = function (configServiceId) {
        var request = $.ajax({url:"/myadmin/configService/getConfigServiceForId",data:{"configServiceId":configServiceId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("数据服务器查询错误，请联系管理员");
            return false;
        }
        console.log(requestJSON["body"])
        return requestJSON["body"];
    };

    context.editConfigServiceBtn = function (configServiceId) {
        // var request = $.ajax({url:"/myadmin/configService/getConfigServiceForId",data:{"configServiceId":configServiceId},async:false,type:"post"});
        //
        // var requestJSON = JSON.parse(request.responseText);
        // if (requestJSON["code"] !== 10000){
        //     alert("数据服务器查询错误，请联系管理员");
        //     return ;
        // }
        var requestJSON = getConfigData(configServiceId);
        if (!requestJSON){
            return ;
        }
        var requestBody = requestJSON;
        $("#serviceConfKey_"+configServiceId).data(requestBody);
        $("#submit").attr("onclick","editConfigService('"+configServiceId+"')");

        context.openDiv('adminAddConfigServiceSubPage','bgdiv','编辑数据服务器');
        $("#serviceConfKey").attr("disabled", true);
        $("#serviceConfKey").val(requestBody["serviceConfKey"]);
        $("#alias").attr("disabled", true);
        $("#alias").val(requestBody["alias"]);
        $("#serviceConfDesc").val(requestBody["serviceConfDesc"]);
        $("#serviceConf").val(requestBody["serviceConf"]);
    };

    context.editConfigService = function (configServiceId) {
        var requestJSON = getConfigData(configServiceId);
        if (!requestJSON){
            return ;
        }
        console.log($("#serviceConfKey_"+configServiceId).data())
        if (!isObjectValueEqual(requestJSON,$("#serviceConfKey_"+configServiceId).data())){
            alert("本数据已被 "+requestJSON["modBy"]+" 更新，请刷新后重新编辑");
            return;
        }

        var configServiceData = context.getPageConfigServiceData();
        if(!configServiceData){
            return;
        }
        configServiceData["id"] = configServiceId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/configService/editConfigService",
            type: "post",
            data: {"configServiceData": JSON.stringify(configServiceData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddConfigServiceSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteConfigServiceBtn = function (element, configServiceId) {
        if (!confirm("确认删除 [" + $("#serviceConfKey_"+configServiceId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/configService/delConfigService",
            type: "post",
            data: {"configServiceId": configServiceId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetConfigServiceBtn = function (element, configServiceId) {
        if (!confirm("确认启用 [" + $("#serviceConfKey_"+configServiceId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/configService/resetConfigService",
            type: "post",
            data: {"configServiceId": configServiceId},
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
                key = "服务名";
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


