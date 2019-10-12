"use strict";

function setHistoryItems(keyword,alias) {
    if(!keyword || (!alias)){return;}
    keyword = keyword.trim();
    alias = alias.trim();
    var histroy = {};
    histroy['keyword'] = keyword;
    histroy['alias'] = alias;
    histroy = JSON.stringify(histroy);
    let { historyItems } = localStorage;
    if (historyItems === undefined) {
      localStorage.historyItems = histroy;
    } else {
      const onlyItem = historyItems.split('|').filter(function (e){
          if(e == histroy){
              return false;
          }else{return true}
      });
      if (onlyItem.length > 0) historyItems = histroy + '|' + onlyItem.join('|');
      localStorage.historyItems = historyItems;
    }
}
function getHistoryItems(way) {
    var history = localStorage.getItem("historyItems");
    var arr = [];
    $("#historyList").remove();
    if(history) {
        var temple = "";
        temple += '<div id="historyList"><span>我的历史 </span>';
        if(history.indexOf('|') < 0) arr.push(history);
        arr = history.split('|');
        if(arr.length >= 5){
            arr = arr.slice(0, 5);  // 历史记录展示最大条数
        }
        // checkAccount(arr, type, newArr);
        if(arr.length > 0) {
            if(way=='button'){
                $.each(arr, function (i, g) {
                    var hc = {};
                    hc = JSON.parse(g);
                    temple += '<button type="button" name="debug" ' +
                    'onclick="saveOrDebug(\'debug\',\''+ hc['keyword'] +'\',\''+ hc['alias'] + '\')"'+' ' +
                    'class="btn btn-info">'+hc['alias'] + '</button>';
                });
                temple +=  '<a onclick="clearHistroryItems()"><i class="glyphicon glyphicon-trash"></i></a>';

            }
            else if(way=='check'){
                temple += '<div></div>';
                $.each(arr, function (i, g) {
                    var hc = {};
                    hc = JSON.parse(g);
                    temple+='<label style="margin-left: 30px" ><input type="checkbox" name="httpConf" value='+'\''+ hc['keyword']+
                        '\' id='+'\''+ hc['alias']+ '\'>'+ hc['alias'] + '</label>';
                });
                temple +=  '<a onclick="clearHistroryItems()" style="margin-left: 30px"><i class="glyphicon glyphicon-trash"></i></a>';

            }
        }
    }
     $("#history").after(temple);

}
function clearHistroryItems() {
    localStorage.removeItem('historyItems');
    $("#historyList").remove();
}