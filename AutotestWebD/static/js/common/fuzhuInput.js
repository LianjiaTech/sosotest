var thisElementForPublicKey = '';
var currentCodeEditor = '';
var lastModeType = 'KW';
$(function () {
    var isResizing = false, lastDownX = 0;
    var container = $('#container'), right = $('#right'), handle = $('#handle');
    //var left = $('#left');
    handle.on('mousedown', function (e) {
        isResizing = true;
        lastDownX = e.clientX;
    });
    $(document).on('mousemove', function (e) {
        // we don't want to do anything if we aren't resizing.
        if (!isResizing) return;
        var offsetRight = container.width() - (e.clientX - container.offset().left);
        //left.css('right', offsetRight);
        right.css('width', offsetRight);
        setFuzhuHeight();
    }).on('mouseup', function (e) {
        // stop resizing
        isResizing = false;
    });
});

$(document).keydown(function(event){
　　if(event.keyCode === 27){
        //27是ESC键
      var closeList = ["CloseDetailDiv('showDetailsInfoDiv','showDetailsInfoDivFade')","CloseDiv('addRequestDatagramDiv','fade')","hideFuzhuBar()",
      "closeInterfaceList()","closeTestCaseList()","closeTaskList()"];
      for(var clsIndex = 0; clsIndex < closeList.length; clsIndex++){
          try{eval(closeList[clsIndex])}catch(e){}
      }
    }
});
function ChangeFuzhuType(modeType) {
    if(modeType == "PY"){
        $("#publicKeyDiv").css("display","none");
        $("#publicKeyPyDiv").css("display","block");
        lastModeType = "PY";
    }else{
        $("#publicKeyDiv").css("display","block");
        $("#publicKeyPyDiv").css("display","none");
        lastModeType = "KW";
    }
}
function resetGlobalElement(element,codeEditor) {
    var elementValue = "";
    if(codeEditor === ""){
        elementValue = element.val();
    }else{
        elementValue = codeEditor.getValue();
    }
    if(elementValue.trim().match(/^\#(\s)*python/g)){
            lastModeType = "PY";
    }
    ChangeFuzhuType(lastModeType);
    setFuzhuHeight();
    var rightMinWidth = 180;
    if($("#right").css("width").replace("px","")<rightMinWidth){
        $("#right").css("width",rightMinWidth+"px");
    }
    var tipElementList = $("#publicKeyDiv").find('a');
    tipElementList.each(function () {
        $(this).css("display", "none");
    });

    var elementName = element.attr("name");
    var commonTip = ["VAR", "GVAR", "TEXT", "LOGIN", "GET_TOKEN", "EXECUTE_INTERFACE", "JSON_GET", "JSON_PATH_EXIST","RE_FINDALL","BS_FIND","URL_ENCODE",
                "JSON_LIST_LEN", "GET_JSON_KEY_BY_INDEX","GET_LIST_KEY_VALUE_TO_STRING_WITH_SPLIT_TAG","TIMESTAMP", "DATETIME_FORMAT", "SPECIAL_TIMESTAMP", "TIMESTAMP_FORMAT", "RANDOM_INT", "RANDOM_CN",
                "RANDOM_EN", "SUB_STR", "EVAL", "CONST","Branch"];
    var VARTip = ["VAR", "GVAR"];
    var afterVal = ["INTERFACE_CONST","Branch"];
    var expectTip = ["SQL_SELEC", "COMPARE","Branch"];
    var timeSleep = ["TIME_SLEEP"];
    var showTipNameDict =
        {
            "common": commonTip,
            "VAR": VARTip,
            "expect": expectTip,
            "afterVal":afterVal,
            "timeSleep":timeSleep
        };

    var elementNameDict =
        {
            "common":["commonValBeforeInput","commonAfterValInput","BeforeValInput","afterValInput","commonValAfter","commonValBefore","keywordCode"],
            "VAR": [ "headerKey","headerValue","paramsKey","paramsValue","bodyFormKey","bodyFormValue","urlEncodeKey","urlEncodeValue","body-raw-input","x-www-form-urlencoded-input","URL","parameter","parameters"],
            "afterVal":["afterValInput","keywordCode"],
            "timeSleep":["BeforeValInput","afterValInput","commonValBeforeInput","commonAfterValInput","keywordCode"]
        };

    for(var elementKey in elementNameDict ){
           if($.inArray(elementName, elementNameDict[elementKey]) != -1){
                thisElementForPublicKey = element;
                currentCodeEditor = codeEditor;
                 for(var tipName = 0; tipName<showTipNameDict[elementKey].length;tipName++){
                    $("[name='publicKey-"+showTipNameDict[elementKey][tipName]+"']").css("display","block");
                }
            }
    }
}

function hideFuzhuBar(){
    $("#right").css("width","0.3%");
}

function resetPublicKey(key) {
    if (currentCodeEditor == ""){
        thisElementForPublicKey.val(thisElementForPublicKey.val()+key);
    }else{
        if(currentCodeEditor.somethingSelected()){
            //执行替换
            currentCodeEditor.replaceSelection(key);
        }else{
            currentCodeEditor.setValue(currentCodeEditor.getValue()+key);
        }
    }
}

function setFuzhuHeight(){
    $("#right").css('height', window.innerHeight*0.85);
    $("#publicKeyDiv").css('height', window.innerHeight*0.85);
}

function OpenDetailDiv(title,content){
    //弹出详情层
    var obshowdiv =  $('#showDetailsInfoDiv');
    var offtop=obshowdiv.offset().top;
    var offleft=obshowdiv.offset().left;
    obshowdiv.css("top",offtop+"px");
    obshowdiv.css("left",offleft+"px");
    obshowdiv.css("width","100%");
    obshowdiv.css("height","100%");
    obshowdiv.show();

    var obbgdiv = $('#showDetailsInfoDivFade');
    obbgdiv.show();
    obbgdiv.css("top",offtop+0+"px");
    obbgdiv.css("left",offleft+0+"px");
    $("#realDetailInfoText").val(content);
    $("#realDetailInfoTitle").text(title);
    $('html,body').animate({scrollTop:offtop}, 800);
}
//关闭弹出层
function CloseDetailDiv(show_div,bg_div){
    $('#'+show_div).hide();
    $('#'+bg_div).hide();
}

window.onscroll = function () {
    $("#right").css("top", $(document).scrollTop()+window.innerHeight*0.1 );
    setFuzhuHeight();
};