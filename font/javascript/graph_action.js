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
}

function save_attr_linear_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#"+button["id"]).parent();
    var in_channel = form.find("[name = \"in_channel\"]").val();
    console.log(in_channel)
    var out_channel = form.find("[name = \"out_channel\"]").val();
    console.log(out_channel)
    window.localStorage.setItem(id,"{\"in_channel\":\""+in_channel+"\", \"out_channel\":\""+out_channel+"\"}");
}

function save_attr_view_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#"+button["id"]).parent();
    var shape = form.find("[name = \"shape\"]").val();
    window.localStorage.setItem(id,"{\"shape\":\""+shape+"\"}");
}

function save_attr_conv1d_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#"+button["id"]).parent();
    var in_channel = form.find("[name = \"in_channel\"]").val();
    var out_channel = form.find("[name = \"out_channel\"]").val();
    var kernel_size = form.find("[name = \"kernel_size\"]").val();
    var stride = form.find("[name = \"stride\"]").val();
    var padding = form.find("[name = \"padding\"]").val();
    //var activity = form.find("[name = \"activity\"]").val();
    //var pool_way = form.find("[name = \"pool_way\"]").val();
    window.localStorage.setItem(id,"{\"in_channel\":\""+in_channel+ "\", \"out_channel\":\""+out_channel+ "\", \"kernel_size\":\""+kernel_size+ "\", \"stride\":\""+stride+ "\", \"padding\":\""+padding+ "\"}");
}

function save_attr_conv2d_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#"+button["id"]).parent();
    var in_channel = form.find("[name = \"in_channel\"]").val();
    var out_channel = form.find("[name = \"out_channel\"]").val();
    var kernel_size = form.find("[name = \"kernel_size\"]").val();
    var stride = form.find("[name = \"stride\"]").val();
    var padding = form.find("[name = \"padding\"]").val();
    //var activity = form.find("[name = \"activity\"]").val();
    //var pool_way = form.find("[name = \"pool_way\"]").val();
    window.localStorage.setItem(id,"{\"in_channel\":\""+in_channel+ "\", \"out_channel\":\""+out_channel+ "\", \"kernel_size\":\""+kernel_size+ "\", \"stride\":\""+stride+ "\", \"padding\":\""+padding+ "\"}");
}