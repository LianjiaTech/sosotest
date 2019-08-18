"use strict";
var page = 1;
var checkArr = {};
var orderBy = "u.state desc, u.id desc";
(function (context) {

    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page};
        var htmlobj = $.ajax({
            url: "/myadmin/interfacePermission/getInterfacePermissionSubPage",
            async: false,
            type: "post",
            data: data
        });
        $("#interfacePermissionSubPage").html(htmlobj.responseText);
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
        obshowdiv.find("input").attr("required", "required");
    };

    context.CloseDiv = function (close_div, bg_div) {
        //清空弹出层文本框和下拉框
        $("#url").html("");
        $("#permissionKey").html("");
        $("#" + close_div).find("input[required='required']").removeAttr("required");
        $("body").attr("style", "height: auto; min-height: 100%;");
        $("#" + close_div).hide();
        $("#" + bg_div).hide();
        $("#fade").hide();
    };

    // context.getInterfaces = function () {
    //     var ajaxrequest = $.ajax({
    //         url: "/myadmin/interfacePermission/getAllInterface",
    //         async: false,
    //         type: "post"
    //     });
    //     var requestJSON = JSON.parse(ajaxrequest.responseText);
    //     if (requestJSON["code"] != 10000) {
    //         alert("接口获取失败，请联系管理员");
    //         return;
    //     }
    //     return requestJSON["body"];
    // }

    // context.getPermissionKeys = function () {
    //     var ajaxrequest = $.ajax({
    //         url: "/myadmin/interfacePermission/getAllPermissionKeys",
    //         async: false,
    //         type: "post"
    //     });
    //     var permissionKeysRequestJSON = JSON.parse(ajaxrequest.responseText);
    //     if (permissionKeysRequestJSON["code"] != 10000) {
    //         alert("权限获取失败，请联系管理员");
    //         return;
    //     }
    //     return permissionKeysRequestJSON["body"];
    // };


    context.addInterfacePermissionBtn = function () {
        $("#submit").attr("onclick", "addInterfacePermission()");
        context.openDiv('adminAddInterfacePermissionSubPage', 'bgdiv', '添加接口权限');
    };

    context.interfacePermissionReload = function () {

        $('#loadingPage').css('display', 'block');
        var ajaxRequest = $.ajax({
            url: "/myadmin/interfacePermission/reload",
            type: "get",
            async: true,
            success:function () {
                try{
                    var ajaxJson = JSON.parse(ajaxRequest.responseText);
                    if (ajaxJson["code"] === 10000){
                        alert("刷新完成");
                        $("#loadingPage").css("display", "none");
                    }else {
                        alert("刷新失败,请联系管理员");
                        $("#loadingPage").css("display", "none");
                    }
                }catch (err){
                    alert("刷新异常,请联系管理员");
                    $("#loadingPage").css("display", "none");
                }
            }
        });



    }

    context.getPageInterfacePermissionData = function () {
        var verifyElement = $("[required='required']");
        for (var index = 0; index < verifyElement.length; index++) {
            if (verifyElement.eq(index).val() === "") {
                return false;
            }
        }
        var interfacePermissionData = {};

        interfacePermissionData["permissionName"] = $("#permissionName").val().trim();
        interfacePermissionData["permissionKey"] = $("#permissionKey").val().trim();
        interfacePermissionData["url"] = $("#url").val().trim();
        interfacePermissionData["permission"] = $("#permission").val().trim();
        interfacePermissionData["isDefault"] = $("#isDefault").val().trim();

        return interfacePermissionData;
    };


    context.addInterfacePermission = function () {
        var interfacePermissionData = context.getPageInterfacePermissionData();

        if (!interfacePermissionData) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/interfacePermission/addInterfacePermission",
            type: "post",
            data: {"interfacePermissionData": JSON.stringify(interfacePermissionData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddInterfacePermissionSubPage', 'bgdiv');
            context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.editInterfacePermissionBtn = function (interfacePermissionId) {
        var request = $.ajax({
            url: "/myadmin/interfacePermission/getInterfacePermissionForId",
            data: {"interfacePermissionId": interfacePermissionId},
            async: false,
            type: "post"
        });

        var requestJSON = JSON.parse(request.responseText);
        if (requestJSON["code"] !== 10000) {
            alert("接口具有权限查询错误，请联系管理员");
            return;
        }

        var requestBody = requestJSON["body"];
        $("#permissionName").val(requestBody["permissionName"]);
        $("#permissionKey").val(requestBody["permissionKey"]);
        $("#url").val(requestBody["url"]);
        $("#permission").val(requestBody["permission"]);
        $("#isDefault").val(requestBody["isDefault"]);
        $("#submit").attr("onclick", "editInterfacePermission('" + interfacePermissionId + "')");

        // for (var permissionKeyIndex in permissionKeysRequestBody) {
        //     $("#permission").append('<option value="' + permissionKeysRequestBody[permissionKeyIndex] + '">' + permissionKeysRequestBody[permissionKeyIndex] + '</option>');
        // }
        var htmlobjPermissionKey = $("#permission").find("option");
        htmlobjPermissionKey.each(function () {
            if($(this).text() === requestBody["permission"]){
                $(this).attr("selected",true);
            }
        });
        var htmlobjIsDefault = $("#isDefault").find("option");
        htmlobjIsDefault.each(function () {
            if($(this).text() === requestBody["isDefault"]){
                $(this).attr("selected",true);
            }
        });
        $('.select2').select2();
        context.openDiv('adminAddInterfacePermissionSubPage', 'bgdiv', '编辑接口权限');
    };

    context.editInterfacePermission = function (interfacePermissionId) {
        var interfacePermissionData = context.getPageInterfacePermissionData();
        if (!interfacePermissionData) {
            return;
        }
        interfacePermissionData["id"] = interfacePermissionId;
        var ajaxRequest = $.ajax({
            url: "/myadmin/interfacePermission/editInterfacePermission",
            type: "post",
            data: {"interfacePermissionData": JSON.stringify(interfacePermissionData)},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.CloseDiv('adminAddInterfacePermissionSubPage', 'bgdiv');
             context.ReloadPage();
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.deleteInterfacePermissionBtn = function (element, interfacePermissionId) {
        if (!confirm("确认删除 [" + $("#url_" + interfacePermissionId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/interfacePermission/delInterfacePermission",
            type: "post",
            data: {"interfacePermissionId": interfacePermissionId},
            async: false
        });
        var request = JSON.parse(ajaxRequest.responseText);
        if (request["code"] === 10000) {
            context.selected();
        } else {
            alert("错误 " + request["code"] + ":" + request["message"]);
        }
    };

    context.resetInterfacePermissionBtn = function (element, interfacePermissionId) {
        if (!confirm("确认启用 [" + $("#url_" + interfacePermissionId).text() + "]  ?")) {
            return;
        }
        var ajaxRequest = $.ajax({
            url: "/myadmin/interfacePermission/resetInterfacePermission",
            type: "post",
            data: {"interfacePermissionId": interfacePermissionId},
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
        if(e.keyCode === 13) {
            context.queryRequest();
        }
    };


    context.queryRequest = function () {
        checkArr.url = $("#queryUrl").val();
        checkArr.permissionKey = $("#queryPermissionKey").val();
        var queryHtml = '<span style="font-size: 15px;float:left;padding-top: 4px;margin-right: 10px">搜索条件:</span>';

        for (var index in checkArr) {
            if (checkArr[index] === "") {
                continue;
            }

            var key = "";
            if (index === "url") {
                key = "接口";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }

            if (index === "permissionKey") {
                key = "接口具有权限";
                queryHtml += '<span class="tag" onclick="delQuery(\'' + index + '\')"><span>' + key + '：' + checkArr[index] + '&nbsp;&nbsp;</span><span class="fa fa-fw fa-close"></span></span>';
            }
        }

        $("#queryStyle").html(queryHtml);

        context.selected();
    };

    context.delQuery = function (condition) {
        if (condition === "url") {
            $("#queryUrl").val("");
        }

        if (condition === "permissionKey") {
            $("#queryPermissionKey").val("");
        }
        context.queryRequest();
    };


})(window);
window.selected();


$(function () {
    //Initialize Select2 Elements
    $('.select2').select2();

});