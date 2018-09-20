(function ($) {
    $(function () {
        $("#id_name").after("<div id='name_autocomplete'></div>");
        $("#id_name").bindWithDelay("keyup change", function (e) {
            let url = '';
            if (INSTITUTEUNIT_ID === 'None') {
                url = "/institute_unit_autocomplete/?term=" + e.currentTarget.value
            } else {
                url = "/institute_unit_autocomplete/?term=" + e.currentTarget.value + "&id=" + INSTITUTEUNIT_ID;
            }
            $.get(url, function (data) {
                let html = "<ul style='padding-left:30%;'>";
                for (let institute_unit of data) {
                    let name = institute_unit["name"];
                    let url = institute_unit["url"];
                    html += "<li><a href='" + url + "'>" + name + "</a></li>";
                }
                html += "</ul>";


                $("#name_autocomplete").html(html);
            });
        }, 80);

    })
}(django.jQuery));






