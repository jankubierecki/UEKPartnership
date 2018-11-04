(function ($) {
    $(function () {
        $("#id_name").after("<div id='name_autocomplete'></div>");
        $("#id_name").bindWithDelay("keyup change", function (e) {
            let url = '';
            if (COMPANY_ID === 'None') {
                url = "/company_autocomplete/?term=" + e.currentTarget.value
            } else {
                url = "/company_autocomplete/?term=" + e.currentTarget.value + "&id=" + COMPANY_ID;
            }
            $.get(url, function (data) {
                let html = "<ul>";
                for (let company of data) {
                    let name = company["name"];
                    let url = company["url"];
                    html += "<li><a href='" + url + "'>" + name + "</a></li>";
                }

                html += "</ul>";

                $("#name_autocomplete").html(html);
            });
        }, 80);

    })
}(django.jQuery));






