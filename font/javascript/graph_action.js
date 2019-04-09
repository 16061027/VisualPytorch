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
    var out_channel = form.find("[name = \"out_channel\"]").val();
    window.localStorage.setItem(id,"{\"in_channel\":"+in_channel+", \"out_channel\":"+out_channel+"}");
}



