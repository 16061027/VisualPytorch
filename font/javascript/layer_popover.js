var view_layer = "<form class=\"form-horizontal\" role=\"form\"><div class=\"form-group\">" +
    "                    <label class=\"col-sm-5 control-label\">shape</label>" +
    "                            <div class=\"col-sm-5\">" +
    "                        <input type=\"text\"; class=\"form-control\" placeholder=\"1\">" +
    "                    </div>" +
    "                </div>" +
    "<button type=\"button\" class=\"btn btn-success\" style=\"width: 150px\" id=\"id_anchor\">确认</button>"+
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
    "<button type=\"button\" class=\"btn btn-success\" style=\"width: 150px\" id=\"id_anchor\" onclick=\"save_attr(this)\">确认</button>"+
    "                </form>"

var searh_layer = {
    "view_layer": view_layer,
    "linear_layer": linear_layer
}