"use strict";
var page = 1;
var checkArr = {};
var orderBy = "rsc.state desc, rsc.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/serviceConf/getServiceConfSubPage",async:false,type:"post",data:data});
        $("#adminServerConfSubPage").html(htmlobj.responseText);
        selectedTask();
    };

   context.selectedTask = function() {
        var htmlobj = $.ajax({url:"/myadmin/serviceConf/getServiceTaskConfSubPage",async:false,type:"post"});
        $("#adminServiceTaskConfSubPage").html(htmlobj.responseText);
    };
   
   context.queueDeleteTask = function (taskExecuteId) {
       if (confirm("确认从执行队列中删除"+taskExecuteId+"?")){
           var htmlobj = $.ajax({url:"/myadmin/serviceConf/queueDeleteTask?taskExecuteId="+taskExecuteId,async:false,type:"get"});
           if(JSON.parse(htmlobj.responseText).code === 10000){
               alert("请求发送成功，请稍后刷新");
           }
           selected()
       }
   };

   // context.checkSelectTask = function () {
   //     var adminServiceTaskConfSubPageElement = $("#adminServiceTaskConfSubPage");
   //     if (adminServiceTaskConfSubPageElement.css("display") === "none"){
   //          adminServiceTaskConfSubPageElement.show();
   //          context.selectedTask();
   //     }else {
   //         adminServiceTaskConfSubPageElement.hide();
   //     }
   //
   // }


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
            $("#serviceName").attr("required","required");
            $("#serviceMaxProgressNum").attr("required","required");
            // selected();
            // $("#userAddSubPage").css("display","block");
        };
    
    context.CloseDiv = function (close_div,bg_div) {
        //清空弹出层文本框和下拉框
        $("#account").val("");
        context.resetPwd();
        $("#userName").val("");
        $("#email").val("");
        $("#token").val("");
        $("#userType").val($("#userType").children().eq(0).val());
        $("#audit").val($("#audit").children().eq(0).val());
        $("#superManager").val("0");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.addAdminUserBtn = function () {
        $("#account").attr("disabled", false);
        context.openDiv('adminServiceSubPage','bgdiv','添加管理员');
    };

    context.getPageAdminServiceConf = function () {
          var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var userData = {};
        userData["serviceName"] = $("#serviceName").val().trim();
        userData["maxTaskProgressNum"] = $("#serviceMaxTaskProgressNum").val().trim();
        userData["maxCaseProgressNum"] = $("#serviceMaxCaseProgressNum").val().trim();

        return userData;
    };


    context.saveEditAdminServiceConf = function (serviceId) {
        var serviceData = context.getPageAdminServiceConf();
        serviceData.id = serviceId;
        if(!serviceData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/serviceConf/saveEditServiceConf",type:"post",data:{"serviceData":JSON.stringify(serviceData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('adminServiceSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.authorizeBtn = function (userId) {
        context.openDiv('userAutorizeSubPage', 'bgdiv', '管理员授权');
        context.doubleBoxFunction(userId);
    };

      var requestBody = [];
    var requestAllBody = [];
    context.doubleBoxFunction = function (userId) {

        requestBody = [];
        requestAllBody = [];

        requestBody = context.getAllPermissions();

        var requestAll = $.ajax({url: "/myadmin/adminManagePermission/getAllSelectedPermissions", data: {"userId": userId}, async: false, type: "post"});
        var requestAllJSON = JSON.parse(requestAll.responseText);
        if (requestAllJSON["code"] !== 10000) {
            alert("权限查询错误，请联系管理员");
            return;
        }
        requestAllBody = requestAllJSON["body"];



        for (var i=0; i<requestAllBody.length; i++) {
            for (var j=0; j<requestBody.length; j++) {
                    var permissionKey = requestAllBody[i]["permissionKey"];
                    var key = requestBody[j]["permissionKey"];
                if (permissionKey == key){
                    requestBody.splice(j,1);
                }
            }
        }


        $('#userAutorizeSubPage').find("select").html("");
            $('.demo').doublebox({
                nonSelectedListLabel: '选择权限',
                selectedListLabel: '已选择的权限',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false,
                nonSelectedList: requestBody,
                selectedList: requestAllBody,
                optionValue: "permissionKey",
                optionText: "permissionName",
                doubleMove: true,
            });

        context.userAuthorize = function () {
        var permissionKeys = context.getSelectedPermissionKeys();

        var userPermissionsData = {};
        userPermissionsData["userId"] = userId;
        userPermissionsData["permissionKeys"] = permissionKeys;

        var ajaxRequest = $.ajax({
            url: "/myadmin/admin/addPermissionsToUser",
            type: "post",
            data: {"userPermissionsData": JSON.stringify(userPermissionsData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {

            context.CloseDiv('userAutorizeSubPage', 'bgdiv');
            requestBody = []
            requestAllBody = []
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
        };

    };


    context.editAdminServiceConfBtn = function (serviceId) {
        var request = $.ajax({url:"/myadmin/serviceConf/getAdminServiceConfForId",data:{"serviceId":serviceId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("查询错误，请联系管理员");
            return ;
        }
        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","saveEditAdminServiceConf('"+serviceId+"')");

        context.openDiv('adminServiceSubPage','bgdiv','编辑服务');
        $("#serviceName").val(requestBody.serviceName);
        $("#serviceIp").val(requestBody.serviceIp);
        $("#servicePort").val(requestBody.servicePort);
        $("#serviceMaxTaskProgressNum").val(requestBody.maxTaskProgressNum);
        $("#serviceMaxCaseProgressNum").val(requestBody.maxCaseProgressNum);
    };

    context.editAdminServiceConf = function (userId) {
        var userData = context.getPageAdminUserData();
        if(!userData){
            return;
        }
        userData["id"] = userId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/serviceConf/editServiceConf",
            type: "post",
            data: {"userData": JSON.stringify(userData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminServiceSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteAdminUserBtn = function (element, userId) {
        if (!confirm("确认删除 [" + $("#userName_"+userId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/admin/delAdminUser",
            type: "post",
            data: {"userId": userId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetAdminUserBtn = function (element, userId) {
        if (!confirm("确认启用 [" + $("#userName_"+userId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/admin/resetAdminUser",
            type: "post",
            data: {"userId": userId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetPwd = function () {
        $("#passWord").val("123456");
        $("#passWord1").val("123456");
    };
    
    context.EnterPress = function () {
        var e = event || window.event;
        if(e.keyCode === 13){
            context.queryRequest();
        }
    };

    context.queryRequest = function () {
        checkArr.userName = $("#queryUserName").val();
        checkArr.type = $("#queryType").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for(var index in checkArr){
            if (checkArr[index] === ""){
                continue;
            }
            var key = "";
            if  (index === "userName"){
                key = "用户名称";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
            if (index === "type"){
                key = "用户类型";
                var value = $("#queryType :checked").text();
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + value + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "userName"){
            $("#queryUserName").val("");
        }

        if (condition === "type"){
            $("#queryType").val($("#queryType").children().eq(0).val());
        }
        context.queryRequest();
    };

    context.authorizeBtn = function (userId) {
        context.openDiv('userAutorizeSubPage', 'bgdiv', '编辑小组');
        context.doubleBoxFunction(userId);
    };

    context.getSelectedPermissionKeys = function () {
        var permissionKeys = new Array(); //数组定义标准形式，不要写成Array arr = new Array();
        $("#bootstrap-duallistbox-selected-list_doublebox option").each(function () {
            var val = $(this).val(); //获取单个value

            permissionKeys.push(val);
        });
        return permissionKeys;
    };

    context.getAllPermissions = function () {
        var request = $.ajax({url:"/myadmin/adminManagePermission/getAllPermissions", async: false, type: "post"});
        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("用户查询错误，请联系管理员");
            return;
        };

        var requestBody = requestJSON["body"];
        return requestBody;
    };


})(window);
window.selected();
window.resetPwd();

