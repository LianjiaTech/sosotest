"use strict";
var page = 1;
var checkArr = {};
var orderBy = "t.state desc, t.id desc";
(function (context) {

    var teamId = getUrlParam("teamId");
    context.selected = function () {
        var data = {checkArr: encodeURI(JSON.stringify(checkArr)), orderBy: orderBy, page: page, teamId:teamId};
        var htmlobj = $.ajax({url: "/myadmin/userRole/getUserRoleSubPage", async: false, type: "post", data: data});
        $("#userRoleSubPage").html(htmlobj.responseText);
    };

    context.pageCall = function (pageNum) {
        page = pageNum;
        context.selected();
    };

    context.ReloadPage = function(){
        location.reload();
    };

    context.setTeamLeaderBtn = function (element,loginName) {
        var data = {"loginName": loginName, "teamId":teamId}
        var request = $.ajax({url: "/myadmin/userRole/setTeamLeader", data: data, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        var requestBody = requestJSON["body"];
        if (requestJSON["code"] === 10011) {
            alert("组长不能撤销自己，请联系管理员");
            return;
        }else if (requestJSON["code"] !== 10000) {
            alert("操作错误，请联系管理员");
            return;
        }


        var state= requestBody["state"]

        if (state === 1){
            element.css("display","none");
            element.next().css("display","");

        }else if(state === 0){
            element.css("display","none");
            element.prev().css("display","");
        }

    };


    context.delTeamLeaderBtn = function (element,loginName) {
        var data = {"loginName": loginName, "teamId":teamId}
        var request = $.ajax({url: "/myadmin/userRole/delTeamLeader", data: data, async: false, type: "post"});

        var requestJSON = JSON.parse(request.responseText);
        var requestBody = requestJSON["body"];
        if (requestJSON["code"] === 10011) {
            alert("组长不能撤销自己，请联系管理员");
            return;
        }else if (requestJSON["code"] !== 10000) {
            alert("操作错误，请联系管理员");
            return;
        }


        var state= requestBody["state"]

        if (state === 1){
            element.css("display","none");
            element.next().css("display","");

        }else if(state === 0){
            element.css("display","none");
            element.prev().css("display","");
        }

    };



})(window);
window.selected();


