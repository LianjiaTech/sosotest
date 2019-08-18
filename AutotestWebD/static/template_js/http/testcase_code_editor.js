var codeEditor = {}
function initAllEditor(stepNum){
    //readOnly:'nocursor',
    //
    var beforeElement = $("#commonValBefore__"+stepNum).find("[name='commonValBefore']");
    var afterElement = $("#commonValAfter__"+stepNum).find("[name='commonValAfter']");
    codeEditor["before_testCaseStep_"+stepNum] = CodeMirror.fromTextArea(beforeElement[0], {
        lineNumbers: true,
        matchBrackets: true,
        mode: "text/x-python",
        indentUnit: 4,
        indentWithTabs: false,
    });
    codeEditor["before_testCaseStep_"+stepNum].on("focus",function(editor,change){
        resetGlobalElement(beforeElement,codeEditor["before_testCaseStep_"+stepNum]);
    });
    // codeEditor["before_testCaseStep_"+stepNum].on("blur",function(editor,change){
    //     setTimeout(function(){
    //         codeEditor["before_testCaseStep_"+stepNum].setValue(codeEditor["before_testCaseStep_"+stepNum].getValue().trim().replace("\t","    "));
    //         renderDivByData(codeEditor["before_testCaseStep_"+stepNum].getValue(),"commonValBeforeInputLinkDiv");
    //       },200);
    // });
    codeEditor["before_testCaseStep_"+stepNum].setOption("extraKeys", {
        Tab: newTab
    });
    codeEditor["after_testCaseStep_"+stepNum] = CodeMirror.fromTextArea(afterElement[0], {
        lineNumbers: true,
        matchBrackets: true,
        mode: "text/x-python",
        indentUnit: 4,
        indentWithTabs: false,
    });
    codeEditor["after_testCaseStep_"+stepNum].on("focus",function(editor,change){
        resetGlobalElement(afterElement,codeEditor["after_testCaseStep_"+stepNum]);
    });
    codeEditor["after_testCaseStep_"+stepNum].on("blur",function(editor,change){
        setTimeout(function(){
            codeEditor["after_testCaseStep_"+stepNum].setValue(codeEditor["after_testCaseStep_"+stepNum].getValue().trim().replace("\t","    "));
            renderDivByData(codeEditor["after_testCaseStep_"+stepNum].getValue(),"commonValAfterInputLinkDiv");
          },200);
    });
    codeEditor["after_testCaseStep_"+stepNum].setOption("extraKeys", {
        Tab: newTab
    });

    if( optionFromContext === "check"){
        codeEditor["before_"+stepNum].setOption("readOnly", true);
        codeEditor["after_"+stepNum].setOption("readOnly", true);
    }
}

function dubboInitParameterEditor(stepNum){
    var parameterElement = $("#testCaseStep_"+stepNum).find("[name='parameter']");
     codeEditor["parameter_testCaseStep_"+stepNum] = CodeMirror.fromTextArea(parameterElement[0], {
        lineNumbers: true,
        matchBrackets: true,
        mode: "text/x-python",
        indentUnit: 4,
        indentWithTabs: false,
    });
    codeEditor["parameter_testCaseStep_"+stepNum].on("focus",function(editor,change){
        resetGlobalElement(parameterElement,codeEditor["parameter_testCaseStep_"+stepNum]);
    });
    // codeEditor["parameter_testCaseStep_"+stepNum].on("blur",function(editor,change){
    //     renderDivByData(codeEditor["parameter_testCaseStep_"+stepNum].getValue(),"commonValBeforeInputLinkDiv");
    // });
    codeEditor["parameter_testCaseStep_"+stepNum].setOption("extraKeys", {
        Tab: newTab
    });
}
