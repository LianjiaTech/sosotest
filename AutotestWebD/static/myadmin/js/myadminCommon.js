//验证
function isRequired () {

}
isRequired.prototype ={
    formRequired: function(ele){
        if (!ele || ele.nodeType !== 1) return;
        var isRequired = null;
        if (typeof window.screenX === "number") {
            if (typeof ele.attr("required") === "string") {
                isRequired = 'required';
            }
        } else {
            // IE6, IE7, IE8
            var outer = ele.outerHTML, part = outer.slice(0, outer.search(/\/?['"]?>(?![^<]*<['"])/));
            if (/\srequired\b/i.test(part)){
                isRequired = 'required';
            }
        }
        return isRequired;
    }
};


//获取url中的参数
function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return unescape(r[2]); return null; //返回参数值
}