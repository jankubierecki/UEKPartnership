(function ($) {
    let company_id = "#id_company";
    let company_value;

    function update_select(source_id, target_id, source_val) {
        if (source_val["currentValue"] == null) {
            $(target_id).prop("disabled", true);
        }
        $(source_id).on('select2:select', function (e) {
            source_val["currentValue"] = e.params.data['id'];
            $(target_id).prop("disabled", false);
            $(target_id).val(null).trigger('change');
        });
        $(source_id).on('change', function (e) {
            source_val["currentValue"] = e.currentTarget.value;
            $(target_id).prop("disabled", false);
            $(target_id).val(null).trigger('change');
        });

        try {
            $(target_id).select2('destroy');
        } catch (e) {

        }
        $(target_id).djangoAdminSelect2({
            ajax: {
                data: function (params) {

                    return {
                        term: params.term,
                        page: params.page,
                        parent_id: source_val["currentValue"]
                    };
                }

            }

        });

    }

    function onElementInserted(containerSelector, elementSelector, callback) {

        var onMutationsObserved = function (mutations) {
            mutations.forEach(function (mutation) {
                if (mutation.addedNodes.length) {
                    var elements = $(mutation.addedNodes).find(elementSelector);
                    for (var i = 0, len = elements.length; i < len; i++) {
                        callback(elements[i]);
                    }
                }
            });
        };

        var target = $(containerSelector)[0];
        var config = {childList: true, subtree: true};
        var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
        var observer = new MutationObserver(onMutationsObserved);
        observer.observe(target, config);

    }

    $(function () {
        company_value = {currentValue: $(company_id).val()};

        //update fields
        $(".field-company_contact_persons select.select2-hidden-accessible").each(function () {
            update_select(company_id, this, company_value)
        })
        onElementInserted("body", ".field-company_contact_persons select.select2-hidden-accessible", function () {
            $(".field-company_contact_persons select.select2-hidden-accessible").each(function () {
                update_select(company_id, this, company_value)
            })
        })


        $(".field-university_contact_persons select.select2-hidden-accessible").each(function () {
            let institute_id = $(this).closest(".dynamic-contracts").find(".field-institute_unit select")
            let institute_unit_value = {currentValue: $(institute_id).val()};
            update_select(institute_id, this, institute_unit_value)
        })

        onElementInserted("body", ".field-university_contact_persons select.select2-hidden-accessible", function () {
            $(".field-company_contact_persons select.select2-hidden-accessible").each(function () {
                let institute_id = $(this).closest(".dynamic-contracts").find(".field-institute_unit select")
                let institute_unit_value = {currentValue: $(institute_id).val()};
                update_select(institute_id, this, institute_unit_value)
            })
        })


    })
}(django.jQuery));