const business_register_on_load = () => {

    // VERIFICATIONS
    $('#confirm_account_name').html($('#bus_reg_account').val());
    $('#confirm_company_chinese_name').html($('#bus_reg_company_name_chinese').val());
    $('#confirm_company_english_name').html($('#bus_reg_company_name_english').val());
    $('#confirm_person_in_charge').html($('#bus_reg_person_in_charge').val());
    $('#confirm_phone_num').html($('#bus_reg_phone_num').val());
    $('#confirm_business_email').html($('#bus_reg_email').val());


    $('#bus_reg_account').on('change paste keyup', el => {
        const current_value = $(el.target).val();
        $('#confirm_account_name').html(current_value);
    });


    $('#bus_reg_company_name_chinese').on('change paste keyup', el => {
        const current_value = $(el.target).val();
        $('#confirm_company_chinese_name').html(current_value);
    });


    $('#bus_reg_company_name_english').on('change paste keyup', el => {
        const current_value = $(el.target).val();
        $('#confirm_company_english_name').html(current_value);
    });


    $('#bus_reg_person_in_charge').on('change paste keyup', el => {
        const current_value = $(el.target).val();
        $('#confirm_person_in_charge').html(current_value);
    });


    $('#bus_reg_phone_num').on('change paste keyup', el => {
        const current_value = $(el.target).val();
        $('#confirm_phone_num').html(current_value);
    });


    $('#bus_reg_email').on('change paste keyup', el => {
        const current_value = $(el.target).val();
        $('#confirm_business_email').html(current_value);
    });


    // BUTTONS AND VALIDATIONS

    const ANIMATION_DURATION = 200;

    $('#bus_reg_sec_1').show();

    $('#bus_reg_sec_1_next').click(() => {
        // Client-side Validation
        const account = $('#bus_reg_account');
        const password = $('#bus_reg_password');
        const repeat_password = $('#bus_reg_repeat_password');

        const account_errors = $('#bus_reg_account_errors');
        const password_errors = $('#bus_reg_password_errors');
        const repeat_password_errors = $('#bus_reg_repeat_password_errors');

        let error = false;

        for (el of [account, password, repeat_password]) {
            $(el).removeClass('is-valid is-invalid');
        }

        for (el of [account_errors, password_errors, repeat_password_errors]) {
            $(el).empty();
        }

        // account must be filled
        // TODO: Is there a lower limit on the account name?
        if ($(account).val().length == 0) {
            error = true;
            $(account).addClass('is-invalid');

            $(account_errors).append("<p class='error'>帳號不能為空</p>");
        } else {
            $(account).addClass('is-valid');
        }

        // TODO: Discuss the password policy
        // ASSUMPTION: Password length >= 8
        if ($(password).val().length < 8) {
            error = true;
            $(password).addClass('is-invalid');

            $(password_errors).append("<p class='error'>您的密碼必須有至少 8 個字元。</p>")
        } else {
            $(password).addClass('is-valid');
        }

        if ($(repeat_password).val() != $(password).val()) {
            error = true;
            $(repeat_password).addClass('is-invalid');

            $(repeat_password_errors).append("<p class='error'>您重複輸入的密碼必須與上面的相同。</p>")
        } else {
            $(repeat_password).addClass('is-valid');
        }

        // Exit if the data is invalid
        if (error) return;

        // Otherwise, go to the next section
        $('#bus_reg_sec_1').fadeToggle({
            duration: ANIMATION_DURATION,
            done: () => {
                $('#bus_reg_sec_2').fadeToggle();
                $('#bus_reg_company_name_chinese').focus();
            }
        });
    });

    $('#bus_reg_sec_2_prev').click(() => {
        $('#bus_reg_sec_2').fadeToggle({
            duration: ANIMATION_DURATION,
            done: () => {
                $('#bus_reg_sec_1').fadeToggle();
            }
        });
    });

    $('#bus_reg_sec_2_next').click(() => {
        // Client-side Validation
        const c_name = $('#bus_reg_company_name_chinese');
        const e_name = $('#bus_reg_company_name_english');

        const c_name_errors = $('#bus_reg_company_name_chinese_errors');
        const e_name_errors = $('#bus_reg_company_name_english_errors');

        let error = false;

        for (const el of [c_name, e_name]) {
            $(el).removeClass('is-valid is-invalid');
        }

        for (const el of [c_name_errors, e_name_errors]) {
            $(el).empty();
        }

        // Chinese Name must exist
        if ($(c_name).val().length == 0) {
            error = true;
            $(c_name).addClass('is-invalid');
            // TODO: Update to Chinese warning
            $(c_name_errors).append("<p class='error'>您必須提供企業的中文名稱。</p>");
        } else {
            $(c_name).addClass('is-valid')
        }

        $(e_name).addClass('is-valid');

        // Exit if data is invalid
        if (error) return;

        // Otherwise, go to the next section
        $('#bus_reg_sec_2').fadeToggle({
            duration: ANIMATION_DURATION,
            done: () => {
                $('#bus_reg_sec_3').fadeToggle();
                $('#bus_reg_person_in_charge').focus();
            }
        });
    });

    $('#bus_reg_sec_3_prev').click(() => {
        $('#bus_reg_sec_3').fadeToggle({
            duration: ANIMATION_DURATION,
            done: () => {
                $('#bus_reg_sec_2').fadeToggle();
            }
        });
    });

    $('#bus_reg_sec_3_next').click(() => {
        const pic = $('#bus_reg_person_in_charge');
        const phone = $('#bus_reg_phone_num');
        const email = $('#bus_reg_email');

        const pic_errors = $('#bus_reg_person_in_charge_errors');
        const phone_errors = $('#bus_reg_phone_num_errors');
        const email_errors = $('#bus_reg_email_errors');

        let error = false;

        const email_regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/


        for (const el of [pic, phone, email]) {
            $(el).removeClass('is-valid is-invalid');
        }

        for (const el of [pic_errors, phone_errors, email_errors]) {
            $(el).empty();
        }

        // Must provide Person-in-charge
        if ($(pic).val().length == 0) {
            error = true;
            $(pic).addClass('is-invalid');
            $(pic_errors).append("<p class='error'>您必須提供聯絡人的名稱。</p>");
        } else {
            $(pic).addClass('is-valid');
        }

        // Must provide a valid phone number
        if ($(phone).val().length != 8 || !(["2", "3", "5", "6", "7", "9"].includes($(phone).val().charAt(0)))) {
            error = true;
            $(phone).addClass('is-invalid');

            error_msg = $(phone).val().length != 8 ? "聯絡電話必須是 8 個數字。" : "您的電話必須是有效的香港電話號碼。";

            $(phone_errors).append("<p class='error'>" + error_msg + "</p>")
        } else {
            $(phone).addClass('is-valid');
        }

        // Must provide an email address that is valid
        if (!(email_regex.test($(email).val()))) {
            error = true;
            $(email).addClass('is-invalid');
            $(email_errors).append("<p class='error'>您必須提供有效的電子郵箱地址。</p>");
        } else {
            $(email).addClass('is-valid');
        }

        if (error) return;

        // Fill in Empty Confirm Values
        $(".bus-reg-confirm").each((index, element) => {
            if ($(element).html() == '') {
                $(element).html("<span class='text-info'>未填寫</span>");
            }
        });

        $('#bus_reg_sec_3').fadeToggle({
            duration: ANIMATION_DURATION,
            done: () => {
                $('#bus_reg_sec_4').fadeToggle();
            }
        });
    });

    $('#bus_reg_sec_4_prev').click(() => {
        $('#bus_reg_sec_4').fadeToggle({
            duration: ANIMATION_DURATION,
            done: () => {
                $('#bus_reg_sec_3').fadeToggle();
            }
        });
    });

    $('#business_register').on('keydown', e => {
        if (e.which == 13) {
            e.preventDefault();

            if ($('#bus_reg_sec_1').is(":visible")) {
                $('#bus_reg_sec_1_next').click();
            } else if ($('#bus_reg_sec_2').is(":visible")) {
                $('#bus_reg_sec_2_next').click();
            } else if ($('#bus_reg_sec_3').is(":visible")) {
                $('#bus_reg_sec_3_next').click();
            } else if ($('#bus_reg_sec_4').is(":visible")) {
                $('#business_register').submit();
            }
        }
    });
};
