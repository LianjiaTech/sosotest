"use strict";
var page = 1;
var checkArr = {};
var orderBy = "t.id desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/team/getTeamSubPage", async: false, type: "post", data: data});
        $("#teamSubPage").html(htmlobj.responseText);
    };

    context.pageCall = function (pageNum) {
        page = pageNum;
        context.selected();
    };

    context.ReloadPage = function(){
        location.reload();
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
        $("#teamName").val("");
        $("#teamDesc").val("");
        $("#teamKey").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addTeamBtn = function () {
        $("#teamKey").attr("disabled", false);
        $("#submit").attr("onclick", "addTeam()");
        context.openDiv('teamAddSubPage', 'bgdiv', '添加小组');
    };

    context.getPageTeamData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var teamData = {};
        teamData["teamName"] = $("#teamName").val().trim();
        teamData["teamKey"] = $("#teamKey").val().trim();
        teamData["teamDesc"] = $("#teamDesc").val().trim();
        return teamData;
    }

    context.getPageTeamDataForEdit = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var teamData = {};
        teamData["teamName"] = $("#teamName").val().trim();
        teamData["teamDesc"] = $("#teamDesc").val().trim();
        return teamData;
    };

    context.addTeam = function () {
        var teamData = context.getPageTeamData();
        // alert(teamData);
        if (!teamData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/team/addTeam",
            type: "post",
            data: {"teamData": JSON.stringify(teamData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('teamAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editTeamBtn = function (teamId) {
        var request = $.ajax({url: "/myadmin/team/getTeamForId", data: {"teamId": teamId}, async: false, type: "post"});
        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("小组查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editTeam('" + teamId + "')");

        context.openDiv('teamAddSubPage', 'bgdiv', '编辑小组');
        $("#teamName").val(requestBody["teamName"]);
        $("#teamKey").attr("disabled", true);
        $("#teamKey").val(requestBody["teamKey"]);
        $("#teamDesc").val(requestBody["teamDesc"]);
    };

    context.editTeam = function (teamId) {
        var teamData = context.getPageTeamDataForEdit();
        // delete teamData["teamKey"]
        if (!teamData) {
            return;
        }
        teamData["id"] = teamId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/team/editTeam",
            type: "post",
            data: {"teamData": JSON.stringify(teamData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('teamAddSubPage', 'bgdiv');
             context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteTeamBtn = function (element, teamId) {
        if (!confirm("确认删除 [" + $("#teamName_" + teamId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/team/delTeam",
            type: "post",
            data: {"teamId": teamId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetTeamBtn = function (element, teamId) {
        if (!confirm("确认启用 [" + $("#teamName_" + teamId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/team/resetTeam",
            type: "post",
            data: {"teamId": teamId},
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
        $("#passWord").val("123465");
    };

    context.EnterPress = function () {
        var e = event || window.event;
        if (e.keyCode === 13) {
            context.queryRequest();
        }
    };

    context.queryRequest = function () {
        checkArr.teamName = $("#queryTeamName").val();
        checkArr.type = $("#queryType").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "teamName") {
                key = "小组名称";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }

        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.addUsersToTeamBtn = function (teamId) {
        context.openDiv('teamAddUsersSubPage', 'bgdiv', '编辑小组');
        context.doubleBoxFunction(teamId);
    };


    
    context.delQuery = function (condition) {
        if (condition === "teamName") {
            $("#queryTeamName").val("");
        }

        if (condition === "type") {
            $("#queryType").val($("#queryType").children().eq(0).val());
        }
        context.queryRequest();
    };


    
    context.getSelectedLoginNames = function () {
        var loginNames = new Array(); //数组定义标准形式，不要写成Array arr = new Array();
        $("#teamAddUsersSubPage").find("#bootstrap-duallistbox-selected-list_doublebox option").each(function () {
            var val = $(this).val(); //获取单个value

            loginNames.push(val);
        });
        return loginNames;
    };

    context.getAllUsers = function () {
        var request = $.ajax({url:"/myadmin/team/getAllUsers", async: false, type: "post"});
        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("用户查询错误，请联系管理员");
            return;
        };

        return requestJSON["body"];
    };

    var requestBody = [];
    var requestAllBody = [];

    //加载用户的
    context.doubleBoxFunction = function (teamId) {
        requestBody = [];
        requestAllBody = [];
        requestBody = context.getAllUsers();

        var requestAll = $.ajax({url: "/myadmin/team/getAllSelectedUsers", data: {"teamId": teamId}, async: false, type: "post"});
        var requestAllJSON = JSON.parse(requestAll.responseText);
        if (requestAllJSON["code"] !== 10000) {
            alert("小组成员查询错误，请联系管理员");
            return;
        }
        requestAllBody = requestAllJSON["body"];


        for (var i=0; i<requestAllBody.length; i++) {
            for (var j=0; j<requestBody.length; j++) {
                    var loginName = requestAllBody[i]["loginName"];
                    var name = requestBody[j]["loginName"];
                if (loginName === name){
                    requestBody.splice(j,1);

                }
            }
        };

        $('#teamAddUsersSubPage').find("select").html("");
        $('#teamAddUsersSubSelect').doublebox({
            nonSelectedListLabel: '选择用户',
            selectedListLabel: '已选择的用户',
            preserveSelectionOnMove: 'moved',
            moveOnSelect: false,
            nonSelectedList: requestBody,
            selectedList: requestAllBody,
            optionValue: "loginName",
            optionText: "userName",
            doubleMove: true
        });

        context.saveUsersToTeam = function () {
            var loginNames = context.getSelectedLoginNames();

            var teamUsersData = {};
            teamUsersData["teamId"] = teamId;
            teamUsersData["loginNames"] = loginNames;

            var ajaxRequest = $.ajax({
                url: "/myadmin/team/addUsersToTeam",
                type: "post",
                data: {"teamUsersData": JSON.stringify(teamUsersData)},
                async: false
            });
            var request = JSON.parse(ajaxRequest.responseText);
            if (request["code"] === 10000) {
                // context.selected();
                context.CloseDiv('teamAddUsersSubPage', 'bgdiv');
                requestBody = [];
                requestAllBody = [];
                context.selected();
            } else {
                alert("错误 " + request["code"] + ":" + request["message"]);
            }
        };
    };


    context.teamAuthorizeBtn = function (teamId) {
        context.openDiv('teamAutorizeSubPage', 'bgdiv', '小组授权');
        context.authorizeDoubleBoxFunction(teamId);
    };

    context.getSelectedTeamPermissionKeys = function () {
        var permissionKeys = new Array(); //数组定义标准形式，不要写成Array arr = new Array();
        $("#teamAutorizeSubPage").find("#bootstrap-duallistbox-selected-list_doublebox option").each(function () {
            var val = $(this).val(); //获取单个value

            permissionKeys.push(val);
        });
        return permissionKeys;
    }

     context.getAllPermissions = function () {
        var request = $.ajax({url:"/myadmin/interfacePermission/getAllPermissionKeys", async: false, type: "post"});
        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("用户查询错误，请联系管理员");
            return;
        };

        var requestBody = requestJSON["body"];
        return requestBody;
    }

    var authorizeRequestBody = [];
    var authorizeRequestAllBody = [];

    //加载权限的
    context.authorizeDoubleBoxFunction = function (teamKey) {
        authorizeRequestAllBody = [];
        authorizeRequestBody = [];
        authorizeRequestBody = context.getAllPermissions();

        var requestAll = $.ajax({
            url: "/myadmin/interfacePermission/getTeamPermissionKeys",
            data: {"teamKey": teamKey},
            async: false,
            type: "post"
        });
        var requestAllJSON = JSON.parse(requestAll.responseText);
        if (requestAllJSON["code"] !== 10000) {
            alert("权限查询错误，请联系管理员");
            return;
        }
        authorizeRequestAllBody = requestAllJSON["body"];

        for (var i=0; i<authorizeRequestAllBody.length; i++) {
            for (var j=0; j<authorizeRequestBody.length; j++) {
                    var permissionKey = authorizeRequestAllBody[i]["permissionKey"];
                    var key = authorizeRequestBody[j]["permissionKey"];
                if (permissionKey == key){
                    authorizeRequestBody.splice(j,1);
                }
            }
        };

         $('#teamAutorizeSubPage').find("select").html("");
           $('#teamAutorizeSubSelect').doublebox({
                nonSelectedListLabel: '选择权限',
                selectedListLabel: '已选择的权限',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false,
                nonSelectedList: authorizeRequestBody,
                selectedList: authorizeRequestAllBody,
                optionValue: "permissionKey",
                optionText: "permissionName",
                doubleMove: true,
            });

        context.teamAuthorize = function () {
        var permissionKeys = context.getSelectedTeamPermissionKeys();

        var teamPermissionsData = {};
        teamPermissionsData["teamKey"] = teamKey;
        teamPermissionsData["permissionKeys"] = permissionKeys;

        var ajaxRequest = $.ajax({
            url: "/myadmin/team/addPermissionsToTeam",
            type: "post",
            data: {"teamPermissionsData": JSON.stringify(teamPermissionsData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('teamAutorizeSubPage', 'bgdiv');
            authorizeRequestBody = [];
            authorizeRequestAllBody = [];
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
        };

    };

     context.openDivTransferData = function (show_div, bg_div, title) {
         //打开的时候，加载dataType的数据
         $("#dataType").html(dataTypeHtml);
         $("#supPageTransferDataTitle").text(title);
         $("body").attr("style", "overflow:scroll;overflow-y:hidden;overflow-x:hidden");
         //弹出详情层
         var obshowdiv = $('#' + show_div);
         var objclosediv = $('#' + show_div + '> label');
         var obbgdiv = $('#' + bg_div);
         var offtop = obshowdiv.offset().top;
         var offleft = obshowdiv.offset().left;
         obshowdiv.css("top", offtop + 160 + "px");
         objclosediv.css("top", "40px");
         objclosediv.css("left", "90%");
         obshowdiv.show();
         obbgdiv.show();
         $("#fade").show();
         var docheight = $(document).height();
         obbgdiv.height(docheight);
         $('html,body').animate({scrollTop: offtop}, 800);
           $("#transferDataSubPage").css("display","block");
         //obshowdiv.find("input").attr("required","required");
     };

     context.CloseDivTransferData = function (close_div, bg_div) {
         //关闭的时候，清空数据
         $("#fromUsers").html("");
         $("#dataType").html("");
         $("#toUsers").html("");
         $('.select2').select2();

         //清空弹出层文本框和下拉框
         $("#dataType").val("");
         $("#fromUsers").val("");
         $("#toUsers").val("");
         $("#" + close_div).find("input[required='required']").removeAttr("required");
         $("body").attr("style", "height: auto; min-height: 100%;");
         $("#" + close_div).hide();
         $("#" + bg_div).hide();
         $("#fade").hide();
     };

     context.transferDataBtn = function (teamId) {
          var ajaxrequest = $.ajax({
              url:"/myadmin/team/getTeammates",
              async:false,
              type: "post",
              data: {"teamId": teamId}
          });
         var requestJSON = JSON.parse(ajaxrequest.responseText);
         if (requestJSON["code"] != 10000){
             alert("小组成员获取失败，请联系管理员");
             return;
         }
         var requestBody = requestJSON["body"];
         for(var userIndex in requestBody){
              $("#fromUsers").append('<option value="'+userIndex+'">'+requestBody[userIndex]+'</option>');
              $("#toUsers").append('<option value="'+userIndex+'">'+requestBody[userIndex]+'</option>');
         }
         context.openDivTransferData('transferDataSubPage', 'bgdiv', '转移数据');
     };

     context.getPageTransferData = function () {
        var typeList = []; //数组定义标准形式，不要写成Array arr = new Array();
        $("#transferDataSubPage").find("#dataType option:selected").each(function () {
            var val = $(this).val(); //获取单个value

            typeList.push(val);
        });
        return typeList;
    };

    context.getPageFromUsers = function () {
        var fromUsersList = []; //数组定义标准形式，不要写成Array arr = new Array();
        $("#transferDataSubPage").find("#fromUsers option:selected").each(function () {
            var val = $(this).val(); //获取单个value
            fromUsersList.push(val);
        });
        return fromUsersList;
    };

    context.getPageToUsers = function () {
        return $("#transferDataSubPage").find("#toUsers option:selected").val();
    };

    context.transferData = function () {
        var dataTypeList = context.getPageTransferData();
        var fromUsersList = context.getPageFromUsers();
        var toUser = context.getPageToUsers();
        var dataDict = {};
        dataDict["dataTypeList"] = dataTypeList;
        dataDict["fromUsersList"] = fromUsersList;
        dataDict["toUser"] = toUser;
        $("#loading").css("display", "");
        context.CloseDivTransferData('transferDataSubPage', 'bgdiv', '转移数据');
        var ajaxRequest = $.ajax({
            url: "/myadmin/team/tansferData",
            async: true,
            type: "post",
            data:{"dataDict": JSON.stringify(dataDict)},
            timeout: 0,
            success:function () {
                var requestJSON = JSON.parse(ajaxRequest.responseText);
                if (requestJSON["code"] === 10000) {
                    context.selected();
                    // return;
                }else {
                    alert("获取转移数据失败，请联系管理员");
                }
                $("#loading").css("display", "none");
                // context.CloseDivTransferData('transferDataSubPage', 'bgdiv', '转移数据');
            },
            error:function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("转移数据太大，请求超时");
                    $("#loading").css("display", "none");
                }
        });

    }

})(window);
// window.doubleBoxFunction();
window.selected();
window.resetPwd();

//获得dataType数据
var dataTypeHtml = $("#dataType").html();

 $(function () {
         //Initialize Select2 Elements
     $('.select2').select2();

 })

