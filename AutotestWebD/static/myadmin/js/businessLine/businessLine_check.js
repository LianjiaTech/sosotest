"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/businessLine/getBusinessLineSubPage",async:false,type:"post",data:data});
        $("#bussinessLineSubPage").html(htmlobj.responseText);
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
            // selected();
            // $("#userAddSubPage").css("display","block");
        };
    
    context.CloseDiv = function (close_div,bg_div) {
        //清空弹出层文本框和下拉框
        $("#bussinessLineName").val("");
        $("#bussinessLineDesc").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.addBusinessLineBtn = function () {
        $("#submit").attr("onclick","addBusinessLine()");
        context.openDiv('adminAddBusinessLineSubPage','bgdiv','添加业务线');
    };

    context.getPageBusinessLineData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var businessLineData = {};
        businessLineData["businessLineName"] = $("#bussinessLineName").val().trim();
        businessLineData["businessLineDesc"] = $("#bussinessLineDesc").val().trim();

        return businessLineData;
    };


    context.addBusinessLine = function () {
        var businessLineData = context.getPageBusinessLineData();

        if(!businessLineData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/businessLine/addBusinessLine",type:"post",data:{"businessLineData":JSON.stringify(businessLineData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminAddBusinessLineSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editBusinessLineBtn = function (businessLineId) {
        var request = $.ajax({url:"/myadmin/businessLine/getBusinessLineForId",data:{"businessLineId":businessLineId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("业务线查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editBusinessLine('"+businessLineId+"')");

        context.openDiv('adminAddBusinessLineSubPage','bgdiv','编辑业务线');
        $("#bussinessLineName").attr("disabled", true);
        $("#bussinessLineName").val(requestBody["bussinessLineName"]);
        $("#bussinessLineDesc").val(requestBody["bussinessLineDesc"]);
    };

    context.editBusinessLine = function (businessId) {
        var businessLineData = context.getPageBusinessLineData();
        if(!businessLineData){
            return;
        }
        businessLineData["id"] = businessId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/businessLine/editBusinessLine",
            type: "post",
            data: {"businessLineData": JSON.stringify(businessLineData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddBusinessLineSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteBusinessLineBtn = function (businessLineId) {
        if (!confirm("确认删除 [" + $("#bussinessLineName_"+businessLineId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/businessLine/delBusinessLine",
            type: "post",
            data: {"businessLineId": businessLineId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetBusinessLineBtn = function (businessLineId) {
        if (!confirm("确认重启 [" + $("#bussinessLineName_"+businessLineId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/businessLine/resetBusinessLine",
            type: "post",
            data: {"businessLineId": businessLineId},
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
        checkArr.bussinessLineName = $("#queryBusinessLineName").val();
        checkArr.type = $("#queryType").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            }
            var key = "";
            if  (index === "bussinessLineName"){
                key = "业务线名称";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "bussinessLineName"){
            $("#queryBusinessLineName").val("");
        }

        context.queryRequest();
    };


})(window);
window.selected();


