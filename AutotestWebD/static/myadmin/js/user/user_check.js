"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function() {
        var data = {checkArr : encodeURI(JSON.stringify(checkArr)),orderBy : orderBy,page:page};
        var htmlobj = $.ajax({url:"/myadmin/user/getUserSubPage",async:false,type:"post",data:data});
        $("#userSubPage").html(htmlobj.responseText);
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
            obshowdiv.find("input").not("#token").attr("required","required");
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
        $("#state").val($("#state").children().eq(0).val());
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style","height: auto; min-height: 100%;");
        $("#"+close_div).hide();
        $("#"+bg_div).hide();
        $("#fade").hide();
    };

    context.addUserBtn = function () {
        $("#account").attr("disabled", false);
        $("#submit").attr("onclick","addUser()");
        context.openDiv('userAddSubPage','bgdiv','添加用户');
    };

    context.getPageUserData = function () {
        var verifyElement = $("input[required='required']");
        for (var index = 0; index < verifyElement.length ; index ++){
            if (verifyElement.eq(index).val()===""){
                return false;
            }
        }
        var userData = {};

        userData["loginName"] = $("#account").val().trim();
        userData["email"] = $("#email").val().trim();
        userData["userName"] = $("#userName").val().trim();
        userData["pwd"] = $("#passWord").val().trim();
        userData["pwd1"] = $("#passWord1").val().trim();
        if(userData["pwd"] != userData["pwd1"]){
            alert("两次密码输入不一致，请重新输入");
            return ;
        }
        userData["token"] = $("#token").val().trim();
        userData["type"] = $("#userType").val().trim();
        userData["audit"] = $("#audit").val().trim();
        userData["state"] = $("#state").val().trim();
        userData["defaultPermission"] = $("#defaultPermission").val().trim();
        return userData;
    };


    context.addUser = function () {
        var userData = context.getPageUserData();
        if(!userData){
            return;
        }
        var ajaxRequest = $.ajax({url:"/myadmin/user/addUser",type:"post",data:{"userData":JSON.stringify(userData)},async:false});
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000){
            context.CloseDiv('userAddSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        }else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editUserBtn = function (userId) {
        var request = $.ajax({url:"/myadmin/user/getUserForId",data:{"userId":userId},async:false,type:"post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000){
            alert("用户查询错误，请联系管理员");
            return ;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick","editUser('"+userId+"')");

        context.openDiv('userAddSubPage','bgdiv','编辑用户');
        $("#passWord").removeAttr("required");
        $("#passWord1").removeAttr("required");
        $("#account").attr("disabled", true);
        $("#account").val(requestBody["loginName"]);
        $("#passWord").val("");
        $("#passWord1").val("");
        $("#userName").val(requestBody["userName"]);
        $("#email").val(requestBody["email"]);
        $("#token").val(requestBody["token"]);
        $("#userType").val(requestBody["type"]);
        $("#audit").val(requestBody["audit"]);
        $("#state").val(requestBody["state"]);
        $("#defaultPermission").val(requestBody["defaultPermission"]);
    };

    context.editUser = function (userId) {
        var userData = context.getPageUserData();
        if(!userData){
            return;
        }
        userData["id"] = userId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/user/editUser",
            type: "post",
            data: {"userData": JSON.stringify(userData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('userAddSubPage','bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteUserBtn = function (userId) {
        if (!confirm("确认删除 [" + $("#userName_"+userId ).text()+ "]  ?" )){
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/user/delUser",
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
        context.openDiv('userAutorizeSubPage', 'bgdiv', '用户授权');
        context.doubleBoxFunction(userId);
    };

    context.authorizeAllUsersBtn = function () {
        context.openDiv("allUsersAuthorizeSubPage", 'bgdiv', '所有用户授权');
        context.authorizeAllUsersBoubleBoxFunction();
    };

    context.getSelectedPermissionKeys = function () {
        var permissionKeys = [];
        //var permissionKeys = new Array(); //数组定义标准形式，不要写成Array arr = new Array();
        $("#userAutorizeSubPage").find("#bootstrap-duallistbox-selected-list_doublebox option").each(function () {
            var val = $(this).val(); //获取单个value
            permissionKeys.push(val);
        });
        return permissionKeys;
    };

    context.getAllSelectedPermissionKeys = function () {
        var permissionKeysAllUsers = new Array(); //数组定义标准形式，不要写成Array arr = new Array();
        $("#allUsersAuthorizeSubPage").find("#bootstrap-duallistbox-selected-list_doublebox option").each(function () {
            var val = $(this).val(); //获取单个value

            permissionKeysAllUsers.push(val);
        });
        return permissionKeysAllUsers;
    };

    context.getAllPermissions = function () {
        var request = $.ajax({url:"/myadmin/interfacePermission/getAllPermissionKeys", async: false, type: "post"});
        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("用户查询错误，请联系管理员");
            return;
        };

        var requestBody = requestJSON["body"];
        return requestBody;
    };


     var requestBody = [];
    var requestAllBody = [];
    context.doubleBoxFunction = function (loginName) {

        requestBody = [];
        requestAllBody = [];

        requestBody = context.getAllPermissions();

        var requestAll = $.ajax({url: "/myadmin/interfacePermission/getUserPermissionKeys", data: {"loginName": loginName}, async: false, type: "post"});
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
        userPermissionsData["loginName"] = loginName;
        userPermissionsData["permissionKeys"] = permissionKeys;

        var ajaxRequest = $.ajax({
            url: "/myadmin/user/addPermissionsToUser",
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



    context.getAllUsersSelectedPermissions = function () {
        var requestAll = $.ajax({url: "/myadmin/permission/getAllUsersSelectedPermissions", async: false, type: "post"});
        var requestAllJSON = JSON.parse(requestAll.responseText);
        if (requestAllJSON["code"] !== 10000) {
            alert("权限查询错误，请联系管理员");
            return;
        }
        var requestAllBody = requestAllJSON["body"];
        return requestAllBody;
    }

    var requestBodyAllUsers = [];
    var requestAllBodyAllUsers = [];
    context.authorizeAllUsersBoubleBoxFunction = function () {

        requestBodyAllUsers = [];
        requestAllBodyAllUsers = [];

        requestBodyAllUsers = context.getAllPermissions();
        requestAllBodyAllUsers = context.getAllUsersSelectedPermissions();


        for (var i=0; i<requestAllBodyAllUsers.length; i++) {
            for (var j=0; j<requestBodyAllUsers.length; j++) {
                    var permissionKey = requestAllBodyAllUsers[i]["permissionKey"];
                    var key = requestBodyAllUsers[j]["permissionKey"];
                if (permissionKey == key){
                    requestBodyAllUsers.splice(j,1);
                }
            }
        };


        $('#allUsersAuthorizeSubPage').find("select").html("");
            $('.demo').doublebox({
                nonSelectedListLabel: '选择权限',
                selectedListLabel: '已选择的权限',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false,
                nonSelectedList: requestBodyAllUsers,
                selectedList: requestAllBodyAllUsers,
                optionValue: "permissionKey",
                optionText: "permissionName",
                doubleMove: true,
            });

        context.allUsersAuthorize = function () {
        var permissionKeys = context.getAllSelectedPermissionKeys();

        var userPermissionsData = {};
        //userPermissionsData["userId"] = userId;
        userPermissionsData["permissionKeys"] = permissionKeys;
        $("#loading").css("display", "");
        context.CloseDiv('allUsersAuthorizeSubPage', 'bgdiv');
        var ajaxRequest = $.ajax({
            url: "/myadmin/user/addPermissionsToAllUsers",
            type: "post",
            data: {"userPermissionsData": JSON.stringify(userPermissionsData)},
            async: true,
            timeout: 0,
            success:function () {
                var request = JSON.parse(ajaxRequest.responseText);
                if (request["code"] === 10000) {
                    requestBody = []
                    requestAllBody = []
                    context.selected();
                } else {
                    alert("错误 " + request["code"] + ":" + request["message"]);
                }
                $("#loading").css("display", "none");
            },
            error:function (XMLHttpRequest, textStatus, errorThrown) {
                alert("数据处理过大，请求超时");
                $("#loading").css("display", "none");
            }
        });

        };
    }

})(window);
window.selected();
window.resetPwd();

