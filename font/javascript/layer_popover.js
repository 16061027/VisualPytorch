var view_layer = "<form class=\"form-horizontal\" role=\"form\"><div class=\"form-group\">" +
    "                    <label class=\"col-sm-5 control-label\">shape</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\"; class=\"form-control\" placeholder=\"1\">" +
    "                    </div>" +
    "                </div>" +
    "                </form>"
var linear_layer = "<form class=\"form-horizontal\" role=\"form\"><div class=\"form-group\">" +
    "                    <label class=\"col-sm-5 control-label\">in_channel</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">out_channel</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                </div>" +
    "                </form>"
var conv1d_layer = "<form class=\"form-horizontal\" role=\"form\"><div class=\"form-group\">" +
    "                    <label class=\"col-sm-5 control-label\">in_channel</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">out_channel</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">kernel_size</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">stride</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">padding</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">activity</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <select id=\"disabledSelect\" class=\"form-control\">\n" +
    "                            <option value=\"None\">None</option>\n" +
    "                            <option value=\"torch.nn.functional.relu\">relu</option>\n" +
    "                            <option value=\"torch.nn.functional.leaky_relu\">leaky_relu</option>\n" +
    "                            <option value=\"torch.nn.functional.sigmoid\">sigmoid</option>\n" +
    "                            <option value=\"torch.nn.functional.tanh\">tanh</option>\n" +
    "                            <option value=\"torch.nn.functional.softmax\">softmax</option>\n" +
    "                        </select>" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">pool_way</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <select id=\"disabledSelect\" class=\"form-control\">\n" +
    "                            <option value=\"None\">None</option>\n" +
    "                            <option value=\"torch.nn.functional.max_pool1d\">max_pool1d</option>\n" +
    "                            <option value=\"torch.nn.functional.max_pool2d\">max_pool2d</option>\n" +
    "                            <option value=\"torch.nn.functional.max_pool3d\">max_pool3d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool1d\">AvgPool1d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool2d\">AvgPool2d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool3d\">AvgPool3d</option>\n" +
    "                        </select>" +
    "                    </div>" +
    "                </div>" +
    "                </form>"
var conv2d_layer = "<form class=\"form-horizontal\" role=\"form\"><div class=\"form-group\">" +
    "                    <label class=\"col-sm-5 control-label\">in_channel</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">out_channel</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">kernel_size</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">stride</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">padding</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\" class=\"form-control\">" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">activity</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <select id=\"disabledSelect\" class=\"form-control\">\n" +
    "                            <option value=\"None\">None</option>\n" +
    "                            <option value=\"torch.nn.functional.relu\">relu</option>\n" +
    "                            <option value=\"torch.nn.functional.leaky_relu\">leaky_relu</option>\n" +
    "                            <option value=\"torch.nn.functional.sigmoid\">sigmoid</option>\n" +
    "                            <option value=\"torch.nn.functional.tanh\">tanh</option>\n" +
    "                            <option value=\"torch.nn.functional.softmax\">softmax</option>\n" +
    "                        </select>" +
    "                    </div>" +
    "                    <label class=\"col-sm-5 control-label\">pool_way</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <select id=\"disabledSelect\" class=\"form-control\">\n" +
    "                            <option value=\"None\">None</option>\n" +
    "                            <option value=\"torch.nn.functional.max_pool1d\">max_pool1d</option>\n" +
    "                            <option value=\"torch.nn.functional.max_pool2d\">max_pool2d</option>\n" +
    "                            <option value=\"torch.nn.functional.max_pool3d\">max_pool3d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool1d\">AvgPool1d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool2d\">AvgPool2d</option>\n" +
    "                            <option value=\"torch.nn.AvgPool3d\">AvgPool3d</option>\n" +
    "                        </select>" +
    "                    </div>" +
    "                </div>" +
    "                </form>"
var searh_layer = {
    "view_layer": view_layer,
    "linear_layer": linear_layer,
    "conv1d_layer": conv1d_layer,
    "conv2d_layer": conv2d_layer
}