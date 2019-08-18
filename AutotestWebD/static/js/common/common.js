String.prototype.startWith=function(str){
  var reg=new RegExp("^"+str);
  return reg.test(this);
};

String.prototype.endWith=function(str){
  var reg=new RegExp(str+"$");
  return reg.test(this);
};

//js获取请求的url中的参数
function getUrl() {
    return this.location.href.split(this.location.host)[1].split("?")[0];
}
function getParam(paramName) {
    paramValue = "", isFound = !1;
    if (this.location.search.indexOf("?") == 0 && this.location.search.indexOf("=") > 1) {
        arrSource = unescape(this.location.search).substring(1, this.location.search.length).split("&"), i = 0;
        while (i < arrSource.length && !isFound) arrSource[i].indexOf("=") > 0 && arrSource[i].split("=")[0].toLowerCase() == paramName.toLowerCase() && (paramValue = arrSource[i].split("=")[1], isFound = !0), i++
    }
    return paramValue == "" && (paramValue = null), paramValue
}
$(document).keydown(function(event){
    //监听 ctrl + S 保存
    var keyCode = event.keyCode || event.which || event.charCode;
    var ctrlKey = event.ctrlKey || event.metaKey;
    if(ctrlKey && keyCode == 83) {
        var interfaceTestcaseUrlList = [
            "/dubbo/interfaceAddPage",
            "/dubbo/operationInterface",
            "/dubbo/testCaseAddPage",
            "/dubbo/operationTestCase",
            "/interfaceTest/HTTP_InterfaceAddPage",
            "/interfaceTest/HTTP_operationInterface",
            "/interfaceTest/HTTP_TestCaseAddPage",
            "/interfaceTest/HTTP_operationTestCase",
        ];
        if(interfaceTestcaseUrlList.indexOf(getUrl()) > -1){
            var paramOption = getParam("option");
            if( paramOption === "edit"){
                saveOrDebug('edit');
            }else if(paramOption === "copy" || paramOption === null || paramOption === "" || paramOption === "addbymock"){
                saveOrDebug('save');
            }
        }

        var taskUrlList = [
            "/dubbo/TaskAddPage",
            "/dubbo/operationTask",
            "/interfaceTest/HTTP_TaskAddPage",
            "/interfaceTest/HTTP_operationTask",
        ];
        if(taskUrlList.indexOf(getUrl()) > -1){
            saveTask();
        }

        var taskSuiteUrlList = [
            "/dubbo/TaskSuiteAddPage",
            "/dubbo/operationTaskSuite",
            "/interfaceTest/HTTP_TaskSuiteAddPage",
            "/interfaceTest/HTTP_operationTaskSuite",
        ];
        if(taskSuiteUrlList.indexOf(getUrl()) > -1){
            saveTaskSuite();
        }

        var datakeywordUrlList = [
            "/datakeyword/addPage",
            "/datakeyword/operationCheck",
        ];
        if(datakeywordUrlList.indexOf(getUrl()) > -1){
            var paramOption = getParam("option");
            if( paramOption === "edit"){
                saveOrDebug('edit');
            }else{
                saveOrDebug('save');
            }
        }

        var httpmockUrlList = [
            "/mockserver/HTTP_InterfaceAddPage",
            "/mockserver/HTTP_operationInterface",
        ];
        if(httpmockUrlList.indexOf(getUrl()) > -1){
            var paramOption = getParam("option");
            if( paramOption === "edit"){
                saveOrDebug('edit');
            }else{
                saveOrDebug('save');
            }
        }

        event.preventDefault(); //反之浏览器的ctrl S 弹出
    }
});
//获取key列表，比如 $GVAR[abc] $GVAR[def],返回[abc,def]
function getKeyList(strToBeProcessed,startTag,endTag){
    var proList = strToBeProcessed.split(startTag);
    var keyList = [];
    for(var index=1; index < proList.length; index++ ){
        var tmpStr = proList[index];
        var tmpEndPos = tmpStr.indexOf(endTag);
        if(tmpEndPos > 0){
            var tmpVarkey = tmpStr.substring(0,tmpEndPos);
            var tmpVarkeyTrimed = tmpVarkey.trim();
            keyList.push(tmpVarkeyTrimed);
        }
    }
    return keyList;
}
//渲染gvar text等div的html。
function renderDivByData(data,renderDivId) {
    var commonValBeforeInputLinkDivInnerHtml = "";

    var gvarStartTagList = ["$GVAR[","gvar("];
    var gvarEndTagList = ["]",")"];
    for(var tagIndex=0; tagIndex<gvarStartTagList.length; tagIndex++){
        var startTag = gvarStartTagList[tagIndex];
        var endTag = gvarEndTagList[tagIndex];
        var keylist = getKeyList(data,startTag,endTag);
        for(var index = 0; index < keylist.length; index++ ){
            commonValBeforeInputLinkDivInnerHtml += '<a href="/interfaceTest/HTTP_GlobalVarsConf?key='+keylist[index].replace(/\"/g,"").replace(/\'/g,"")+'" target="_blank">'+startTag+keylist[index]+endTag+'</a> &nbsp;&nbsp;';
        }
    }
    var textStartTagList = ["$TEXT[","$IMPORT[","$RUNFUNC[","text("];
    var textEndTagList = ["]","]","]",")"];
    for(var tagIndex=0; tagIndex<textStartTagList.length; tagIndex++) {
        var startTag = textStartTagList[tagIndex];
        var endTag = textEndTagList[tagIndex];
        var keylist = getKeyList(data, startTag, endTag);
        for (var index = 0; index < keylist.length; index++) {
            commonValBeforeInputLinkDivInnerHtml += '<a href="/interfaceTest/HTTP_GlobalTextConf?key=' + keylist[index].replace(/\"/g,"").replace(/\'/g,"") + '" target="_blank">' + startTag + keylist[index] + endTag + '</a> &nbsp;&nbsp;';
        }
    }
    var textStartTagList = ["EXECUTE_INTERFACE(","execute_interface("];
    var textEndTagList = [")",")"];
    for(var tagIndex=0; tagIndex<textStartTagList.length; tagIndex++) {
        var startTag = textStartTagList[tagIndex];
        var endTag = textEndTagList[tagIndex];
        var keylist = getKeyList(data, startTag, endTag);
        for (var index = 0; index < keylist.length; index++) {
            commonValBeforeInputLinkDivInnerHtml += '<a href="/interfaceTest/HTTP_operationInterfaceByInterfaceId?option=check&interfaceId=' + keylist[index].split(",")[0].replace(/\"/g,"").replace(/\'/g,"") + '" target="_blank">' + startTag + keylist[index].split(",")[0] + endTag + '</a> &nbsp;&nbsp;';
        }
    }
    var textStartTagList = ["EXECUTE_DUBBO_INTERFACE(","execute_dubbo_interface("];
    var textEndTagList = [")",")"];
    for(var tagIndex=0; tagIndex<textStartTagList.length; tagIndex++) {
        var startTag = textStartTagList[tagIndex];
        var endTag = textEndTagList[tagIndex];
        var keylist = getKeyList(data, startTag, endTag);
        for (var index = 0; index < keylist.length; index++) {
            commonValBeforeInputLinkDivInnerHtml += '<a href="/dubbo/operationInterfaceByInterfaceId?option=check&interfaceId=' + keylist[index].split(",")[0].replace(/\"/g,"").replace(/\'/g,"") + '" target="_blank">' + startTag + keylist[index].split(",")[0] + endTag + '</a> &nbsp;&nbsp;';
        }
    }

    var textStartTagList = ["imports("];
    var textEndTagList = [")"];
    for(var tagIndex=0; tagIndex<textStartTagList.length; tagIndex++) {
        var startTag = textStartTagList[tagIndex];
        var endTag = textEndTagList[tagIndex];
        var keylist = getKeyList(data, startTag, endTag);
        for (var index = 0; index < keylist.length; index++) {
            commonValBeforeInputLinkDivInnerHtml += '<a href="/datakeyword/operationCheckByKey?option=check&type=PYTHON_CODE&key=' + keylist[index].replace(/\"/g,"").replace(/\'/g,"") + '" target="_blank">' + startTag + keylist[index] + endTag + '</a> &nbsp;&nbsp;';
        }
    }
    $("#"+renderDivId).html(commonValBeforeInputLinkDivInnerHtml);
}