"use strict";
var page = 1;
var checkArr = {};
var orderBy = "t.state desc, t.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({url: "/myadmin/role/getRoleSubPage", async: false, type: "post", data: data});
        $("#roleSubPage").html(htmlobj.responseText);
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
    };

    context.CloseDiv = function (close_div, bg_div) {
        //清空弹出层文本框和下拉框
        $("#roleName").val("");
        $("#roleKey").val("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    context.addRoleBtn = function () {
        $("#roleKey").attr("disabled", false);
        $("#submit").attr("onclick", "addRole()");
        context.openDiv('roleAddSubPage', 'bgdiv', '添加角色');
    };

    context.getPageRoleData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var roleData = {};
        roleData["roleName"] = $("#roleName").val().trim();
        roleData["roleKey"] = $("#roleKey").val().trim();
        return roleData;
    }


    context.addRole = function () {
        var roleData = context.getPageRoleData();
        // alert(teamData);
        if (!roleData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/role/addRole",
            type: "post",
            data: {"roleData": JSON.stringify(roleData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('roleAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editRoleBtn = function (roleId) {
        var request = $.ajax({url: "/myadmin/role/getRoleForId", data: {"roleId": roleId}, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("角色查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];

        $("#submit").attr("onclick", "editRole('" + roleId + "')");

        context.openDiv('roleAddSubPage', 'bgdiv', '编辑角色');
        $("#roleName").val(requestBody["roleName"]);
        $("#roleKey").attr("disabled", true);
        $("#roleKey").val(requestBody["roleKey"]);
    };

    context.editRole = function (roleId) {
        var roleData = context.getPageRoleData();
        if (!roleData) {
            return;
        }
        roleData["id"] = roleId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/role/editRole",
            type: "post",
            data: {"roleData": JSON.stringify(roleData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('roleAddSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteRoleBtn = function (element, roleId) {
        if (!confirm("确认删除 [" + $("#roleName_" + roleId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/role/delRole",
            type: "post",
            data: {"roleId": roleId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetRoleBtn = function (element, roleId) {
        if (!confirm("确认启用 [" + $("#roleName_" + roleId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/role/resetRole",
            type: "post",
            data: {"roleId": roleId},
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
        if (e.keyCode === 13) {
            context.queryRequest();
        }
    };

    context.queryRequest = function () {
        checkArr.roleName = $("#queryRoleName").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }
            var key = "";
            if (index === "roleName") {
                key = "角色名称";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }

        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    
    context.delQuery = function (condition) {
        if (condition === "roleName") {
            $("#queryRoleName").val("");
        }
        context.queryRequest();
    };


})(window);
window.selected();
window.resetPwd();

