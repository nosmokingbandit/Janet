var link_bind = function(e) {
    e.preventDefault();
    var anchor = e.target || e.srcElement;
    if (anchor.getAttribute("data-bind") != "true")
        return true;
    var call = anchor.href;
    var params = anchor.getAttribute("data-params");

    if (params !== null)
        eval(call + "('" + params + "')");
    else
        eval(call + "()");
    return false;
};

var form_bind = function (e) {
    e.preventDefault();
    var form = e.target || e.srcElement;
    if (form.getAttribute("data-bind") != "true")
        return true;
    var action = form.action;

    var formdata = {};
    for (var i = 0, ii = form.length; i < ii; ++i) {
        var input = form[i];
        if (input.name && input.type !== "file")
            formdata[input.name] = input.value;
    }

    var params = form.getAttribute("data-params");

    exec = action + "('" + JSON.stringify(formdata);
    exec += params !== null ? ("', '" + params) : "";
    exec += "')";
    console.log(exec);
    eval(exec);
    return false;
};

var file_dialog = function (e) {
    e.preventDefault();

    var id_of_pseudo_filebox = e.target.getAttribute("data-display");
    var ext_filter_json = e.target.getAttribute("data-filter");
    var filemode = e.target.getAttribute("data-filemode");

    if (ext_filter_json === null || ext_filter_json === "null")
        ext_filter_json = '[{"title": "Any file", "extensions": "*.*"}]';

    if (filemode === null || filemode === "null")
        filemode = 'file';

    var dialog = GUIHelper.file_dialog(filemode, ext_filter_json);
    if(dialog){
        document.getElementById(id_of_pseudo_filebox).value = dialog;
    }

    return false;
};


var bind_all = function () {
    var anchors = document.getElementsByTagName("a");
    var forms = document.getElementsByTagName("form");
    for (var i = anchors.length - 1; i >= 0; i--) {
        if(!anchors[i].classList.contains("htmlpy-activated")){
            anchors[i].onclick = link_bind;
            anchors[i].classList.add("htmlpy-activated");
        }
    }

    for (var fi = forms.length - 1; fi >= 0; fi--) {
        if(!forms[fi].classList.contains("htmlpy-activated")){
            forms[fi].onsubmit = form_bind;
            form = forms[fi];
            for (var i = form.length - 1; i >= 0; i--) {
                var input = form[i];
                if (input.type === "file") {
                    var fileboxname = input.getAttribute("name");
                    var value = input.getAttribute("value") || "";
                    var disabledInput = document.createElement("input");

                    disabledInput.setAttribute("disabled", "disabled");
                    disabledInput.setAttribute("name", fileboxname);
                    disabledInput.setAttribute("id", fileboxname + "_path");
                    disabledInput.setAttribute("value", value);

                    var button = document.createElement("button");
                    if(input.getAttribute("data-filemode") == "directory"){
                        button.innerHTML = "Choose directory";
                    } else {
                        button.innerHTML = "Choose file";
                    }

                    button.setAttribute("data-display", fileboxname + "_path");
                    button.setAttribute("data-filter", input.getAttribute("data-filter") || "[]");
                    button.setAttribute("data-filemode", input.getAttribute("data-filemode"));
                    button.setAttribute("data-for", input.getAttribute("name"))
                    button.className += "_htmlpy_button";
                    button.onclick = file_dialog;

                    input.parentNode.insertBefore(disabledInput, input.nextSibling);
                    input.parentNode.insertBefore(button, disabledInput.nextSibling);

                    input.style.display = "none";
                }
            }
            forms[fi].classList.add("htmlpy-activated");
        }
    }
};

bind_all();
document.body.addEventListener("DOMNodeInserted", bind_all);
document.body.classList.add("htmlPy-active");
