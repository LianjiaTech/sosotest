$.ajaxSetup({
      beforeSend: function(xhr, settings){
          var csrftoken = $.cookie('csrftoken');
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    });
    changeProduct();
    function changeProduct(){
        var productid = $("#productid").val();
        if(productid == null){
            return;
        }
        jQuery.post('/getProductitem',{
            productid:productid
        },function(dat){
            var productitemid = $("#productitemid");
            var options = '';
            for(jsonkey in dat){
                options += "<option value='" + jsonkey + "'>" + dat[jsonkey] + "</option>";
            }
            if(options != ''){
                productitemid.html(options);
            }
        });
    }