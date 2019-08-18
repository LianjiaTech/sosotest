"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/businessLineModule/getBusinessLineModule",async:false,type:"post",data:data});
        $("#businessLineModuleSubPage").html(htmlobj.responseText);
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
        // $("#businessLine").val("");
        // $("#module").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.getAllBusinessLines = function () {
        var ajaxRequest = $.ajax({
            url: "/myadmin/businessLineModule/getAllBusinessLines",
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

    context.addBusinessLineModuleBtn = function () {
        var businessLineRequestBody = context.getAllBusinessLines();
        var moduleNameRequestBody = context.getAllModuleNames();

         $('.select2').select2();

        for (var businessLine in businessLineRequestBody){
            $("#businessLine").append('<option value="'+businessLineRequestBody[businessLine]+'"> '+businessLineRequestBody[businessLine] +'</option>');
        }

        for (var moduleName in moduleNameRequestBody){
            $("#module").append('<option value="'+ moduleNameRequestBody[moduleName]+'"> '+ moduleNameRequestBody[moduleName] +' </option>');
        }

        $("#submit").attr("onclick","addBusinessLineModule()");
        context.openDiv('adminAddBusinessLineModuleSubPage','bgdiv','添加业务线模块');
    };


    context.getPageBusinessLineModuleData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var businessLineModuleData = {};
        businessLineModuleData["businessLine"] = $("#businessLine").val().trim();
        businessLineModuleData["module"] = $("#module").val().trim();
        businessLineModuleData["level"] = $("#level").val().trim();

        return businessLineModuleData;
    };


    context.addBusinessLineModule = function () {
        var businessLineModuleData = context.getPageBusinessLineModuleData();

        if(!businessLineModuleData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/businessLineModule/addBusinessLineModule",type:"post",data:{"businessLineModuleData":JSON.stringify(businessLineModuleData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddBusinessLineModuleSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editBusinessLineModuleBtn = function (businessLineModuleId) {
        var request = $.ajax({url:"/myadmin/businessLineModule/getBusinessLineModuleForId",data:{"businessLineModuleId":businessLineModuleId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("业务线的模块查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editBusinessLineModule('"+businessLineModuleId+"')");

         var businessLinesRequestBody = context.getAllBusinessLines();

        var moduleNamesRequestBody = context.getAllModuleNames();

        for (var businessLineIndex in businessLinesRequestBody) {
                    $("#businessLine").append('<option value="' + businessLinesRequestBody[businessLineIndex] + '">' + businessLinesRequestBody[businessLineIndex] + '</option>');
                }

        var htmlobj = $("#businessLine").find("option");
        htmlobj.each(function () {
            if($(this).text() === requestBody["bussinessLineName"]){
                $(this).attr("selected",true);
            }
        });

        $('.select2').select2();



        for (var moduleNameIndex in moduleNamesRequestBody) {
            $("#module").append('<option value="' + moduleNamesRequestBody[moduleNameIndex] + '">' + moduleNamesRequestBody[moduleNameIndex] + '</option>');
        }
        var htmlobjModuleName = $("#module").find("option");
        htmlobjModuleName.each(function () {
            if($(this).text() === requestBody["moduleName"]){
                $(this).attr("selected",true);
            }
        });
        $('.select2').select2();


        context.openDiv('adminAddBusinessLineModuleSubPage','bgdiv','编辑业务线模块');
    };

    context.editBusinessLineModule = function (businessLineModuleId) {
        var businessLineModuleData = context.getPageBusinessLineModuleData();
        if(!businessLineModuleData){
            return;
        }
        businessLineModuleData["id"] = businessLineModuleId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/businessLineModule/editBusinessLineModule",
            type: "post",
            data: {"businessLineModuleData": JSON.stringify(businessLineModuleData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddBusinessLineModuleSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteBusinessLineModuleBtn = function (element, businessLineModuleId) {
        if (!confirm("确认删除 [" + $("#businessLine_"+businessLineModuleId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/businessLineModule/delBusinessLineModule",
            type: "post",
            data: {"businessLineModuleId": businessLineModuleId},
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

    context.getBusinessLineId = function () {
         var businessLineName = $("#queryBusinessLine").val();
         if(businessLineName !=""){
                 var ajaxRequest = $.ajax({
                url: "/myadmin/businessLineModule/getBusinessLineId",
                type: "post",
                data: {"businessLineName": businessLineName},
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

        checkArr.businessLineId = context.getBusinessLineId();
        // checkArr.moduleId = context.getModuleId();


        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            }
            var key = "";
            if  (index === "businessLineId"){

                key = "业务线";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + $("#queryBusinessLine").val() + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }

            // if  (index === "moduleId"){
            //     key = "业务线的模块";
            //     queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            // }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "businessLineId"){
            $("#queryBusinessLine").val("");
        }

        // if (condition === "moduleId"){
        //     $("#queryModule").val("");
        // }
        context.queryRequest();
    };


})(window);
window.selected();


$(function () {
    //Initialize Select2 Elements
    $('.select2').select2();

})