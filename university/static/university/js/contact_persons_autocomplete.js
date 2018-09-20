(function ($) {

    //todo change this

    let contract_id;
    let set_id;
    let company_id = "#id_contracts-" + contract_id + "-company";
    let institute_unit_id = "#id_contracts-" + contract_id + "-institute_unit";
    let university_contact_person_id = "#id_contracts-" + contract_id + "-contracttuuniversitycontactperson_set-" + set_id + "-university_contact_person";
    let company_contact_person_id = "#id_contracts-" + contract_id + "-contracttocompanycontactperson_set-" + set_id + "-company_contact_person";
    let company_value;
    let institute_unit_value;

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