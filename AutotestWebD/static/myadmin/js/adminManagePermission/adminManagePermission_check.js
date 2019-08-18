"use strict";
var page = 1;
var checkArr = {};
var orderBy = "t.state desc, t.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/adminManagePermission/getPermissionSubPage", async: false, type: "post", data: data});
        $("#adminManagePermissionSubPage").html(htmlobj.responseText);
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
        obshowdiv.find("input").attr("required","required");
        // selected();
        // $("#userAddSubPage").css("display","block");
    };

    context.CloseDiv = function (close_div, bg_div) {
        //清空弹出层文本框和下拉框
        $("#permissionName").val("");
        $("#permissionKey").val("");
        $("#permissionValue").val("");
        $("#isDefaultPermission").val("0");

        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addPermissionBtn = function () {
        $("#permissionKey").attr("disabled", false);
        $("#submit").attr("onclick", "addPermission()");
        context.openDiv('permissionAddSubPage', 'bgdiv', '添加权限');
    };

    context.getPagePermissionData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var permissionData = {};
        permissionData["permissionName"] = $("#permissionName").val().trim();
        permissionData["permissionKey"] = $("#permissionKey").val().trim();
        permissionData["permissionValue"] = $("#permissionValue").val().trim();
        permissionData["isDefaultPermission"] = $("#isDefaultPermission").val().trim();
        // teamData["teamDesc"] = $("#teamDesc").val().trim();
        return permissionData;
    }


    context.addPermission = function () {
        var permissionData = context.getPagePermissionData();
        // alert(teamData);
        if (!permissionData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/adminManagePermission/addPermission",
            type: "post",
            data: {"permissionData": JSON.stringify(permissionData)},
            async: false
        });
        console.log(ajaxRequest.responseText)
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            CloseDiv('permissionAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editPermissionBtn = function (permissionId) {
        var request = $.ajax({url: "/myadmin/adminManagePermission/getPermissionForId", data: {"permissionId": permissionId}, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("权限查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editPermission('" + permissionId + "')");

        context.openDiv('permissionAddSubPage', 'bgdiv', '编辑权限');
        $("#permissionName").val(requestBody["permissionName"]);
        $("#permissionKey").attr("disabled", true);
        $("#permissionKey").val(requestBody["permissionKey"]);
        $("#permissionValue").attr("disabled", true);
        $("#permissionValue").val(requestBody["permissionValue"]);
        $("#isDefaultPermission").val(requestBody["isDefaultPermission"]);
        // $("#teamDesc").val(requestBody["teamDesc"]);
    };

    context.editPermission = function (permissionId) {
        var permissionData = context.getPagePermissionData();
        if (!permissionData) {
            return;
        }
        permissionData["id"] = permissionId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/adminManagePermission/editPermission",
            type: "post",
            data: {"permissionData": JSON.stringify(permissionData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            CloseDiv('permissionAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deletePermissionBtn = function (element, permissionId) {
        if (!confirm("确认删除 [" + $("#permissionName_" + permissionId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/adminManagePermission/delPermission",
            type: "post",
            data: {"permissionId": permissionId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetPermissionBtn = function (element, permissionId) {
        if (!confirm("确认启用 [" + $("#permissionName_" + permissionId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/adminManagePermission/resetPermission",
            type: "post",
            data: {"permissionId": permissionId},
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
    };

    context.EnterPress = function () {
        var e = event || window.event;
        if (e.keyCode === 13) {
            context.queryRequest();
        }
    };

    context.queryRequest = function () {
        checkArr.permissionName = $("#queryPermissionName").val();
        checkArr.type = $("#queryType").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "permissionName") {
                key = "权限名称";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }

        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.addUsersToTeamBtn = function (roleId) {
        $("#submit").attr("onclick", "addUsersToRole()");
        // context.openDiv('teamAddSubPage', 'bgdiv', '编辑小组');
        context.openDiv('roleAddUsersSubPage', 'bgdiv', '添加权限成员');

    }

    context.addUsersToTeam = function (teamId) {
        $("#submit").attr("onclick", "addUsersToTeam()");
        context.openDiv('teamAddUsersSubPage', 'bgdiv', '添加权限');

    }
    
    context.delQuery = function (condition) {
        if (condition === "permissionName") {
            $("#queryPermissionName").val("");
        }

        if (condition === "type") {
            $("#queryType").val($("#queryType").children().eq(0).val());
        }
        context.queryRequest();
    };

    // context.doubleBoxFunction = function () {
    //     $(document).ready(function () {
    //         var demo2 = $('.demo').doublebox({
    //             nonSelectedListLabel: '选择角色',
    //             selectedListLabel: '授权用户角色',
    //             preserveSelectionOnMove: 'moved',
    //             moveOnSelect: false,
    //             nonSelectedList: [{"roleId": "1", "roleName": "zhangsan"}, {"roleId": "2", "roleName": "lisi"}, {
    //                 "roleId": "3",
    //                 "roleName": "wangwu"
    //             }],
    //             selectedList: [{"roleId": "4", "roleName": "zhangsan1"}, {"roleId": "5", "roleName": "lisi1"}, {
    //                 "roleId": "6",
    //                 "roleName": "wangwu1"
    //             }],
    //             optionValue: "roleId",
    //             optionText: "roleName",
    //             doubleMove: true,
    //         });
    //     });
    // };

})(window);
// window.doubleBoxFunction();
window.selected();
window.resetPwd();

