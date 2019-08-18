"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.id desc";
(function (context) {

     context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({
            url:"/myadmin/changeLog/getChangeLogSubPage",
            async:false,
            type:"post",
            data:data
        });
        $("#changeLogSubPage").html(htmlobj.responseText);
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
        checkArr.loginName = $("#queryUserName").val();
        checkArr.otherLoginName = $("#queryOtherUserNameTab").val();
        checkArr.dataId = $("#queryDataIdTab").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            }
            var key = "";
            if  (index === "loginName"){
                key = "修改人";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
            if (index === "otherLoginName"){
                key = "被修改人";
                var value = $("#queryType :checked").text();
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + value + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
            if (index === "dataId"){
                key = "修改的数据ID";
                var value = $("#queryType :checked").text();
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + value + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "loginName"){
            $("#queryUserName").val("");
        }

        if (condition === "otherLoginName"){
            $("#queryOtherUserNameTab").val("");
        }

        if (condition === "dataId"){
            $("#queryDataIdTab").val("");
        }
        context.queryRequest();
    };

    context.getChangeLogDataForId = function (changeLogId){
        var ajaxRequest = $.ajax({
            url:"/myadmin/changeLog/getChangeLogDataForId",
            type:"post",
            async:false,
            data:{"changeLogId":changeLogId}
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if(request["code"] === 10000){
            context.selected();
            return request["body"];
        }else{
            alert("错误" + request["code"] + ":" + request["message"]);
        }
    };

    context.checkDetailsBtn = function(changeLogId) {
        var dataDict = context.getChangeLogDataForId(changeLogId);
        context.openDivCheckDetails('checkDetailsSubPage', 'bgdiv', '查看详情');
        $("#beforeData").val(dataDict["beforeData"]);
        $("#afterData").val(dataDict["afterData"]);
    };
    
    context.openDivCheckDetails = function (show_div, bg_div, title) {

         $("#supPageCheckDetailsTitle").text(title);
         $("body").attr("style", "overflow:scroll;overflow-y:hidden;overflow-x:hidden");
         //弹出详情层
         var obshowdiv = $('#' + show_div);
         var objclosediv = $('#' + show_div + '> label');
         var obbgdiv = $('#' + bg_div);
         var offtop = obshowdiv.offset().top;
         var offleft = obshowdiv.offset().left;
         obshowdiv.css("top", offtop);
         objclosediv.css("top", "20px");
         objclosediv.css("left", "90%");
         obshowdiv.show();
         obbgdiv.show();
         $("#fade").show();
         var docheight = $(document).height();
         obbgdiv.height(docheight);
         $('html,body').animate({scrollTop: offtop}, 800);
     };

    context.CloseDivCheckDetails = function (close_div, bg_div) {

         //清空弹出层文本框和下拉框
         $("#beforeData").val("");
         $("#afterData").val("");
         $("body").attr("style", "height: auto; min-height: 100%;");
         $("#" + close_div).hide();
         $("#" + bg_div).hide();
         $("#fade").hide();
     };



})(window);
window.selected()


