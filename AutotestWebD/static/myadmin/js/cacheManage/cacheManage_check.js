"use strict";
var page = 1;
var checkArr = {};
(function (context) {

     context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),page:page};
        var htmlobj = $.ajax({
            url:"/myadmin/cacheManage/getCacheManageSubPage",
            async:false,
            type:"post",
            data:data
        });
        $("#cacheManageSubPage").html(htmlobj.responseText);
    };

    context.pageCall = function (pageNum) {
        page = pageNum;
        context.selected();
    };

    context.ReloadPage = function(){
        location.reload();
    };

    context.EnterPress = function () {
        var e = event || window.event;
        if(e.keyCode === 13){
            context.queryRequest();
        }
    };

    context.queryRequest = function () {
        checkArr.cachekey = $("#queryCacheKey").val();

        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            }
            var key = "";
            if  (index === "cachekey"){
                key = "缓存key";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }

        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "cachekey"){
            $("#queryCacheKey").val("");
        }

        context.queryRequest();
    };

    context.openDiv = function (show_div, bg_div, title) {
        $("#supPageTitle").text(title);
        $("body").attr("style", "overflow:scroll;overflow-y:hidden;overflow-x:hidden");
        //弹出详情层
        var obshowdiv = $('#' + show_div);
        var objclosediv = $('#' + show_div + '> label');
        var obbgdiv = $('#' + bg_div);
        var offtop = obshowdiv.offset().top;
        var offleft = obshowdiv.offset().left;
        obshowdiv.css("top", offtop + 160 + "px");
        objclosediv.css("top", "40px");
        objclosediv.css("left", "90%%");
        obshowdiv.show();
        obbgdiv.show();
        $("#fade").show();
        var docheight = $(document).height();
        obbgdiv.height(docheight);
        $('html,body').animate({scrollTop: offtop}, 800);
        // selected();
        // $("#userAddSubPage").css("display","block");
        obshowdiv.find("input").attr("required","required");
    };

    context.CloseDiv = function (close_div, bg_div) {
        //清空弹出层文本框和下拉框
        $("#cacheKey").val("");
        $("#cacheValue").val("");
        $("cacheKey").attr("disabled", false);
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.ReloadPage = function(){
        location.reload();
    };
       
    context.addBtn = function () {
        $("#cacheKey").attr("disabled", false);
        $("#submit").attr("onclick", "addCacheData()");
        context.openDiv("adminAddCacheDataSubPage", "bgdiv", "添加缓存数据");
    };

    context.addCacheData = function () {
        var cacheData = {};
        cacheData["cacheKey"] = $("#cacheKey").val().trim();
        cacheData["cacheValue"] = $("#cacheValue").val().trim();

        if (!cacheData){
            return;
        }
        var ajaxRequest = $.ajax({
            url:"/myadmin/cacheManage/addCacheData",
            type:"post",
            async:false,
            data:{"cacheData":JSON.stringify(cacheData)}
        });  
        var response = JSON.parse(ajaxRequest.responseText);
        if (response["code"] === 10000){
            context.CloseDiv("adminAddCacheDataSubPage", "bgdiv");
            context.ReloadPage();
            context.selected();
        }else{
            alert("错误" + response["code"] + ":" + response["message"]);
        }
    };
    
    context.getCacheValueForCacheKey = function (cacheDataKey) {
        var ajaxRequest = $.ajax({
            url:"/myadmin/cacheManage/getCacheValueForCacheKey",
            type:"post",
            async:false,
            data:{"cacheDataKey":cacheDataKey}
        });
        
        var response = JSON.parse(ajaxRequest.responseText);
        if (response["code"] === 10000){
            return response["body"];
        }else{
            alert("错误" + response["code"] + ":" + response["message"]);
        }
    };
    
    context.editBtn = function (cacheDataKey) {

        var requestBody = context.getCacheValueForCacheKey(cacheDataKey);

        $("#submit").attr("onclick", "editCacheData('" + cacheDataKey + "')");

        context.openDiv('adminAddCacheDataSubPage', 'bgdiv', '编辑缓存数据');
        $("#cacheKey").val(requestBody["cacheKey"]);
        $("#cacheKey").attr("disabled", true);
        $("#cacheValue").val(requestBody["cacheValue"]);
    };
    
    context.editCacheData = function (cacheDataKey) {
       var cacheData = {};
        cacheData["cacheKey"] = $("#cacheKey").val().trim();
        cacheData["cacheValue"] = $("#cacheValue").val().trim();

        if (!cacheData){
            return;
        }
        
        var ajaxRequest = $.ajax({
            url: "/myadmin/cacheManage/editCacheData",
            type: "post",
            data: {"cacheData": JSON.stringify(cacheData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddCacheDataSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteBtn = function (cacheDataKey) {
        if (!confirm("确认删除 [" + cacheDataKey+ "]  ?" )){
            return;
        }
         var ajaxRequest = $.ajax({
            url:"/myadmin/cacheManage/deleteCacheData",
            type:"post",
            async:false,
            data:{"cacheDataKey":cacheDataKey}
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if(request["code"] === 10000){
            context.selected();
        }else{
            alert("错误" + request["code"] + ":" + request["message"]);
        }
    };
    
    context.flushAllBtn = function () {
        if (!confirm("确认删除所有缓存数据?" )){
            return;
        }
        if (!confirm("删除所有缓存数据，可能会影响用户的调试结果?" )){
            return;
        }
         var ajaxRequest = $.ajax({
            url:"/myadmin/cacheManage/flushAllDatas",
            type:"post",
            async:false,
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if(request["code"] === 10000){
            context.selected();
        }else{
            alert("错误" + request["code"] + ":" + request["message"]);
        }
    };





})(window);
window.selected()


