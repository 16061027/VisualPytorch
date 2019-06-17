function get_content(name, parid) {
    if (name == "view_layer") {
        return "<form class=\"form-horizontal\" role=\"form\" id = 'form" + parid + "' name = 'view_layer'><div class=\"form-group\">" +
            "                    <label class=\"col-sm-5 control-label\">shape</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='shape' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["shape"] + "\" placeholder=\"1\">" +
            "                    </div>" +
            "                </div>" +
            "                </form>";
    }

    if (name == "concatenate_layer") {
        return "<form class=\"form-horizontal\" role=\"form\" id = 'form" + parid + "' name = 'concatenate_layer'><div class=\"form-group\">" +
            "                    <label class=\"col-sm-5 control-label\">dim</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='dim' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["dim"] + "\" placeholder=\"1\">" +
            "                    </div>" +
            "                </div>" +
            "                </form>";
    }

    if (name == "linear_layer") {
        return "<form class=\"form-horizontal\" role=\"form\" id = 'form" + parid + "' name = 'linear_layer'><div class=\"form-group\">" +
            "                    <label class=\"col-sm-5 control-label\">in_channels</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='in_channels' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["in_channels"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-5 control-label\">out_channels</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='out_channels' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["out_channels"] + "\">" +
            "                    </div>" +
            "                </div>" +
            "                </form>";
    }

    if (name == "conv1d_layer") {
        return "<form class=\"form-horizontal\" role=\"form\" id = 'form" + parid + "' name = 'conv1d_layer'><div class=\"form-group\">" +
            "                    <label class=\"col-sm-5 control-label\">in_channels</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='in_channels' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["in_channels"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-5 control-label\">out_channels</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='out_channels' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["out_channels"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-5 control-label\">kernel_size</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='kernel_size' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["kernel_size"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-5 control-label\">stride</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='stride' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["stride"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-5 control-label\">padding</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='padding' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["padding"] + "\">" +
            "                    </div></div><div class=\"form-group\">" +
            "                    <label class=\"control-label\">activity</label>" +

            "                        <select id=\"" + parid + "activity\" class=\"form-control\">\n" +
            "                            <option value=\"None\">None</option>\n" +
    "                            <option value=\"torch.nn.ReLU\">relu</option>\n" +
    "                            <option value=\"torch.nn.LeakyReLU\">leaky_relu</option>\n" +
    "                            <option value=\"torch.nn.Sigmoid\">sigmoid</option>\n" +
    "                            <option value=\"torch.nn.Tanh\">tanh</option>\n" +
            "                        </select>" +

            "                    <label class=\"control-label\">pool_way</label>" +

            "                        <select id=\"" + parid + "pool_way\" name='pool_way' class=\"form-control\">\n" +
    "                            <option value=\"None\">None</option>\n" +
    "                            <option value=\"torch.nn.MaxPool1d\">max_pool1d</option>\n" +
    "                            <option value=\"torch.nn.MaxPool2d\">max_pool2d</option>\n" +
    "                            <option value=\"torch.nn.MaxPool3d\">max_pool3d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool1d\">AvgPool1d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool2d\">AvgPool2d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool3d\">AvgPool3d</option>\n" +
            "                        </select>" +

            "                    <label class=\"col-sm-6 control-label\">pool_kernel_size</label>" +
            "                            <div class=\"col-sm-6\">" +
            "                        <input type=\"text\" id=\"" + parid + "pool_kernel_size\" name='pool_kernel_size' disabled=true class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["pool_kernel_size"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-6 control-label\">pool_stride</label>" +
            "                            <div class=\"col-sm-6\">" +
            "                        <input type=\"text\" id=\"" + parid + "pool_stride\" name='pool_stride' disabled=true class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["pool_stride"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-6 control-label\">pool_padding</label>" +
            "                            <div class=\"col-sm-6\">" +
            "                        <input type=\"text\" id=\"" + parid + "pool_padding\" name='pool_padding' disabled=true class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["pool_padding"] + "\">" +
            "                    </div>" +
            "                </div>" +
            "                </form>";
    }

    if (name == "conv2d_layer") {
        return "<form class=\"form-horizontal\" role=\"form\" id = 'form" + parid + "' name = 'conv2d_layer'><div class=\"form-group\">" +
            "                    <label class=\"col-sm-5 control-label\">in_channels</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='in_channels' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["in_channels"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-5 control-label\">out_channels</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='out_channels' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["out_channels"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-5 control-label\">kernel_size</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='kernel_size' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["kernel_size"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-5 control-label\">stride</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='stride' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["stride"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-5 control-label\">padding</label>" +
            "                            <div class=\"col-sm-5\">" +
            "                        <input type=\"text\" name='padding' class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["padding"] + "\">" +
            "                    </div></div><div class=\"form-group\">" +
            "                    <label class=\"control-label\">activity</label>" +

            "                        <select id=\"" + parid + "activity\" class=\"form-control\">\n" +
            "                            <option value=\"None\">None</option>\n" +
    "                            <option value=\"torch.nn.ReLU\">relu</option>\n" +
    "                            <option value=\"torch.nn.LeakyReLU\">leaky_relu</option>\n" +
    "                            <option value=\"torch.nn.Sigmoid\">sigmoid</option>\n" +
    "                            <option value=\"torch.nn.Tanh\">tanh</option>\n" +
            "                        </select>" +

            "                    <label class=\"control-label\">pool_way</label>" +

            "                        <select id=\"" + parid + "pool_way\" name='pool_way' class=\"form-control\">\n" +
            "                            <option value=\"None\">None</option>\n" +
"                            <option value=\"None\">None</option>\n" +
    "                            <option value=\"torch.nn.MaxPool1d\">max_pool1d</option>\n" +
    "                            <option value=\"torch.nn.MaxPool2d\">max_pool2d</option>\n" +
    "                            <option value=\"torch.nn.MaxPool3d\">max_pool3d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool1d\">AvgPool1d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool2d\">AvgPool2d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool3d\">AvgPool3d</option>\n" +
            "                        </select>" +

            "                    <label class=\"col-sm-6 control-label\">pool_kernel_size</label>" +
            "                            <div class=\"col-sm-6\">" +
            "                        <input type=\"text\" id=\"" + parid + "pool_kernel_size\" name='pool_kernel_size' disabled=true class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["pool_kernel_size"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-6 control-label\">pool_stride</label>" +
            "                            <div class=\"col-sm-6\">" +
            "                        <input type=\"text\" id=\"" + parid + "pool_stride\" name='pool_stride' disabled=true class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["pool_stride"] + "\">" +
            "                    </div>" +
            "                    <label class=\"col-sm-6 control-label\">pool_padding</label>" +
            "                            <div class=\"col-sm-6\">" +
            "                        <input type=\"text\" id=\"" + parid + "pool_padding\" name='pool_padding' disabled=true class=\"form-control\" value=\"" + eval('(' + window.sessionStorage.getItem(parid) + ')')["pool_padding"] + "\">" +
            "                    </div>" +
            "                </div>" +
            "                </form>";
    }

}

