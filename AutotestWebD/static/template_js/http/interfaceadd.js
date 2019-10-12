
var commonValBeforeInputEditor = null;
var commonValAfterInputEditor = null;

function useCustomToggle() {
    if ($("#useCustomUri").prop("checked")){
        $("#useCustomUri").prop("checked",false);
        $("#useCustomUriBtn").html('使用自定义地址<i class="fa fa-hand-o-right"></i>');
    }else {
        $("#useCustomUri").prop("checked",true);
        $("#useCustomUriBtn").html('<i class="fa fa-hand-o-left"></i>使用服务配置地址');
    }
}

function initAllEditor(){

    //readOnly:'nocursor',
    commonValBeforeInputEditor = CodeMirror.fromTextArea($("#commonValBeforeInput")[0], {
        lineNumbers: true,
        matchBrackets: true,
        mode: "text/x-python",
        indentUnit: 4,
        indentWithTabs: false,
    });
    commonValBeforeInputEditor.on("focus",function(editor,change){
        resetGlobalElement($("#commonValBeforeInput"),commonValBeforeInputEditor);
    });
    commonValBeforeInputEditor.on("blur",function(editor,change){
        // commonValBeforeInputEditor.setValue(commonValBeforeInputEditor.getValue().trim().replace("\t","    "));
        renderDivByData(commonValBeforeInputEditor.getValue(),"commonValBeforeInputLinkDiv");
    });
    commonValBeforeInputEditor.setOption("extraKeys", {
        Tab: newTab
    });
    commonValAfterInputEditor = CodeMirror.fromTextArea($("#commonValAfterInput")[0], {
        lineNumbers: true,
        matchBrackets: true,
        mode: "text/x-python",
        indentUnit: 4,
        indentWithTabs: false,
    });
    commonValAfterInputEditor.on("focus",function(editor,change){
        resetGlobalElement($("#commonValAfterInput"),commonValAfterInputEditor);
    });
    commonValAfterInputEditor.on("blur",function(editor,change){
        // commonValAfterInputEditor.setValue(commonValAfterInputEditor.getValue().trim().replace("\t","    "));
        renderDivByData(commonValAfterInputEditor.getValue(),"commonValAfterInputLinkDiv");
    });
    commonValAfterInputEditor.setOption("extraKeys", {
        Tab: newTab
    });

    if( optionFromContext === "check"){
        commonValBeforeInputEditor.setOption("readOnly", true);
        commonValAfterInputEditor.setOption("readOnly", true);
    }
}

$("#sources").select2();
$("#caselevel").select2();
$("#methodSelect").select2();

function initJudgeVersion() {
     if ( requestSessionVersion !== "CurrentVersion"){
         alert("现在为历史版本页面");
     }
}

initJudgeVersion();

var businessLine_module_relation = $.ajax({
              url: bmRelationUrl ,
              type: 'get',
              async: false,
         });
try{
    var bmDict = JSON.parse(businessLine_module_relation.responseText).body;
}catch (e){
    alert(bmDict);
    alert("获取业务线模块关联失败")
}

switchModule($("#businessLine").val());

function switchModule(blId) {
    $("#modules option").remove();
    var mdSelect = $("#modules");
    for(var index = 0; index < bmDict[blId].length;index ++){
        jQuery("<option></option>").val(bmDict[blId][index]["id"]).text(bmDict[blId][index]["moduleName"]).appendTo(mdSelect);
    }
    $("#businessLine").select2();
    $("#modules").select2();
}

var checkResultId = 0;
var data = {};

function toggleUrlEncode(element,tableName) {
    if(element.text()=="原始"){
        element.parent().parent().parent().parent().css("display","none");
        element.parent().parent().parent().parent().next().css("display","block");
        var tableData = tableDataTourlencode(tableName);
        element.parent().parent().parent().parent().next().children().val(tableData);
    }else {
        element.parent().css("display","none");
        element.parent().prev().attr("style","table-layout: fixed;");
        tableInitList(tableName,urlencodeToList(element.next().val()));
    }
}

function formDataTabInit(jsonModel) {
    for(var i = 0 ; i < jsonModel.length ; i++){
        addTableTr($("#body-form-Tbody"));
        var element = $("[name='body-form-Tr']").eq(i);
        var elementKeyTd = element.children().eq(0).children();
        var elementValueTd = element.children().eq(1).children();
        elementKeyTd.eq(0).val(jsonModel[i]["key"]);
        elementKeyTd.eq(1).val(jsonModel[i]["type"]);

        formDataInput_file( element.children().eq(0).children().eq(1));
        if(jsonModel[i]["type"] == "text"){
            elementValueTd.eq(0).val(jsonModel[i]["value"]);
        }else{
            elementValueTd.eq(2).children().eq(1).val(jsonModel[i]["value"]["showPath"]);
            elementValueTd.eq(2).children().eq(2).text(JSON.stringify(jsonModel[i]["value"]));
        }

    }
}

function tableInit(elementName,jsonModel) {
    if(JSON.stringify(jsonModel) != "{}") {
        var i = 0;
        for (var key in jsonModel) {
            if (i == ($("[name='" + elementName + "Tr']").length - 1)) {
                addTableTr($("#" + elementName + "Tbody"));
            }
            var element = $("[name='" + elementName + "Tr']").eq(i).find('td');
            var headerKey = element.eq(0).children();
            var headerValue = element.eq(1).children().eq(0);
            headerKey.val(key);
            headerValue.val(jsonModel[key]);
            if(key != "" || jsonModel[key] != ""){
                 i++;
            }
        }
        var htmlElement = $("[name='" + elementName + "Tr']");
        for(var j=0;j<htmlElement.length;j++){
            if(j > i){
                htmlElement.eq(j-1).remove();
            }
        }

    }else {
        var htmlElement = $("[name='" + elementName + "Tr']");
        for(var i=0;i<htmlElement.length-1;i++){
            htmlElement.eq(i).remove();
        }
    }
}

function tableInitList(elementName,urlencodeList) {
    for(var i=0;i<urlencodeList.length;i++){
         if (i == ($("[name='" + elementName + "Tr']").length - 1)) {
                addTableTr($("#" + elementName + "Tbody"));
            }
         var element = $("[name='" + elementName + "Tr']").eq(i).find('td');
         var headerKey = element.eq(0).children();
         var headerValue = element.eq(1).children().eq(0);
        headerKey.val(urlencodeList[i][0]);
        headerValue.val(urlencodeList[i][1]);
    }
    $("#debugSug").attr("disabled",false);
    $("[data-id='debugSug']").attr("class","btn dropdown-toggle btn-default bs-placeholder");
}

function loadFile(element) {
    var file = element[0].files[0];
    if (file.size > 1024*1024) {
        alert("文件大小不能超过1M");
        element.val('');
        return false;
    }
    element.parent().next().val(element.val());
    element.parent().next().next().text('');

}

function addTableTr(element) {
        var lastElement = element.children().last();
        var lastElementHtml = lastElement.prop("outerHTML");
        lastElement.after(lastElementHtml);
        tableStyle(element)
    }

function tableStyle(element) {
    var elementList = element.children();
    for(var i=0;i<elementList.length;i++){
        var elementInput = elementList.eq(i).find("input");
        if(i != (elementList.length - 1)){
             elementInput.css("background-color", "");
             elementInput.attr("onclick", "");
             elementList.eq(i).find("button").css("display", "block");
             elementList.eq(i).find("select").attr("disabled", false);
             elementList.eq(i).find("select").css("background-color", "");
        }else {
             elementInput.css("background-color", "rgb(183, 186, 189)");
             elementList.eq(i).find("button").css("display", "none");
             elementList.eq(i).find("select").css("background-color", "rgb(183, 186, 189)");
             elementList.eq(i).find("select").attr("disabled", true);
        }
    }
}

function clickBodyRadio() {
    var checkedRadio =  $("input[name='body']:checked").val();
    if (checkedRadio == "none"){
        $("#body-none").css("display","block");
        $("#body-form-data").css("display","none");
        $("#body-x-www-form-urlencoded").css("display","none");
        $("#body-raw-select").css("display","none");
        $("#body-raw").css("display","none");
        $("#body-binary").css("display","none");
    }else if (checkedRadio == "form-data"){
        $("#body-none").css("display","none");
        $("#body-form-data").css("display","block");
        $("#body-x-www-form-urlencoded").css("display","none");
        $("#body-raw-select").css("display","none");
        $("#body-raw").css("display","none");
        $("#body-binary").css("display","none");
    }else if(checkedRadio == "x-www-form-urlencoded"){
        $("#body-none").css("display","none");
        $("#body-x-www-form-urlencoded").css("display","block");
        $("#body-form-data").css("display","none");
        $("#body-raw-select").css("display","none");
        $("#body-raw").css("display","none");
        $("#body-binary").css("display","none");
    }else if(checkedRadio == "raw"){
        $("#body-none").css("display","none");
        $("#body-raw-select").css("display","block");
        $("#body-raw").css("display","block");

        $("#body-x-www-form-urlencoded").css("display","none");
        $("#body-form-data").css("display","none");
        $("#body-binary").css("display","none");
    }else {
        $("#body-none").css("display","none");
        $("#body-raw-select").css("display","none");
        $("#body-raw").css("display","none");

        $("#body-x-www-form-urlencoded").css("display","none");
        $("#body-form-data").css("display","none");
        $("#body-binary").css("display","block");
    }

}

function formDataInput_file(element) {
    if(element.val() == "text"){
        element.parent().next().find("input").eq(0).css("display","block");
        element.parent().next().find("div").css("display","none");
        element.parent().next().find("button").css("margin-top","-32.5px")
    }else{
        element.parent().next().find("div").css("display","block");
        element.parent().next().find("input").eq(0).css("display","none");
        element.parent().next().find("button").css("margin-top","2px")
    }
}


function tableDataToDict(tabName) {
    var tableTr = $("[name='"+tabName+"Tr']");
    var tableJson = {};
    if(tableTr.length!=0){
        for(var i = 0;i < tableTr.length; i++){
            if(tableTr.eq(i).find("td").eq(0).children().val().trim() == "" && tableTr.eq(i).find("td").eq(1).children().val().trim() == ""){
                continue;
            }
            tableJson[tableTr.eq(i).find("td").eq(0).children().val().trim()] = tableTr.eq(i).find("td").eq(1).children().val().trim()
        }
    }
    return tableJson;
}

function tableDataTourlencode(tabName) {
    var tableTr = $("[name='"+tabName+"Tr']");
    var tableStr = "";
    if(tableTr.length!=0){
        for(var i = 0;i < tableTr.length; i++){
            if(tableTr.eq(i).find("td").eq(0).children().val().trim() == "" && tableTr.eq(i).find("td").eq(1).children().val().trim() == ""){
                continue;
            }
            tableStr += tableTr.eq(i).find("td").eq(0).children().val().trim()+"="+tableTr.eq(i).find("td").eq(1).children().val().trim();
            if(i != (tableTr.length-2)){
                tableStr += "&";
            }
        }
    }
    return tableStr;
}


function changeHeader(codeType) {
    var headerJson = tableDataToDict("header");
    if(codeType == "" || codeType == "Text"){
        if(headerJson["Content-Type"]){
            delete headerJson["Content-Type"];
        }
    }else{
        headerJson["Content-Type"] = codeType
    }
    tableInit("header",headerJson);
    $("[href='#headerTab']").text("HEADER("+($("[name='headerTr']").length-1)+")")

}

function changeBodyTab(method) {
    if(method == "GET" || method == "HEAD"){
         $("[href='#bodyTab']").parent().css("display","none");
         $("[href='#paramsTab']").click();
    }else {
         $("[href='#bodyTab']").parent().css("display","block");
         $("[href='#bodyTab']").click();
    }

}

function changeSelectWidth(codeType) {
    switch (codeType.val()) {
        case "Text":
            codeType.css("width","80px");
            break;
        case "text/plain":
            codeType.css("width","150px");
            break;
        case "application/json":
            codeType.css("width","200px");
            break;
        case "application/javascript":
            codeType.css("width","260px");
            break;
        case "application/xml":
            codeType.css("width","200px");
            break;
        case "text/xml":
            codeType.css("width","150px");
            break;
        case "text/html":
            codeType.css("width","150px");
            break;
    }
}

function urlencodeToList(str) {
    if(str == ""){
        return []
    }
    var strList = str.split("&");
    var retList = [];
    for (var s in strList){
        var sp = strList[s].split("=");
        if(sp.length == 1){
            retList.push(["",sp[0]])
        }else {
            var strText = "";
            for(var i = 1;i<sp.length;i++){
                if(i == sp.length -1){
                    strText = strText + sp[i]
                }else {
                    strText = strText+ sp[i]+"="
                }
            }
            retList.push([sp[0],strText])
        }
    }
    return retList;
}

function urlencodeToDict(str) {
    var strList = str.split("&");
    var strdict = {};
    for (var s in strList){
        var sp = strList[s].split("=");
        strdict[sp[0]] = sp[1]
    }
    return strdict;
}

function dataInit() {
    $("#URI").select2();
    $("#redirectSelect").select2();
    if (optionFromContext != "add" && optionFromContext != "addbymock") {
        if (optionFromContext == "check" || optionFromContext == "caseCheck") {
            $("[type='text']").attr("disabled", true);
            $("select").attr("disabled", true);
            $("input").attr("onclick", "");
            $("input").attr("disabled", true);
            $("[type='radio']").attr("disabled", true);
        }

        $("#preTab").children().eq(0).attr("class","");
        $("#preTab").children().eq(0).attr("class","active");
        $("#preTabContent").children().eq(0).attr("class","tab-pane fade");
        $("#preTabContent").children().eq(0).attr("class","tab-pane fade active in");

        $("#interfaceTab").children().eq(0).attr("class","");
        $("#interfaceTab").children().eq(0).attr("class","active");
        $("#interfaceTabContent").children().eq(0).attr("class","tab-pane fade");
        $("#interfaceTabContent").children().eq(0).attr("class","tab-pane fade active in");

        $("#afterTab").children().eq(0).attr("class","");
        $("#afterTab").children().eq(0).attr("class","active");
        $("#afterTabContent").children().eq(0).attr("class","tab-pane fade");
        $("#afterTabContent").children().eq(0).attr("class","tab-pane fade active in");

        var ajaxobj = $.ajax({
            url: getInterfaceDataForIdUrl + "?id="+getInterfaceDataForIdUrlId, type: "GET", success: function () {
                data = JSON.parse(JSON.parse(ajaxobj.responseText).body);
                $("#interfaceId").val(data["interfaceId"]);
                $("#name").val(data["title"]);
                $("#describe").val(data["casedesc"]);
                $("#businessLine").val(data["businessLineId_id"]).change();
                switchModule($("#businessLine").val());
                try {
                    $("#modules").val(data["moduleId_id"]);
                }catch (e){

                }
                $("#modules").select2();
                $("#sources").val(data["sourceId_id"]);
                $("#sources").select2();
                $("#caselevel").children().each(function () {
                    if ($(this).val() == data["caselevel"]) {
                        $(this).attr("selected", true);
                        $("#caselevel").select2();
                    }
                });
                $("#timeout").val(data.timeout);
                $("#performanceTime").val(data.performanceTime);
                $("#redirectSelect").val(data["urlRedirect"]);
                $("#redirectSelect").select2();
                $("#URI").val(data["uri"]);
                $("#URI").select2();
                $("#customUri").val(data["customUri"]);
                if (data["useCustomUri"] === 0){
                    $("#useCustomUri").prop("checked",true);
                    $("#useCustomUriBtn").html('<i class="fa fa-hand-o-left"></i>使用服务配置地址');
                }else {
                    $("#useCustomUri").prop("checked",false);
                    $("#useCustomUriBtn").html('使用自定义地址<i class="fa fa-hand-o-right"></i>');
                }

                $("#commonValBeforeInput").val(data["varsPre"]);
                renderDivByData(data["varsPre"],"commonValBeforeInputLinkDiv");

                $("#URL").val(data["url"]);
                $("#methodSelect").children().each(function () {
                    if ($(this).val() == data["method"]) {
                        $(this).attr("selected", true);
                        $("#methodSelect").select2();
                    }
                });
                tableInit("header",JSON.parse(data["header"]));
                changeBodyTab(data["method"]);
                $("[href='#headerTab']").text("HEADER("+($("[name='headerTr']").length-1)+")");
                var parameter = $("#parameter");
                var paramsFlag = 0;
                var paramsList = urlencodeToList(data["params"]);
                for (var paramsIndex = 0;paramsIndex<paramsList.length;paramsIndex++){
                    if (paramsList[paramsIndex][0] == "" || paramsList[paramsIndex][1] == ""){
                        paramsFlag = 1;
                        break;
                    }
                }
                if (paramsFlag == 0){
                    tableInitList("params",urlencodeToList(data["params"]));
                }else {
                    parameter.parent().parent().children().eq(0).css("display", "none");
                    parameter.parent().parent().children().eq(1).css("display", "block");
                    parameter.val(data["params"]);
                }
                if (data["bodyType"]){
                    $("input:radio[value="+data["bodyType"]+"]").attr("checked",true);
                    clickBodyRadio();

                    switch (data["bodyType"] ){
                        case "none":
                            break;
                        case "x-www-form-urlencoded":
                            var urlencodedFlag = 0;
                            var urlencodedList = urlencodeToList(data["bodyContent"]);
                            for (var urlencodedIndex = 0;urlencodedIndex<urlencodedList.length;urlencodedIndex++){
                                if (urlencodedList[urlencodedIndex][0] == "" || urlencodedList[urlencodedIndex][1] == ""){
                                    urlencodedFlag = 1;
                                    break;
                                }
                            }
                            if (urlencodedFlag == 0){
                                tableInitList("x-www-form-urlencoded",urlencodeToList(data["bodyContent"]));
                            }else {
                                var urlencoded = $("#x-www-form-urlencoded-input");
                                urlencoded.parent().parent().children().eq(0).css("display", "none");
                                urlencoded.parent().parent().children().eq(1).css("display", "block");
                                urlencoded.val(data["bodyContent"]);
                            }
                            break;
                        case "raw":
                            var header = JSON.parse(data["header"]);
                            if("Content-Type" in header){
                                $("#headerSelected").children().each(function () {
                                    if($(this).val() == header["Content-Type"]){
                                        $("#headerSelected").val(header["Content-Type"]);
                                        changeSelectWidth($("#headerSelected"));
                                    }
                                })
                            }
                            $("#body-raw-input").val(data["bodyContent"]);
                            break;
                        case "binary":
                            $("#binarySpan").text(data["bodyContent"])
                            $("#textName").val(JSON.parse(data["bodyContent"])["showPath"])
                            break;
                        case "form-data":
                            try{
                                var bodyDict = JSON.parse(data["bodyContent"]);
                                formDataTabInit(bodyDict);
                            }catch (err){
                                console.log('data["bodyContent"]::' + data["bodyContent"]);
                            }
                            break
                    }

                }

                $("#commonValAfterInput").val(data["varsPost"]);
                renderDivByData(data["varsPost"],"commonValAfterInputLinkDiv");
                initAllEditor();
            }
        });

    }
    else if (getUrlParam("dataKey") !== null){
        // if (interfaceAutoFillKey !== ""){
        //     var htmlobj = $.ajax({url:HTTP_InterfaceGetAutoFillDataUrl+"?interfaceAutoFillKey="+interfaceAutoFillKey,async:false});
            var htmlobj = $.ajax({url:HTTP_InterfaceGetAutoFillDataUrl+"?dataKey="+getUrlParam("dataKey"),async:false});
            try{
                var paramsData = JSON.parse(JSON.parse(htmlobj.responseText)["body"]);
                $("#methodSelect").find("option[value='" + paramsData["method"] + "']").prop("selected", true).change();
                //http://127.0.0.1:8000/env/?id=1
                var urlList = paramsData["url"].split("?"); //http://127.0.0.1:8000/env/    和  id=1
                var httpsOrHttpList = urlList[0].split("://") // http  和 127.0.0.1:8000/env/
                var urlSplitList = httpsOrHttpList[1].split("/");//127.0.0.1:8000  和 env ...
                var uriHost = httpsOrHttpList[0] +"://"+urlSplitList[0]; //拼接出 http://127.0.0.1:8000
                var uriConfResp = $.ajax({
                  url: HTTP_getUrikeyByConfigInfoUrl + '?host='+uriHost ,
                  async: false
                });

                $("#customUri").val(data["customUri"]);
                $("#useCustomUri").prop("checked",false);

                $("#URI").val(uriConfResp.responseText);
                $("#URI").select2();
                var url = "";
                for(var i = 1;i < urlSplitList.length;i++){
                        url = url + "/" + urlSplitList[i]
                }
                $("#name").val("[自动录制] "+url);
                $("#describe").val("[自动录制] "+url);

                $("#URL").val(url);
                if (urlList.length > 1){
                    var paramList = urlencodeToList(urlList[1]);
                    for(var index = 0 ;index < paramList.length;index ++){
                        if ($("#commonValBeforeInput").val() === ""){
                            $("#commonValBeforeInput").val("param_" + paramList[index][0] +"="+ paramList[index][1]+";");
                        }else{
                            $("#commonValBeforeInput").val($("#commonValBeforeInput").val() + "\nparam_" + paramList[index][0] +"="+ paramList[index][1]+";");
                        }
                        paramList[index][1] = "$VAR[param_" + paramList[index][0] + "]";
                    }
                    tableInitList('params',paramList);
                }

                var contentTypeFromHeader = "";
                for(var headerIndex = 0; headerIndex < paramsData["headers"].length; headerIndex ++){
                    try {
                        contentTypeFromHeader = paramsData["headers"][headerIndex]["Content-Type"];
                    }catch(e){ }
                }
                if(contentTypeFromHeader.startsWith("multipart/form-data")){
                    //form data类型的，header为空即可。
                    if(paramsData.hasOwnProperty("postData")){
                        var prePostData = paramsData["postData"];
                        var mimeType = '';
                        if (prePostData.hasOwnProperty("mimeType")){
                            mimeType = prePostData["mimeType"];
                        }
                        if (mimeType.startsWith("multipart/form-data")){
                            //x-www-form-urlencoded   key value模式的
                            $("input:radio[name='body']").eq(0).click();
                            $("input:radio[name='body']").eq(0).click();
                            var paramsFromFormdata = [];
                            if (prePostData.hasOwnProperty("params")){
                                paramsFromFormdata = prePostData["params"];
                            }
                            var formdataBodyContentList = [];
                            //[{"key": "delType", "type": "text", "value": "1"}
                            for(var index = 0;index < paramsFromFormdata.length;index ++){
                                if ($("#commonValBeforeInput").val() === ""){
                                    $("#commonValBeforeInput").val("body_" + paramsFromFormdata[index]["name"] +"="+ decodeURIComponent(paramsFromFormdata[index]["value"])+";");
                                }else{
                                    $("#commonValBeforeInput").val($("#commonValBeforeInput").val() + "\nbody_" + paramsFromFormdata[index]["name"] +"="+ decodeURIComponent(paramsFromFormdata[index]["value"])+";");
                                }
                                var tmpFormDataValue = {};
                                tmpFormDataValue['key'] = paramsFromFormdata[index]['name'];
                                tmpFormDataValue['value'] = "$VAR[body_"+paramsFromFormdata[index]["name"]+"]";
                                tmpFormDataValue['type'] = 'text';
                                formdataBodyContentList.push(tmpFormDataValue);
                            }
                            formDataTabInit(formdataBodyContentList);
                        }
                    }
                }else{
                    //其他类型的，不需要处理间隔符
                    tableInit("header",paramsData["headers"][0]);
                    $("[href='#headerTab']").text("HEADER("+($("[name='headerTr']").length-1)+")");
                    if(paramsData.hasOwnProperty("postData")){
                        var prePostData = paramsData["postData"];
                        var mimeType = '';
                        if (prePostData.hasOwnProperty("mimeType")){
                            mimeType = prePostData["mimeType"];
                        }
                        if (mimeType.indexOf("x-www-form-urlencoded")>-1 && prePostData.hasOwnProperty("params")){
                            //x-www-form-urlencoded   key value模式的
                            var postData = prePostData["params"];
                            var paramsList = [];
                            for(var index = 0;index < postData.length;index ++){
                                if ($("#commonValBeforeInput").val() === ""){
                                    $("#commonValBeforeInput").val("body_" + postData[index]["name"] +"="+ decodeURIComponent(postData[index]["value"])+";");
                                }else{
                                    $("#commonValBeforeInput").val($("#commonValBeforeInput").val() + "\nbody_" + postData[index]["name"] +"="+ decodeURIComponent(postData[index]["value"])+";");
                                }
                                paramsList.push([postData[index]["name"],"$VAR[body_"+postData[index]["name"]+"]"]);
                            }
                            tableInitList('x-www-form-urlencoded',paramsList);
                        }else if(mimeType.indexOf("application/json")>-1 && prePostData.hasOwnProperty("text")){
                            $("input:radio[name='body']").eq(2).click();
                            clickBodyRadio();changeHeader(mimeType);
                            $("#headerSelected").val("application/json");
                            $("#body-raw-input").val(prePostData['text']);
                        }else if(mimeType.indexOf("text/plain")>-1 && prePostData.hasOwnProperty("text")){
                            $("input:radio[name='body']").eq(2).click();
                            clickBodyRadio();changeHeader(mimeType);
                            $("#headerSelected").val("text/plain");
                            $("#body-raw-input").val(prePostData['text']);
                        }else if(mimeType.indexOf("application/javascript")>-1 && prePostData.hasOwnProperty("text")){
                            $("input:radio[name='body']").eq(2).click();
                            clickBodyRadio();changeHeader(mimeType);
                            $("#headerSelected").val("application/javascript");
                            $("#body-raw-input").val(prePostData['text']);
                        }else if(mimeType.indexOf("application/xml")>-1 && prePostData.hasOwnProperty("text")){
                            $("input:radio[name='body']").eq(2).click();
                            clickBodyRadio();changeHeader(mimeType);
                            $("#headerSelected").val("application/xml");
                            $("#body-raw-input").val(prePostData['text']);
                        }else if(mimeType.indexOf("text/xml")>-1 && prePostData.hasOwnProperty("text")){
                            $("input:radio[name='body']").eq(2).click();
                            clickBodyRadio();changeHeader(mimeType);
                            $("#headerSelected").val("text/xml");
                            $("#body-raw-input").val(prePostData['text']);
                        }else if(mimeType.indexOf("text/html")>-1 && prePostData.hasOwnProperty("text")){
                            $("input:radio[name='body']").eq(2).click();
                            clickBodyRadio();changeHeader(mimeType);
                            $("#headerSelected").val("text/html");
                            $("#body-raw-input").val(prePostData['text']);
                        }

                    }
                }

                if(paramsData.hasOwnProperty("response")){
                    $("#commonValAfterInput").val("ASSERT("+paramsData["response"]+")");
                }
            }catch (e){
                alert(e);
                alert("参数解析失败，请检查参数或联系管理员");
            }finally {
                initAllEditor();
            }
        // }
    }
    else if (optionFromContext == "addbymock"){
        var ajaxobj = $.ajax({
            url: MOCK_getInterfaceDataForIdUrl+"?id=" + MOCK_getInterfaceDataForIdUrlMockId, type: "GET", success: function () {
                var data = JSON.parse(JSON.parse(ajaxobj.responseText).body);
                initInfosByMockData(data);
            }
        });
        initAllEditor();
    }
    else{
        initAllEditor();
    }
}

function initInfosByMockData(data){
    if(data.hasOwnProperty("title")){
        //有title证明是来自mock的，没有title来自报文
        $("#interfaceId").val("");
        $("#name").val(data["title"]);
    }
    if(data.hasOwnProperty("mockId")) {
        $("#describe").val("来自mockID：" + data["mockId"]);
    }
    if(data.hasOwnProperty("businessLineId")) {
        $("#businessLine").val(data["businessLineId"]).change();
        switchModule($("#businessLine").val());
    }
    if(data.hasOwnProperty("moduleId")) {
        try {
            $("#modules").val(data["moduleId"]);
        } catch (e) {

        }
        $("#modules").select2();
    }
    $("#timeout").val(20);
    $("#performanceTime").val(1);
    $("#URI").val(data["uriKey"]);
    $("#URI").select2();
    $("#URL").val(data["reqUrl"]);
    $("#methodSelect").children().each(function () {
        if ($(this).val() === data["reqMethod"]) {
            $(this).attr("selected", true);
        }
    });
    $("#methodSelect").select2();
    tableInit("header",JSON.parse(data["reqHeader"]));
    changeBodyTab(data["reqMethod"]);
    $("[href='#headerTab']").text("HEADER("+($("[name='headerTr']").length-1)+")");
    var parameter = $("#parameter");
    var paramsFlag = 0;
    var paramsList = urlencodeToList(data["reqParam"]);
    for (var paramsIndex = 0;paramsIndex<paramsList.length;paramsIndex++){
        if (paramsList[paramsIndex][0] == "" || paramsList[paramsIndex][1] == ""){
            paramsFlag = 1;
        }
    }
    if (paramsFlag == 0){
        tableInitList("params",urlencodeToList(data["reqParam"]));
    }else {
        parameter.parent().parent().children().eq(0).css("display", "none");
        parameter.parent().parent().children().eq(1).css("display", "block");
        parameter.val(data["reqParam"]);
    }

    var header = JSON.parse(data["reqHeader"]);
    var formdataBoundary = "";
    if (header.hasOwnProperty("Content-Type")){
        var contentType = header['Content-Type'];
        if(contentType.indexOf("x-www-form-urlencoded") > -1){
            data["bodyType"] = "x-www-form-urlencoded";
        }else if(contentType.indexOf("form-data") > -1){
            data["bodyType"] = "form-data";
            formdataBoundary = "--"+contentType.split("boundary=")[1];
        }else{
            data["bodyType"] = "raw";
        }
    }else if( data["reqBody"] === "" ){
        data["bodyType"] = "x-www-form-urlencoded";
    }else{
        try{
            JSON.parse(data["reqBody"]);
            data["bodyType"] = "raw";
        }catch(e){
            data["bodyType"] = "x-www-form-urlencoded";
        }
    }
    $("input:radio[value="+data["bodyType"]+"]").attr("checked",true);
    clickBodyRadio();
    switch (data["bodyType"] ){
        case "x-www-form-urlencoded":
            tableInitList("x-www-form-urlencoded",urlencodeToList(data["reqBody"]));
            break;
        case "raw":
            if("Content-Type" in header){
                $("#headerSelected").children().each(function () {
                    if($(this).val() == header["Content-Type"]){
                        $("#headerSelected").val(header["Content-Type"]);
                        changeSelectWidth($("#headerSelected"));
                    }
                })
            }
            $("#body-raw-input").val(data["reqBody"]);
            break;
        case "form-data":
            var formDataValueList = data["reqBody"].split(formdataBoundary);
            $("input:radio[name='body']").eq(0).click();
            $("input:radio[name='body']").eq(0).click();
            var formdataVarsList = [];
            for(var fIndex = 1; fIndex<formDataValueList.length-1; fIndex++){
                var tmpFormDict = {};
                var tmpFormdataValue = formDataValueList[fIndex];
                var formKey = tmpFormdataValue.match(/name="(\S*)"/)[1];
                tmpFormDict["key"] = formKey;
                if(tmpFormdataValue.indexOf('filename="')>-1){
                    //file类型
                    tmpFormDict["type"] = "file";
                    tmpFormDict["value"] = "";
                }else{
                    //text类型
                    tmpFormDict["type"] = "text";
                    tmpFormDict["value"] = tmpFormdataValue.split("\r\n\r\n")[1];
                }
                formdataVarsList.push(tmpFormDict);
            }
            formDataTabInit(formdataVarsList);
            break;
    }
    try{
        JSON.parse(data["respBody"]);
        commonValAfterInputEditor.setValue("ASSERT_STRUCT("+data["respBody"]+");");
    }catch (e){
        commonValAfterInputEditor.setValue("ASSERT("+data["respBody"]+");");
    }
}

//获取url中的参数
function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return unescape(r[2]); return null; //返回参数值
}

function result() {
    window.close();
    window.opener.location.href = '/InterfaceTest/HttpInterfaceCheck';
}

function moreEnv() {
    if ($('#debugMoreEnv').css("display") == "none") {
        $('#debugMoreEnv').css("display", "block");
    } else {
        $('#debugMoreEnv').css("display", "none");
    }
}

function HTMLEncode(html) {
    var temp = document.createElement("div");
    (temp.textContent != null) ? (temp.textContent = html) : (temp.innerText = html);
    var output = temp.innerHTML;
    temp = null;
    return output;
}

//查看接口调试详情
function checkDebugCase(id) {
    $('#resultDetailstr' + id).toggle();
    $('#resultDetails' + id).toggle();
}
//跳到事件的地方
function ShowDiv(element){
    obshowdiv =  element;
    offtop=obshowdiv.offset().top-155;
    offleft=obshowdiv.offset().left;
    obshowdiv.show();
    docheight = $(document).height();
    $('html,body').animate({scrollTop:offtop}, 200);
}

function clearResult() {
    $("#debugResultTbody").children().remove();
    checkResultId = 0;
    $("#debugResult").hide();
    $('#clearResult').hide();
}

function valLengthVerify(option) {
    if(option !== "debug"){
         if ($("#name").val() == "") {
            alert("接口名称不能为空");
            return false;
        }

        if ($("#describe").val() == "") {
            alert("接口描述不能为空");
            return false;
        }
    }


    if ($("#URI").val() == "输入URI") {
        alert("URI不能为空");
        return false;
    }

    if ($("#URL").val() == "") {
        alert("接口不能为空");
        return false;
    }else if($("#URL").val().indexOf("?")!=-1){
        alert("url中不能包含问号，参数请填写params，问号自动拼接");
        return false
    }

    if($("#customUri").val() !== "" && $("#customUri").val().trim().toLowerCase().substr(0, 4).indexOf("http") === -1){
        alert("http格式错误");
        return false
    }


    var result = true;
    if ($("input[name='body']:checked").val() == "form-data") {
        var fileInput = $("[name='body-form-Tr']");
        fileInput.each(function () {
            var thisElement = $(this).children().eq(0).children();
            if (thisElement.css("background-color") != "rgb(183, 186, 189)") {
                if (thisElement.val() == "") {
                    alert("form-data的Key值不能为空");
                    result =  false;
                }
            }
        })
    }
    return result;

}
function selectOnchang(option,obj) {
    var value = obj.options[obj.selectedIndex].value;
    var alias = obj.options[obj.selectedIndex].textContent;
    saveOrDebug(option,value,alias);
}
var thisTime = 0;
var debugFlag = false;

function saveOrDebug(option, httpConfKey, alias) {
       $("#publicKeyDiv").css("display","none");
    if (valLengthVerify(option) == false){
        return;
    }
    var formData = new FormData();

    var interfaceId = '';
    if (optionFromContext != "add") {
        interfaceId = $("#interfaceId").val();
    }

    var title = $("#name").val();
    var casedesc = $("#describe").val();
    var businessLineId = $("#businessLine option:selected").val();

    var moduleId = $("#modules option:selected").val();
    if (!moduleId){
        alert("请选择模块");
        return
    }
    var sourceId = $("#sources option:selected").val();
    var caselevel = $("#caselevel option:selected").val();
    var varsPre = commonValBeforeInputEditor.getValue();

    var timeout = "";
    $("#timeout").val() != "" ? timeout = $("#timeout").val() : timeout = 20;
    var performanceTime = "";
    $("#performanceTime").val() != "" ? performanceTime = $("#performanceTime").val() : performanceTime = 1;

    var uri = $("#URI").val();
    var customUri = $("#customUri").val();
    if ($("#useCustomUri").prop("checked")){
         var useCustomUri = 0;
    }else {
         var useCustomUri = 1;
    }
    var urlRedirect = $("#redirectSelect").val();

    var method = $("#methodSelect").val();
    var header = JSON.stringify(tableDataToDict("header"));
    var url = $("#URL").val();

    var paramsElement = $("#parameter");
    if (paramsElement.parent().css("display") == "none") {
        var params = tableDataTourlencode("params");
    } else {
        var params = paramsElement.val();
    }
    if (method != "GET" && method !="HEAD") {
        var bodyType = $("input[name='body']:checked").val();
        switch (bodyType) {
            case "none":
                var bodyContent = "";
            case "x-www-form-urlencoded":
                var urlEncodeElement = $("#x-www-form-urlencoded-input");
                if (urlEncodeElement.parent().css("display") == "none") {
                    var bodyContent = tableDataTourlencode("x-www-form-urlencoded");
                } else {
                    var bodyContent = urlEncodeElement.val();
                }
                break;
            case "raw":
                var bodyContent = $("#body-raw-input").val();
                break;
            case "binary":
                var binarySpan = $("#binarySpan").text();
                if (binarySpan == "") {
                    var fileInput = $("#fileInput")[0].files[0];
                    if(typeof (fileInput) == "undefined"){
                        alert("binary 必须选择文件");
                        return ;
                    }
                    if (typeof(fileInput) != "undefined") {
                        var bodyContent = {};
                        formData.append('file', fileInput);
                        bodyContent['showPath'] = $("#textName").val();
                        bodyContent["filename"] = fileInput.name;
                        bodyContent["size"] = fileInput.size;
                    }
                } else {
                    var bodyContent = JSON.parse(binarySpan);
                }

                break;
            case "form-data":
                var tableTr = $("[name='body-form-Tr']");
                var bodyContent = [];
                if (tableTr.length != 0) {
                    for (var i = 0; i < tableTr.length; i++) {
                        var key = tableTr.eq(i).find("td").eq(0).children().eq(0).val();
                        var type = tableTr.eq(i).find("td").eq(0).children().eq(1).val();
                        if (type == "text") {
                            var value = tableTr.eq(i).find("td").eq(1).children().val();
                            if (key == "" && value == "") {
                                continue
                            }
                        }
                        var thisContent = {};
                        thisContent["key"] = key;
                        thisContent["type"] = type;
                        var assignBodyContent = $("[name='formDataFileSpan']").eq(i).text();
                        if (thisContent["type"] == "text") {
                            thisContent["value"] = value;
                        } else if (assignBodyContent != "") {
                            formData.append(key, assignBodyContent);
                            thisContent["value"] = JSON.parse(assignBodyContent);
                        } else {
                            var formDataFileShowList = $("[name='formDataFileName']");
                            var formFileShowList = $("[name='formDataInput']").eq(i)[0].files[0];
                            if(typeof (formFileShowList) == "undefined"){
                                alert("formdata type 为file时必须选择文件");
                                return
                            }
                            thisContent["value"] = {};
                            thisContent["value"]["showPath"] = formDataFileShowList.eq(i).val();
                            thisContent["value"]["filename"] = formFileShowList.name;
                            thisContent["value"]["size"] = formFileShowList.size;
                            formData.append(key, formFileShowList)
                        }
                        bodyContent.push(thisContent);
                    }
                }
                break;

        }

    }else{
        var bodyType = '';
        var bodyContent = '';
    }
    var varsPost = commonValAfterInputEditor.getValue();

    var interfaceData = {
        interfaceId: interfaceId,
        title: title,
        casedesc: casedesc,
        businessLineId_id: businessLineId,
        moduleId_id: moduleId,
        sourceId_id: sourceId,
        caselevel: caselevel,
        timeout: timeout,
        performanceTime:performanceTime,
        varsPre: varsPre,
        uri: uri,
        customUri: customUri,
        useCustomUri: useCustomUri,
        method: method,
        header: header,
        url: url,
        urlRedirect:urlRedirect,
        params: params,
        varsPost: varsPost,
        bodyType:bodyType,
        bodyContent:bodyContent
    };

    if (option == "save") {
        formData.append("interfaceData",JSON.stringify(interfaceData));
         var interfaceAdd = $.ajax({
              url: HTTP_InterfaceAddUrl ,
              type: 'POST',
              data: formData,
              async: false,
              cache: false,
              contentType: false,
              processData: false
         });

        var interfaceAddJson = JSON.parse(interfaceAdd.responseText);
        if (interfaceAddJson["code"] == "10000") {
            if (optionFromContext == 'copy') {
                window.close();
                window.opener.location.reload();
            } else {
                location.href = HTTP_InterfaceCheckUrl;
            }

        } else {
            alert(interfaceAdd.responseText);
        }
    }
    else if (option == "debug") {
        if(alias&&httpConfKey){
            setHistoryItems(httpConfKey, alias);
            getHistoryItems('button');
        }
        thisTime = 0;
        debugFlag = true;
        checkResultId++;
        interfaceData.httpConfKey_id = httpConfKey;
        $("[name='debug']").attr("disabled", true);
        formData.append("interfaceData",JSON.stringify(interfaceData));
        var interfaceDebugAdd = $.ajax({
             url: HTTP_InterfaceDebugAddUrl ,
              type: 'POST',
              data: formData,
              async: false,
              cache: false,
              contentType: false,
              processData: false
        });

        var debugAddJson = JSON.parse(interfaceDebugAdd.responseText);
        var runing = ' <tr><td  colspan="10" align="center" style="font-size: 30px" >获取结果中...</td></tr>';
        $("#debugResultTbody").html(runing +  $("#debugResultTbody").html());

        $("#debugResult").show();
        $("#clearResult").show();
        if (debugAddJson["code"] == "10000") {
            $.ajax({
                url: HTTP_InterfaceDebugUrl,
                async: true,
                data: debugAddJson,
                type: "POST",
                success: function () {
                    function debugResult() {
                        var url = HTTP_InterfaceDebugGetResultUrl;
                        var getDebugResult = $.ajax({
                            url: url, async: true,
                            type:"POST",
                            data: debugAddJson,
                            success: function () {
                                var msg = 0;
                                var jsonValue = getDebugResult.responseText;
                                try{
                                     var returnMsg = JSON.parse(jsonValue);
                                }catch (err) {
                                    msg = 10000
                                }
                                if (msg ==10000) {

                                    if (jsonValue.url == "/UserLogin") {
                                        location.href = jsonValue.url;
                                        result();
                                    }

                                    try {
                                        $("#debugResultTbody").children().first().remove();
                                        $("#debugResultTbody").html(jsonValue + $("#debugResultTbody").html());
                                        var debugId = $("[name='debugId']");
                                        var debugBtnCheckDetails = $("[name='debugBtnCheckDetails']");
                                        var resultDetails = $("[name='resultDetails']");
                                        for (var i = 0; i< debugId.length;i++){
                                            debugBtnCheckDetails.eq(i).attr("onclick","checkDebugCase('"+(i+1)+"');ShowDiv($(this))");
                                            resultDetails.eq(i).attr("id","resultDetailstr"+(i+1));
                                        }
                                        debugId.first().text(debugId.length);
                                        var HTTPRequestSpan = JSON.parse($("[name='HTTPRequestSpan']").first().text());
                                        var HTTPRequestText = "";

                                        var HTTPBodyContent = $("[name='HTTPBodyContent']").first().text();
                                        var HTTPURL = $("[name='HTTPURL']").first().text();
                                        var HTTPParams = $("[name='HTTPParams']").first().text();
                                        var HTTPMethod = $("[name='HTTPMethod']").first().text();
                                        if(HTTPParams == ""){
                                            HTTPRequestText = HTTPMethod+ " " + HTTPURL+" HTTP/1.1";
                                        }else{
                                            HTTPRequestText = HTTPMethod + " " + HTTPURL+"?"+HTTPParams+" HTTP/1.1";
                                        }



                                        for(var HTTPRequestKey in HTTPRequestSpan){
                                            HTTPRequestText = HTTPRequestText +"\n"+HTTPRequestKey+":"+HTTPRequestSpan[HTTPRequestKey];
                                        }
                                        if(HTTPBodyContent != ""){
                                            HTTPRequestText = HTTPRequestText + "\n\n"+HTTPBodyContent;
                                        }

                                         $("[name='HTTPRequestText']").first().text(HTTPRequestText);


                                        var HTTPResultSpan = JSON.parse($("[name='HTTPResultSpan']").first().text());
                                        var HTTPActualText = "";
                                        var HTTPResultText = "HTTP/1.1 " + HTTPResultSpan["reason"];
                                        for (var HTTPResultKey in HTTPResultSpan["headers"]) {
                                            HTTPResultText = HTTPResultText + "\n" + HTTPResultKey + ":" + HTTPResultSpan["headers"][HTTPResultKey];
                                        }
                                        if (HTTPResultSpan["content"] != "") {
                                            HTTPResultText = HTTPResultText + "\n\n" + HTTPResultSpan["content"];
                                            HTTPActualText = HTTPResultSpan["content"];
                                        }
                                        $("[name='HTTPActualText']").first().text(HTTPActualText);
                                        $("[name='HTTPResultText']").first().text(HTTPResultText);

                                    } catch (err) {
                                        $("[name='HTTPActualText']").first().text($("[name='HTTPResultSpan']").first().text());
                                        $("[name='HTTPResultText']").first().text($("[name='HTTPResultSpan']").first().text());
                                    }

                                    $("[name='debug']").attr("disabled", false);
                                } else if (returnMsg["code"] == 16002) {
                                    thisTime += 1;
                                    $("#debugResultTbody").children().first().children().first().html("获取结果中...已执行"+thisTime+
                                        "秒&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;点击<button class=\"btn btn-danger\" onclick=\"cancelDebug()\">取消</button>调试"
                                    );
                                    if(debugFlag){
                                        debugResult();
                                    }else {
                                         $("#debugResultTbody").children().first().remove();
                                         $("#debugResultTbody").html( '<tr><td name=\'debugId\'>' + checkResultId + '</td><td colspan="9" align="center"  style="font-size: 30px" >调试已取消</td></tr>' + $("#debugResultTbody").html());
                                    }
                                } else {
                                     $("#debugResultTbody").children().first().remove();
                                    $("#debugResultTbody").html('<tr><td name=\'debugId\'>' + checkResultId + '</td><td colspan="10" align="center"  style="font-size: 30px" >结果获取失败，请联系管理员&nbsp;&nbsp;errorCode：' + returnMsg["code"] + '</td></tr>' + $("#debugResultTbody").html());
                                    $("[name='debug']").attr("disabled", false);
                                }

                            },
                            error: function () {
                                thisTime = 0;
                                debugFlag = false;
                                $("#debugResultTbody").children().first().remove();
                                $("#debugResultTbody").html('<tr><td name=\'debugId\' >' + checkResultId + '</td>' + checkResultId + '<td colspan="10" align="center"  style="font-size: 30px" >结果获取失败，服务器异常。'+jsonValue+'</td></tr>' +  $("#debugResultTbody").html());
                                $("[name='debug']").attr("disabled", false);
                            }
                        });

                    }

                    debugResult();
                },
                error:function () {
                     $("#debugResultTbody").children().first().remove();
                                $("#debugResultTbody").html('<tr><td> name=\'debugId\'' + checkResultId + '</td>' + checkResultId + '<td colspan="10" align="center"  style="font-size: 30px" >结果获取失败，服务器异常。'+jsonValue+'</td></tr>' +  $("#debugResultTbody").html());
                                $("[name='debug']").attr("disabled", false);
                }

            });
        } else {
             $("#debugResultTbody").children().first().remove();
            $("#debugResultTbody").html( '<tr><td name=\'debugId\'>' + checkResultId + '</td><td colspan="9" align="center"  style="font-size: 30px" >' + debugAddJson['body'] + '</td></tr>' + $("#debugResultTbody").html());
            $("[name='debug']").attr("disabled", false);
        }
        hideFuzhuBar();
        return;
    }
    else if (option == "edit") {
        var delTip = JSON.parse($.ajax({url:HTTP_InterfaceDelTipUrl+"?id="+data["id"],async:false}).responseText).body;
        if(delTip.num > 0){
            if(!confirm("将影响"+delTip.num+"条用例，编号为："+delTip.list)) {
                return
            }
        }

        interfaceData.id = data["id"];
        interfaceData.addBy = data["addBy_id"];
        formData.append("interfaceData",JSON.stringify(interfaceData));
        formData.append("id",data["id"]);
         var saveEditAjax = $.ajax({
              url: HTTP_InterfaceSaveEditUrl ,
              type: 'POST',
              data: formData,
              async: false,
              cache: false,
              contentType: false,
              processData: false
         });
        if (JSON.parse(saveEditAjax.responseText)["code"] == 10000) {
            if(confirm("保存成功，是否退出编辑？")){
                window.close();
                window.opener.location.reload();
            }
        } else {
            alert(JSON.parse(saveEditAjax.responseText)["message"])
        }
    }
}

function cancelDebug() {
    thisTime = 0;
    debugFlag = false;
    $("[name='debug']").attr("disabled", false);
}

function pageInit() {
    dataInit();
}

//弹出隐藏层
function ShowDiv(show_div,bg_div){
    //弹出详情层
    var obshowdiv =  $('#'+show_div);
    var offtop=obshowdiv.offset().top;
    var offleft=obshowdiv.offset().left;
    obshowdiv.css("top",offtop+40+"px");
    obshowdiv.css("left",offleft+40+"px");
    obshowdiv.show();

    var obbgdiv = $('#'+bg_div);
    obbgdiv.show();
    obbgdiv.css("top",offtop+0+"px");
    obbgdiv.css("left",offleft+0+"px");
    $('html,body').animate({scrollTop:offtop}, 800);
}
//关闭弹出层
function CloseDiv(show_div,bg_div){
    $('#'+show_div).hide();
    $('#'+bg_div).hide();
}
//请求报文转用例。
function httpRequestDatagramToInterfaceCase(){
    ShowDiv("addRequestDatagramDiv","fade");
}
function doDatagramToCase(){
    var requestDatagram =  $("#requestDatagramTextarea").val();
    var responseDatagram = $("#responseDatagramTextarea").val();
    var retData = getDataByDatagram(requestDatagram,responseDatagram);
    if(retData){
        initInfosByMockData(retData);
        CloseDiv("addRequestDatagramDiv","fade");
    }else{
        alert("请求报文不合法！");
    }
}

function getDataByDatagram(requestdata,responsedata){
    var dataDict = {};
    if(requestdata !== ""){
        var reqDataList = requestdata.split("\n\n");
        var reqLineAndHeader = reqDataList[0];
        var reqBodyContent = "";
        if(reqDataList.length>= 2){
            for(var index = 1; index < reqDataList.length; index++ ){
                if(index === reqDataList.length-1){
                    reqBodyContent += reqDataList[index];
                }else{
                    reqBodyContent += reqDataList[index]+"\n\n";
                }
            }
        }
        dataDict['reqBody'] = decodeURIComponent(reqBodyContent);

        //开始处理请求行和头
        var lineHeaderList = reqLineAndHeader.trim().split("\n");
        var reqLine = lineHeaderList[0];
        var reqLineList = reqLine.trim().split(" ");
        var host = "";
        var protocol = "http";
        var isDefaultProtocol = true;
        if(reqLineList.length == 3){
            dataDict['reqMethod'] = reqLineList[0];
            var urlParamList = reqLineList[1].split("?");
            dataDict['reqParam'] = "";
            for(var index = 1; index < urlParamList.length; index++ ){
                if(index === urlParamList.length-1) {
                    dataDict['reqParam'] += urlParamList[index];
                }else{
                    dataDict['reqParam'] += urlParamList[index]+"?";
                }
            }
            var hosturl = urlParamList[0];
            if(hosturl.charAt(0) == "/"){
                //这是url，没有host
                dataDict['reqUrl'] = hosturl;
            }else{
                //host开头
                var protocolhosturllist = hosturl.split("://");
                protocol = protocolhosturllist[0];
                isDefaultProtocol = false;
                var hosturlList = protocolhosturllist[1].split("/");
                host = hosturlList[0];
                dataDict['reqUrl'] = "/";
                for(var index = 1;index <hosturlList.length; index++ ){
                    if(index === hosturlList.length-1) {
                        dataDict['reqUrl'] += hosturlList[index];
                    }else{
                        dataDict['reqUrl'] += hosturlList[index]+"/";
                    }
                }
            }
        }else{
            return false;
        }
        dataDict['uriKey'] = "http-testproject";
        var reqHeaderDict = {};
        for(var index = 1; index < lineHeaderList.length; index++ ){
            var tmpheaderList = lineHeaderList[index].split(":");
            if(tmpheaderList.length == 2){
                reqHeaderDict[tmpheaderList[0]] = decodeURIComponent(tmpheaderList[1].trim());
            }
        }
        dataDict['reqHeader'] = JSON.stringify(reqHeaderDict);

        if(host.trim() == "" && reqHeaderDict.hasOwnProperty("Host")){
            host = reqHeaderDict["Host"];
        }
        if(host.trim() == ""){
            dataDict['uriKey'] = "";
        }else{
            var uriConfResp = $.ajax({
              url: HTTP_getUrikeyByConfigInfoUrl + '?host='+protocol+"://"+host ,
              async: false
            });
            dataDict['uriKey'] = uriConfResp.responseText;
            if(isDefaultProtocol && dataDict['uriKey'] == ""){
                var uriConfResp = $.ajax({
                  url: HTTP_getUrikeyByConfigInfoUrl + '?host=https://'+host ,
                  async: false
                });
                dataDict['uriKey'] = uriConfResp.responseText;
            }
        }
    }else{
        return false;
    }
    dataDict['respBody'] = "";
    if(responsedata !== "") {
        var respList = responsedata.split("\n\n");
        if(respList.length == 1){
            dataDict['respBody'] = respList[0];
        }else{
            for(var index = 1; index < respList.length; index++ ){
                dataDict['respBody'] += respList[index]+"\n\n";
            }
        }
    }
    dataDict['respBody'] = dataDict['respBody'].trim().length<=500 ? dataDict['respBody'].trim():dataDict['respBody'].trim().slice(0,499);
    return dataDict;
}

$("#loading").css("display", "");
pageInit();
window.onload = function () {
    $("#surprise").click();
    $("#surprise2").click();
};
$(document).ready(function() {
   $("#loading").css("display", "none");
   getHistoryItems('button');
});
