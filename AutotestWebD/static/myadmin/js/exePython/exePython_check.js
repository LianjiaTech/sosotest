"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/exePython/getExePythonSubPage",async:false,type:"post",data:data});
        $("#exePythonSubPage").html(htmlobj.responseText);
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
        $("#execPythonAttr").attr("disabled", false);
        $("#execPythonAttr").val("");
        $("#execPythonDesc").val("");
        $("#execPythonValue").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.addExePythonBtn = function () {
        $("#execPythonAttr").attr("disabled", false);
        $("#submit").attr("onclick","addExePython()");
        context.openDiv('adminAddExePythonSubPage','bgdiv','添加执行Python代码数据');
    };

    context.getPageExePythonData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var exePythonData = {};
        exePythonData["execPythonAttr"] = $("#execPythonAttr").val().trim();
        exePythonData["execPythonDesc"] = $("#execPythonDesc").val().trim();
        exePythonData["execPythonValue"] = $("#execPythonValue").val().trim();

        return exePythonData;
    };


    context.addExePython = function () {
        var exePythonData = context.getPageExePythonData();

        if(!exePythonData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/exePython/addExePython",type:"post",data:{"exePythonData":JSON.stringify(exePythonData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddExePythonSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editExePythonBtn = function (exePythonId) {
        var request = $.ajax({url:"/myadmin/exePython/getExePythonForId",data:{"exePythonId":exePythonId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("Python代码执行错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editExePython('"+exePythonId+"')");

        context.openDiv('adminAddExePythonSubPage','bgdiv','编辑python代码执行');
        $("#execPythonAttr").attr("disabled", true)
        $("#execPythonAttr").val(requestBody["execPythonAttr"]);
        $("#execPythonDesc").val(requestBody["execPythonDesc"]);
        $("#execPythonValue").val(requestBody["execPythonValue"]);
    };

    context.editExePython = function (exePythonId) {
        var exePythonData = context.getPageExePythonData();
        if(!exePythonData){
            return;
        }
        exePythonData["id"] = exePythonId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/exePython/editExePython",
            type: "post",
            data: {"exePythonData": JSON.stringify(exePythonData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddExePythonSubPage','bgdiv');
             context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteExePythonBtn = function (exePythonId) {
        if (!confirm("确认删除 [" + $("#execPythonAttr_"+exePythonId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/exePython/delExePython",
            type: "post",
            data: {"exePythonId": exePythonId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetExePythonBtn = function (exePythonId) {
        if (!confirm("确认启用 [" + $("#execPythonAttr_"+exePythonId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/exePython/resetExePython",
            type: "post",
            data: {"exePythonId": exePythonId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };
    context.clearRedisKey = function (attrKey) {
        if (!confirm("确认让属性 [" + attrKey+ "] 立即生效么?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/exePython/delRedisKey",
            type: "post",
            data: {"key": attrKey},
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
        checkArr.execPythonAttr = $("#queryExecPythonAttr").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            };
            var key = "";
            if  (index === "execPythonAttr"){
                key = "属性key";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }

        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "execPythonAttr"){
            $("#queryExecPythonAttr").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();


