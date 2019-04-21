var gobalConfig = {
    "base_url": "http://127.0.0.1:8000/"
};

/*$(function () {
    $('#submit').click( function (e) {
        var conn_list;
        var network = [];
        conn_list = jsPlumb.getAllConnections();
        console.log(conn_list);
        for (var i = 0; i < conn_list.length; i++) {
            var source_id = conn_list[i]["sourceId"];
            var target_id = conn_list[i]["targetId"];
            var conn = {
                "source": $("#" + source_id).attr("name"),
                "target": $("#" + target_id).attr("name")
            }
            network.push(conn);
        }

       $.ajax({
            type: 'POST',
            url: gobalConfig.base_url + 'NeuralNetwork/network/',
            data: JSON.stringify(network),
            contentType: 'application/json; charset=UTF-8',
            success: function (data_return) {
                alert(data_return);
            }
        });
    });
});*/
function save_network() {
    var conn_list;
    var network = [];
    conn_list = jsPlumb.getAllConnections();
    console.log(conn_list);

    for (var i = 0; i < conn_list.length; i++) {
        var source_id = conn_list[i]["sourceId"];
        var target_id = conn_list[i]["targetId"];

        var source = {
            "id": source_id,
            "name": $("#" + source_id).attr("name"),
            "attribute": eval('(' + window.localStorage.getItem(source_id) + ')')
        };
        var target = {
            "id": target_id,
            "name": $("#" + target_id).attr("name"),
            "attribute": eval('(' + window.localStorage.getItem(target_id) + ')')
        };
        var conn = {
            "source": source,
            "target": target
        };
        network.push(conn);
    }
    var epoch=$("#epoch").val();
    if(epoch==""){
        epoch= "1";
    }
    var learning_rate = $("#learning_rate").val();
    if(learning_rate==""){
        learning_rate="0.5";
    }
    var batch_size = $("#batch_size").val();
    if(batch_size==""){
        batch_size="1";
    }
    var static = {
        "epoch": epoch,
        "optimizer": $("#optimzier").find("option:selected").val(),
        "learning_rate": learning_rate,
        "batch_size": batch_size
    };
    var data = {
        "network": network,
        "static": static
    };
    console.log(data);
    $.ajax({
        type: 'POST',
        url: 'NeuralNetwork/network/',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        success: function (data_return) {
        },
        error:function (data_return) {
            alert(data_return["responseText"])
        }
    });
    $.ajax({
        type: 'POST',
        url: 'NeuralNetwork/getcode/',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        success: function (data_return,status,xhr) {
            console.log(data_return,status,xhr);
            if(xhr.status==200){
                var main="";
                var model="";
                var ops = "";
                for(var i=0;i<data_return["Main"].length;i++){
                    main = main+data_return["Main"][i]+"<br>";
                }
                for(var i=0;i<data_return["Model"].length;i++){
                    model = main+data_return["Model"][i]+"<br>";
                }
                for(var i=0;i<data_return["Ops"].length;i++){
                    ops = main+data_return["Ops"][i]+"<br>";
                }
                var code = {
                  "model":model,
                  "main":main,
                  "ops":ops
                };
                window.localStorage.setItem("code",JSON.stringify(data_return));
                window.open("show_code.html");
                //window.location.href="show_code.html";

            }
            else{
                alert(JSON.stringify(data_return));
            }

        },
        error:function (data_return) {
            alert(data_return["responseText"])
        }


    });
}

function save_attr_linear_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#" + button["id"]).parent();
    var in_channel = form.find("[name = \"in_channel\"]");
    var out_channel = form.find("[name = \"out_channel\"]");
    //todo:加入更精确的正则判断
    form.find("[name='input_error']").remove();
    var reg = /^[0-9]+$/ ;
    var flag = true;
    var check_array = [in_channel,out_channel];
    check_array.forEach(function (value,index,array) {
       if(!reg.test(value.val())){
           value.after("<p name='input_error' class='alert_font'>输入不合法</p>");
           flag = false;
       }
    });
    if(!flag){
        return;
    }
    window.localStorage.setItem(id, "{\"in_channel\":\"" + in_channel.val() + "\", \"out_channel\":\"" + out_channel.val() + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_view_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#" + button["id"]).parent();
    var shape = form.find("[name = \"shape\"]");
    form.find("[name='input_error']").remove();
    if(shape.val().replace(" ","")==""){
        shape.after("<p name='input_error' class='alert_font'>输入不合法</p>");
        return;
    }
    window.localStorage.setItem(id, "{\"shape\":\"" + shape.val() + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_conv1d_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#" + button["id"]).parent();
    var in_channel = form.find("[name = \"in_channel\"]");
    var out_channel = form.find("[name = \"out_channel\"]");
    var kernel_size = form.find("[name = \"kernel_size\"]");
    var stride = form.find("[name = \"stride\"]");
    var padding = form.find("[name = \"padding\"]");
    var activity = form.find("[id=\"" + id + "activity\"]").find("option:selected").val();
    var pool_way = form.find("[id=\"" + id + "pool_way\"]").find("option:selected").val();
    //todo:加入更精确的正则判断
    form.find("[name='input_error']").remove();
    var reg = /^[0-9]+$/ ;
    var flag = true;
    var check_array = [in_channel,out_channel,kernel_size,stride,padding];
    check_array.forEach(function (value,index,array) {
       if(!reg.test(value.val())){
           value.after("<p name='input_error' class='alert_font'>输入不合法</p>");
           flag = false;
       }
    });
    if(!flag){
        return;
    }
    //var activity = form.find("[name = \"activity\"]").val();
    //var pool_way = form.find("[name = \"pool_way\"]").val();
    window.localStorage.setItem(id, "{\"in_channel\":\"" + in_channel.val() + "\", \"out_channel\":\"" + out_channel.val() + "\", \"kernel_size\":\"" + kernel_size.val() + "\", " +
        "\"stride\":\"" + stride.val() + "\", \"padding\":\"" + padding.val() + "\",\"activity\":\"" + activity + "\",\"pool_way\":\"" + pool_way + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_conv2d_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#" + button["id"]).parent();
    var in_channel = form.find("[name = \"in_channel\"]");
    var out_channel = form.find("[name = \"out_channel\"]");
    var kernel_size = form.find("[name = \"kernel_size\"]");
    var stride = form.find("[name = \"stride\"]");
    var padding = form.find("[name = \"padding\"]");
    var activity = form.find("[id=\"" + id + "activity\"]").find("option:selected").val();
    var pool_way = form.find("[id=\"" + id + "pool_way\"]").find("option:selected").val();
    //todo:加入更精确的正则判断
    form.find("[name='input_error']").remove();
    var reg = /^[0-9]+$/ ;
    var flag = true;
    var check_array = [in_channel,out_channel,kernel_size,stride,padding];
    check_array.forEach(function (value,index,array) {
       if(!reg.test(value.val())){
           value.after("<p name='input_error' class='alert_font'>输入不合法</p>");
           flag = false;
       }
    });
    if(!flag){
        return;
    }
    //var activity = form.find("[name = \"activity\"]").val();
    //var pool_way = form.find("[name = \"pool_way\"]").val();
    window.localStorage.setItem(id, "{\"in_channel\":\"" + in_channel.val() + "\", \"out_channel\":\"" + out_channel.val() + "\", \"kernel_size\":\"" + kernel_size.val() + "\", " +
        "\"stride\":\"" + stride.val() + "\", \"padding\":\"" + padding.val() + "\",\"activity\":\"" + activity + "\",\"pool_way\":\"" + pool_way + "\"}");
    $("#" + id).popover('hide');
}