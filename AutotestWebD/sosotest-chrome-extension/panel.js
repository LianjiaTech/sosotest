// ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
// ---- ---- ---- ---- ajax

var serviceHost = "http://demo.domain.com";
// var serviceHost = "http://127.0.0.1";
$("#jump").attr("href",serviceHost);

const sendAjax = {
    post: async ({ data, url }) => {
        const xhr = new XMLHttpRequest;
        xhr.responseType = 'json';
        xhr.open('POST', url);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send(data);

        const response = await new Promise((res, rej) => {
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    res(xhr.response);
                    return;
                }
            };
        });

        return response;
    },
    get: async ({ data, url }) => {
        const queryString = Object.keys(data).map(key => `${key}=${data[key]}`).join('&');

        const xhr = new XMLHttpRequest;
        xhr.responseType = 'json';
        xhr.open('GET', `${url}?${queryString}`);
        xhr.send(null);

        const response = await new Promise((res, rej) => {
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    res(xhr.response);
                    return;
                }
            };
        });

        return response;
    }
};

// ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
// ---- ---- ---- ---- channel

// 与当前页面的DevTool Page之间建立一个channel
const channel = chrome.runtime.connect(null, {
    name: chrome.devtools.inspectedWindow.tabId.toString(),
});


// 监听channel消息
channel.onMessage.addListener(result => {

    const { isSuccess, data, mssage } = result;
    if (!isSuccess) {
        document.querySelector('#error').innerHTML += mesage;
        return;
    }



    const { method, queryString, url, response, headers,postData } = data;
    if (url.endsWith(".js")){
        return;
    }
    if (url.endsWith(".css")){
        return;
    }
    if (url.endsWith(".jpg")){
        return;
    }
    if (url.endsWith(".png")){
        return;
    }
    if (url.endsWith(".gif")){
        return;
    }
    // function sendAjaxPost(tmpData) {
    //     var sendUrl = "http://127.0.0.1/interfaceTest/HTTP_InterfaceAddPage";
    //     const xhr = new XMLHttpRequest;
    //     xhr.responseType = 'json';
    //     xhr.open('POST', sendUrl);
    //     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    //     xhr.send(tmpData);
    //
    //     const response = await new Promise((res, rej) => {
    //         xhr.onreadystatechange = () => {
    //             if (xhr.readyState === 4 && xhr.status === 200) {
    //                 res(xhr.response);
    //                 return;
    //             }
    //         };
    //     });
    //
    //     return response;
    // }
    //
    // sendAjaxPost(data);
    // sendAjax.post(JSON.stringify(data),"http://127.0.0.1/interfaceTest/HTTP_InterfaceAddPage");
    var new_headers = [];
    for(var index = 0;index < headers.length;index ++){
        if (headers[index]["name"] === "Content-Type"){
            new_headers.push({"Content-Type":headers[index]["value"]})
        }
    }
    data["headers"] = new_headers;
    var tmpStr = encodeURIComponent(JSON.stringify(data)).replace(/[\u4e00-\u9fa5]/gi,"aa");
    var tmpUrl = url;
    if (tmpUrl.length > 200){
        tmpUrl = tmpUrl.substr(0,200);
        tmpUrl = tmpUrl+"...";
    }
    var checkBoxId = "checkBoxTr_" + $("[name='resultTr']").length;
    // if(tmpStr.length > 7500){
    //     delete data["response"];
    //     var tmpStr1 = encodeURIComponent(JSON.stringify(data)).replace(/[\u4e00-\u9fa5]/gi,"aa");
    //     if (tmpStr1.length > 7500){
    //         $("#result").append('<tr class="urls_href" name="resultTr"><td>-<input class="checkbox_tmp" style="display:none;" type="checkbox" ></td><td><label style="font-size: 15px;float: left">&nbsp;&nbsp;&nbsp;&nbsp;'+method + '</label></td><td><span><a style="display: none" class="tmp_a"></a>' + tmpUrl+'</span></td></tr>');
    //     }else {
    //         $("#result").append('<tr class="urls_href"  name="resultTr"><td>&nbsp;&nbsp;&nbsp;&nbsp;<input class="checkbox_tmp" id="'+ checkBoxId +'" type="checkbox" ></td><td><label style="font-size: 15px;float: left">&nbsp;&nbsp;&nbsp;&nbsp;'+method+'</label></td><td><a class="tmp_a" target="_blank" style="display:block" href="javascript:void(0)" >'+ tmpUrl+'</a></td></tr>');
    //     }
    // }else {
        var responseMaxLength = 5000;
        try{
            JSON.parse(data["response"])
        }catch (Err){
            responseMaxLength = 20;
        }
        if (data["response"].length > responseMaxLength){
            data["response"] = data["response"].substr(0,20);
        }

        $("#result").append('<tr class="urls_href"  name="resultTr"><td>&nbsp;&nbsp;&nbsp;&nbsp;<input class="checkbox_tmp" id="'+ checkBoxId +'" type="checkbox" ></td><td><label style="font-size: 15px;float: left">&nbsp;&nbsp;&nbsp;&nbsp;'+method+'</label></td><td><a class="tmp_a" target="_blank"  name="urls_href" style="display:block" href="javascript:void(0)" >' + tmpUrl+'</a></td></tr>');
    // };
    $("#result").children().last().data(data);


    // $(".checkbox_tmp:last").on("click",this.tmpClick.bind(this,$(".checkbox_tmp:last")));


    $(".checkbox_tmp:last").click(function () {
        tmpClick($(this))
    });
    $(".tmp_a:last").click(function () {
        tmpAClick($(this))
    });


    // document.querySelector('#result').innerHTML += '<a target="_blank" name="urls_href" style="display:block" href=\'http://127.0.0.1/interfaceTest/HTTP_InterfaceAddPage?url='+url+'&method='+method+'&data='+JSON.stringify(queryString)+'\' >'+method+'&nbsp;&nbsp;'+url+'</a><br>';
});

function tmpAClick(element) {
    var requestData = element.parent().parent().data();
    var data = {"requestData":JSON.stringify(requestData)};
    var htmlObj = $.ajax({url:serviceHost+"/interfaceTest/HTTP_InterfacePlugIn",type:"POST",data:data,async:false});
    var responseText = JSON.parse(htmlObj.responseText);
    try{
        if(responseText["code"] === 10000){

                window.open(serviceHost+"/interfaceTest/HTTP_InterfaceAddPage?dataKey=" + responseText["body"]);

        }else {
            $("#error").text("tmpAClick responseText 解析失败 请检查是否登录 "+serviceHost+"或联系管理员");
            $("#titleDiv").show();
        }
    }catch(err){
        htmlObj = $.ajax({url:serviceHost+"/interfaceTest/HTTP_InterfacePlugIn",type:"POST",data:data,async:false});
        responseText = JSON.parse(htmlObj.responseText);
        try{
            if(responseText["code"] === 10000){

                    window.open(serviceHost+"/interfaceTest/HTTP_InterfaceAddPage?dataKey=" + responseText["body"]);

            }else {
                $("#error").text("tmpAClick responseText 解析失败 请检查是否登录 "+serviceHost+"或联系管理员");
                $("#titleDiv").show();
            }
        }catch(err){
           $("#error").text("tmpAClick 解析失败 请检查是否登录 "+serviceHost+"或联系管理员");
           $("#titleDiv").show();
        }
    }

}


var checkList = [];

function tmpClick(element) {
    var thisElementData = element.attr("id");
    if(element.is(':checked')){
        checkList.push(thisElementData);
    }else {
        checkList.splice($.inArray(thisElementData, checkList), 1);
    }
}


function saveTestCase() {
    if(checkList.length === 0){
        $("#error").text("未勾选请求信息");
        $("#titleDiv").show();
        return
    }
    var dataList = [];
    for (var index = 0;index < checkList.length;index ++){
        dataList.push($("#"+checkList[index]).parent().parent().data())
    }
    var data = {"request":JSON.stringify(dataList)};
    var htmlObj = $.ajax({url:serviceHost+"/interfaceTest/HTTP_TestCasePlugIn",type:"POST",data:data,async:false});
    try{
        if (JSON.parse(htmlObj.responseText)["code"] === 10000){

                window.open(serviceHost+"/interfaceTest/HTTP_TestCaseAddPage?dataKey=" + JSON.parse(htmlObj.responseText)["body"]);

        }else {
            $("#error").text("saveTestCase htmlObj 解析失败 请检查是否登录 "+serviceHost+"或联系管理员");
            $("#titleDiv").show();
        }
     }catch(err){
        htmlObj = $.ajax({url:serviceHost+"/interfaceTest/HTTP_TestCasePlugIn",type:"POST",data:data,async:false});
        try{
            if (JSON.parse(htmlObj.responseText)["code"] === 10000){

                window.open(serviceHost+"/interfaceTest/HTTP_TestCaseAddPage?dataKey=" + JSON.parse(htmlObj.responseText)["body"]);

            }else {
                $("#error").text("saveTestCase htmlObj 解析失败 请检查是否登录 "+serviceHost+"或联系管理员");
                $("#titleDiv").show();
            }
        }catch (err){
            $("#error").text("saveTestCase 解析失败 请检查是否登录 "+serviceHost+"或联系管理员");
            $("#titleDiv").show();
        }

    }



}

$("#clearCheckbox").click(function () {
    $(".checkbox_tmp").each(function () {
        if ($(this).is(":checked")){
            $(this).prop("checked",false);
        }
    });
    checkList = [];
})

$("#saveTestCase").click(saveTestCase);

$("#errorBtn").click(function () {
    $("#titleDiv").hide();
})

// ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
// ---- ---- ---- ---- Panel页面中的事件

// 点击按钮，模拟发起ajax请求
// document.querySelector('#button1').addEventListener('click', async () => {
//     const urls = document.querySelector('#result').innerHTML.split('<br>');
//     var filterText = document.getElementById("filterText");
//     // alert(filterText.value);
//     var newUrlString = ""
//     for(var i in urls) {
//          if (urls[i].search(filterText.value) == -1){
//              //没有找到，那么display:block 应该是
//              newUrlString = newUrlString + urls[i].replace(":block",":none").replace(":none",":block") + "<br>";
//          }else{
//              //display:none
//              newUrlString = newUrlString + urls[i].replace(":none",":block").replace(":block",":none");
//          }
//     }
//     document.querySelector('#result').innerHTML = newUrlString;
// });
// // 点击按钮，模拟发起ajax请求
// document.querySelector('#button12').addEventListener('click', async () => {
//     const urls = document.querySelector('#result').innerHTML.split('<br>');
//     alert(JSON.stringify(urls, null, 4));
//
//     // todo: 这里可以用sendAjax.get或者sendAjax.post发起ajax请求
//     // 从而将以上保存的http url存到服务器端
// });
// 点击按钮，模拟发起ajax请求
// document.querySelector('#button13').addEventListener('click', async () => {
//     const urls = document.querySelector('#result').innerHTML.split('<br>');
//     alert(JSON.stringify(urls, null, 4));
//
//     // todo: 这里可以用sendAjax.get或者sendAjax.post发起ajax请求
//     // 从而将以上保存的http url存到服务器端
// });
// ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
//点击按钮 数据
document.querySelector('#hideHref').addEventListener('click',async () => {
    var allHref = $(".urls_href");
    for(var index = 0;index < allHref.length ; index ++){
        if(allHref.eq(index).text().indexOf($("#filterText").val()) > -1){
            allHref.eq(index).hide();
        }

    }
});

document.querySelector('#selectHref').addEventListener('click',async () => {
    var allHref = $(".urls_href");
    for(var index = 0;index < allHref.length ; index ++){
        if(allHref.eq(index).text().indexOf($("#filterText").val()) > -1){
            allHref.eq(index).show();
        }else{
            allHref.eq(index).hide();
        }

    }
});

document.querySelector('#allHref').addEventListener('click',async () => {
    var allHref = $(".urls_href");
    for(var index = 0;index < allHref.length ; index ++){
        allHref.eq(index).show();
    }
});

document.querySelector('#clear').addEventListener('click',async () => {
    document.querySelector('#result').innerHTML = "";
    checkList = [];
});


// ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
