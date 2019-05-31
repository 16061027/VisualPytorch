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


function get_network() {
    var conn_list;
    var nets_conn = [];
    var nets = {};
    $("#canvas").find(".node").each(function (index, element) {
        var id = $(element).attr('id');
        nets[id] = {
            "name": $(element).attr('name'),
            "attribute": eval('(' + window.sessionStorage.getItem(id) + ')'),
            "left": $(element).css('left'),
            "top": $(element).css('top')
        }
    });
    conn_list = jsPlumb.getAllConnections();
    console.log(conn_list);

    for (var i = 0; i < conn_list.length; i++) {
        var source_id = conn_list[i]["sourceId"];
        var target_id = conn_list[i]["targetId"];
        var conn = {
            "source": {
                "id": source_id,
                "anchor_position": conn_list[i]["endpoints"][0]["anchor"]["type"]
            },
            "target": {
                "id": target_id,
                "anchor_position": conn_list[i]["endpoints"][1]["anchor"]["type"]
            }
        };
        nets_conn.push(conn);
    }
    var epoch = $("#epoch").val();
    if (epoch == "") {
        epoch = "1";
    }
    var learning_rate = $("#learning_rate").val();
    if (learning_rate == "") {
        learning_rate = "0.5";
    }
    var batch_size = $("#batch_size").val();
    if (batch_size == "") {
        batch_size = "1";
    }
    var static = {
        "epoch": epoch,
        "optimizer": $("#optimzier").find("option:selected").val(),
        "learning_rate": learning_rate,
        "batch_size": batch_size
    };
    var data = {
        "name": $("#model_name").val(),
        "structure": {
            "nets": nets,
            "nets_conn": nets_conn,
            "static": static
        }
    };
    return data;
}

function translate_network() {
    var data = get_network()["structure"];
    console.log(data);
    $.ajax({
        type: 'POST',
        url: gobalConfig.base_url + 'api/NeuralNetwork/getcode/',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        beforeSend: function (XMLHttpRequest) {
            var token = window.sessionStorage.getItem('token');
            if (token != null) {
                XMLHttpRequest.setRequestHeader("Authorization", "JWT " + token)
            }
        },
        success: function (data_return, status, xhr) {

            if (xhr.status == 200) {
                var main = "";
                var main_print = "";
                var model = "";
                var model_print = "";
                var ops = "";
                var ops_print = "";
                for (var i = 0; i < data_return["Main"].length; i++) {
                    main = main + data_return["Main"][i] + "<br>";
                    main_print=main_print+data_return["Main"][i] + "\n";
                }
                for (var i = 0; i < data_return["Model"].length; i++) {
                    model = model + data_return["Model"][i] + "<br>";
                    model_print=model_print+data_return["Model"][i] + "\n";
                }
                for (var i = 0; i < data_return["Ops"].length; i++) {
                    ops = ops + data_return["Ops"][i] + "<br>";
                    ops_print=ops_print+data_return["Ops"][i] + "\n";
                }
                var code = {
                    "model": model,
                    "main": main,
                    "ops": ops
                };
                var code_print = {
                    "model": model_print,
                    "main": main_print,
                    "ops": ops_print
                };
                window.sessionStorage.setItem("code", JSON.stringify(data_return));
                window.sessionStorage.setItem("code_print", JSON.stringify(code_print));
                window.open("show_code.html");
                //window.location.href="show_code.html";

            }
            else {
                alert(JSON.stringify(data_return));
            }

        },
        error: function (data_return) {
            alert(data_return["responseText"])
        }


    });
}


function save_network() {
    $("#save_modal").modal('hide');
    if (!window.sessionStorage.hasOwnProperty("userinfo")) {
        jump_to_login();
        return
    }
    var data = get_network();
    console.log(data);
    var query_object = getQueryObject(window.location.href);
    if (query_object.hasOwnProperty("id")) {
        var net_id = query_object["id"];
        $.ajax({
            type: 'PUT',
            url: gobalConfig.base_url + 'api/NeuralNetwork/network/' + net_id + '/',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            beforeSend: function (XMLHttpRequest) {
                var token = window.sessionStorage.getItem('token');
                if (token != null) {
                    XMLHttpRequest.setRequestHeader("Authorization", "JWT " + token)
                }
            },
            success: function (data_return) {
            },
            error: function (data_return) {
                alert(data_return["responseText"])
            }
        });
    } else {
        $.ajax({
            type: 'POST',
            url: gobalConfig.base_url + 'api/NeuralNetwork/network/',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            beforeSend: function (XMLHttpRequest) {
                var token = window.sessionStorage.getItem('token');
                if (token != null) {
                    XMLHttpRequest.setRequestHeader("Authorization", "JWT " + token)
                }
            },
            success: function (data_return) {
            },
            error: function (data_return) {
                alert(data_return["responseText"])
            }
        });
    }
}

function save_attr_linear_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#" + button["id"]).parent();
    var in_channel = form.find("[name = \"in_channels\"]");
    var out_channel = form.find("[name = \"out_channels\"]");
    //todo:加入更精确的正则判断
    form.find("[name='input_error']").remove();
    //正整数
    var reg = /^\s*[1-9]\d*\s*$/;
    var flag = true;
    var check_array = [in_channel, out_channel];
    check_array.forEach(function (value, index, array) {
        if (!reg.test(value.val())) {
            value.after("<p name='input_error' class='alert_font'>请输入正整数</p>");
            flag = false;
        }
    });
    if (!flag) {
        return;
    }
    window.sessionStorage.setItem(id, "{\"in_channels\":\"" + in_channel.val() + "\", \"out_channels\":\"" + out_channel.val() + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_view_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#" + button["id"]).parent();
    var shape = form.find("[name = \"shape\"]");
    form.find("[name='input_error']").remove();
    //匹配符合要求的数组
    var reg = /^(\s*[1-9]\d*\s*)+(,\s*[1-9]\d*\s*)*$/;
    if (!reg.test(shape.val())) {
        shape.after("<p name='input_error' class='alert_font'>输入不合法</p>");
        return;

    }
    window.sessionStorage.setItem(id, "{\"shape\":\"" + shape.val() + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_concatenate_layer(button) {
    var id = button["id"].split("popover_")[1];
    var form = $("#" + button["id"]).parent();
    var dim = form.find("[name = \"dim\"]");
    form.find("[name='input_error']").remove();
    var reg = /^\s*\d+\s*$/;
    if (!reg.test(dim.val())) {
        dim.after("<p name='input_error' class='alert_font'>输入不合法</p>");
        return;
    }
    window.sessionStorage.setItem(id, "{\"dim\":\"" + dim.val() + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_conv1d_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#" + button["id"]).parent();
    var in_channels = form.find("[name = \"in_channels\"]");
    var out_channels = form.find("[name = \"out_channels\"]");
    var kernel_size = form.find("[name = \"kernel_size\"]");
    var stride = form.find("[name = \"stride\"]");
    var padding = form.find("[name = \"padding\"]");
    var activity = form.find("[id=\"" + id + "activity\"]").find("option:selected").val();
    var pool_way = form.find("[id=\"" + id + "pool_way\"]").find("option:selected").val();
    var pool_kernel_size = form.find("[name = \"pool_kernel_size\"]");
    var pool_stride = form.find("[name = \"pool_stride\"]");
    var pool_padding = form.find("[name = \"pool_padding\"]");
    //todo:加入更精确的正则判断
    form.find("[name='input_error']").remove();
    var reg = /^\s*[1-9]\d*\s*$/;
    var flag = true;
    var check_array = (padding.val()=="0")?[in_channels, out_channels, kernel_size, stride]:[in_channels, out_channels, kernel_size, stride, padding];
    check_array.forEach(function (value, index, array) {
        if (!reg.test(value.val())) {
            value.after("<p name='input_error' class='alert_font'>输入不合法</p>");
            flag = false;
        }
    });
    if (!flag) {
        return;
    }
    //var activity = form.find("[name = \"activity\"]").val();
    //var pool_way = form.find("[name = \"pool_way\"]").val();
    window.sessionStorage.setItem(id, "{\"in_channels\":\"" + in_channels.val() + "\", \"out_channels\":\"" + out_channels.val() + "\", \"kernel_size\":\"" + kernel_size.val() + "\", " +
        "\"stride\":\"" + stride.val() + "\", \"padding\":\"" + padding.val() + "\",\"activity\":\"" + activity + "\",\"pool_way\":\"" + pool_way + "\",\"pool_kernel_size\":\"" + pool_kernel_size.val() + "\"," +
        "\"pool_stride\":\"" + pool_stride.val() + "\",\"pool_padding\":\"" + pool_padding.val() + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_conv2d_layer(button) {
    //这里是硬编码，考虑在b版本优化
    var id = button["id"].split("popover_")[1];
    var form = $("#" + button["id"]).parent();
    var in_channels = form.find("[name = \"in_channels\"]");
    var out_channels = form.find("[name = \"out_channels\"]");
    var kernel_size = form.find("[name = \"kernel_size\"]");
    var stride = form.find("[name = \"stride\"]");
    var padding = form.find("[name = \"padding\"]");
    var activity = form.find("[id=\"" + id + "activity\"]").find("option:selected").val();
    var pool_way = form.find("[id=\"" + id + "pool_way\"]").find("option:selected").val();
    var pool_kernel_size = form.find("[name = \"pool_kernel_size\"]");
    var pool_stride = form.find("[name = \"pool_stride\"]");
    var pool_padding = form.find("[name = \"pool_padding\"]");
    //todo:加入更精确的正则判断
    form.find("[name='input_error']").remove();
    var reg = /^\s*[1-9]\d*\s*$/;
    var flag = true;
     var check_array = (padding.val()=="0")?[in_channels, out_channels, kernel_size, stride]:[in_channels, out_channels, kernel_size, stride, padding];
    check_array.forEach(function (value, index, array) {
        if (!reg.test(value.val())) {
            value.after("<p name='input_error' class='alert_font'>输入不合法</p>");
            flag = false;
        }
    });
    if (!flag) {
        return;
    }
    //var activity = form.find("[name = \"activity\"]").val();
    //var pool_way = form.find("[name = \"pool_way\"]").val();
    window.sessionStorage.setItem(id, "{\"in_channels\":\"" + in_channels.val() + "\", \"out_channels\":\"" + out_channels.val() + "\", \"kernel_size\":\"" + kernel_size.val() + "\", " +
        "\"stride\":\"" + stride.val() + "\", \"padding\":\"" + padding.val() + "\",\"activity\":\"" + activity + "\",\"pool_way\":\"" + pool_way + "\",\"pool_kernel_size\":\"" + pool_kernel_size.val() + "\"," +
        "\"pool_stride\":\"" + pool_stride.val() + "\",\"pool_padding\":\"" + pool_padding.val() + "\"}");
    $("#" + id).popover('hide');
}




function save_attr_linear_layer_form(id) {
    //这里是硬编码，考虑在b版本优化

    var form = $("#form" + id).parent();
    var in_channel = form.find("[name = \"in_channels\"]");
    var out_channel = form.find("[name = \"out_channels\"]");
    //todo:加入更精确的正则判断
    form.find("[name='input_error']").remove();
    //正整数
    var reg = /^\s*[1-9]\d*\s*$/;
    var flag = true;
    var check_array = [in_channel, out_channel];
    check_array.forEach(function (value, index, array) {
        if (!reg.test(value.val())) {
            value.after("<p name='input_error' class='alert_font'>请输入正整数</p>");
            flag = false;
        }
    });
    if (!flag) {
        return;
    }
    window.sessionStorage.setItem(id, "{\"in_channels\":\"" + in_channel.val() + "\", \"out_channels\":\"" + out_channel.val() + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_view_layer_form(id) {
    //这里是硬编码，考虑在b版本优化
    var form = $("#form" + id).parent();
    var shape = form.find("[name = \"shape\"]");
    form.find("[name='input_error']").remove();
    //匹配符合要求的数组
    var reg = /^(\s*[1-9]\d*\s*)+(,\s*[1-9]\d*\s*)*$/;
    if (!reg.test(shape.val())) {
        shape.after("<p name='input_error' class='alert_font'>输入不合法</p>");
        return;

    }
    window.sessionStorage.setItem(id, "{\"shape\":\"" + shape.val() + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_concatenate_layer_form(id) {
    var form = $("#form" + id).parent();
    var dim = form.find("[name = \"dim\"]");
    form.find("[name='input_error']").remove();
    var reg = /^\s*\d+\s*$/;
    if (!reg.test(dim.val())) {
        dim.after("<p name='input_error' class='alert_font'>输入不合法</p>");
        return;
    }
    window.sessionStorage.setItem(id, "{\"dim\":\"" + dim.val() + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_conv1d_layer_form(id) {
    //这里是硬编码，考虑在b版本优化
    var form = $("#form" + id).parent();
    var in_channels = form.find("[name = \"in_channels\"]");
    var out_channels = form.find("[name = \"out_channels\"]");
    var kernel_size = form.find("[name = \"kernel_size\"]");
    var stride = form.find("[name = \"stride\"]");
    var padding = form.find("[name = \"padding\"]");
    var activity = form.find("[id=\"" + id + "activity\"]").find("option:selected").val();
    var pool_way = form.find("[id=\"" + id + "pool_way\"]").find("option:selected").val();
    var pool_kernel_size = form.find("[name = \"pool_kernel_size\"]");
    var pool_stride = form.find("[name = \"pool_stride\"]");
    var pool_padding = form.find("[name = \"pool_padding\"]");
    //todo:加入更精确的正则判断
    form.find("[name='input_error']").remove();
    var reg = /^\s*[1-9]\d*\s*$/;
    var flag = true;
    var check_array = (padding.val()=="0")?[in_channels, out_channels, kernel_size, stride]:[in_channels, out_channels, kernel_size, stride, padding];
    check_array.forEach(function (value, index, array) {
        if (!reg.test(value.val())) {
            value.after("<p name='input_error' class='alert_font'>输入不合法</p>");
            flag = false;
        }
    });
    if (!flag) {
        return;
    }
    //var activity = form.find("[name = \"activity\"]").val();
    //var pool_way = form.find("[name = \"pool_way\"]").val();
    window.sessionStorage.setItem(id, "{\"in_channels\":\"" + in_channels.val() + "\", \"out_channels\":\"" + out_channels.val() + "\", \"kernel_size\":\"" + kernel_size.val() + "\", " +
        "\"stride\":\"" + stride.val() + "\", \"padding\":\"" + padding.val() + "\",\"activity\":\"" + activity + "\",\"pool_way\":\"" + pool_way + "\",\"pool_kernel_size\":\"" + pool_kernel_size.val() + "\"," +
        "\"pool_stride\":\"" + pool_stride.val() + "\",\"pool_padding\":\"" + pool_padding.val() + "\"}");
    $("#" + id).popover('hide');
}

function save_attr_conv2d_layer_from(id) {
    //这里是硬编码，考虑在b版本优化
    var form = $("#form" + id).parent();
    var in_channels = form.find("[name = \"in_channels\"]");
    var out_channels = form.find("[name = \"out_channels\"]");
    var kernel_size = form.find("[name = \"kernel_size\"]");
    var stride = form.find("[name = \"stride\"]");
    var padding = form.find("[name = \"padding\"]");
    var activity = form.find("[id=\"" + id + "activity\"]").find("option:selected").val();
    var pool_way = form.find("[id=\"" + id + "pool_way\"]").find("option:selected").val();
    var pool_kernel_size = form.find("[name = \"pool_kernel_size\"]");
    var pool_stride = form.find("[name = \"pool_stride\"]");
    var pool_padding = form.find("[name = \"pool_padding\"]");
    //todo:加入更精确的正则判断
    form.find("[name='input_error']").remove();
    var reg = /^\s*[1-9]\d*\s*$/;
    var flag = true;
     var check_array = (padding.val()=="0")?[in_channels, out_channels, kernel_size, stride]:[in_channels, out_channels, kernel_size, stride, padding];
    check_array.forEach(function (value, index, array) {
        if (!reg.test(value.val())) {
            value.after("<p name='input_error' class='alert_font'>输入不合法</p>");
            flag = false;
        }
    });
    if (!flag) {
        return;
    }
    //var activity = form.find("[name = \"activity\"]").val();
    //var pool_way = form.find("[name = \"pool_way\"]").val();
    window.sessionStorage.setItem(id, "{\"in_channels\":\"" + in_channels.val() + "\", \"out_channels\":\"" + out_channels.val() + "\", \"kernel_size\":\"" + kernel_size.val() + "\", " +
        "\"stride\":\"" + stride.val() + "\", \"padding\":\"" + padding.val() + "\",\"activity\":\"" + activity + "\",\"pool_way\":\"" + pool_way + "\",\"pool_kernel_size\":\"" + pool_kernel_size.val() + "\"," +
        "\"pool_stride\":\"" + pool_stride.val() + "\",\"pool_padding\":\"" + pool_padding.val() + "\"}");
    $("#" + id).popover('hide');
}