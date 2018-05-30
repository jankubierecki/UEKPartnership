(function ($) {
    let company_id = "#id_contract-0-company";
    let institute_unit_id = "#id_contract-0-institute_unit";
    let university_contact_person_id = "#id_university_contact_person";
    let company_contact_person_id = "#id_company_contact_person";
    let company_value;
    let institute_unit_value;

    function update_select(source_id, target_id, source_val) {
        $(source_id).on('select2:select', function (e) {
            source_val["currentValue"] = e.params.data['id'];
            $(target_id).val(null).trigger('change');
        });

        $(target_id).select2('destroy');
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

    $(function () {
        company_value = {currentValue: $(company_id).val()};
        institute_unit_value = {currentValue: $(institute_unit_id).val()};


        update_select(company_id, company_contact_person_id, company_value);
        update_select(institute_unit_id, university_contact_person_id, institute_unit_value);
    })
}(django.jQuery));






