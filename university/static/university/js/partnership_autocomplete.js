(function ($) {
    $(function () {
        $("#id_name").after("<div id='name_autocomplete'></div>");
        $("#id_name").bindWithDelay("keyup change", function (e) {
            let url = '';
            if (PARTNERSHIP_ID === 'None') {
                url = "/partnership_autocomplete/?term=" + e.currentTarget.value
            } else {
                url = "/partnership_autocomplete/?term=" + e.currentTarget.value + "&id=" + PARTNERSHIP_ID;
            }
            $.get(url, function (data) {
                let html = "<ul>";
                for (let partnership of data) {
                    let name = partnership["name"];
                    let url = partnership["url"];
                    html += "<li><a href='" + url + "'>" + name + "</a></li>";
                }
                html += "</ul>"
                $("#name_autocomplete").html(html);
            });
        }, 80);

    })
}(django.jQuery));






