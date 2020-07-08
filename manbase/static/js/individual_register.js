const individual_register_on_load = () => {
    // Initial Show of Section 1
    $('#ind_reg_sec_1').show();

    // Section 1 Button

    $('#ind_reg_sec_1_next').click(() => {
        // TODO: Client-side Validation

        $('#ind_reg_sec_1').fadeToggle({
            duration: 200,
            done: () => $('#ind_reg_sec_2').fadeToggle()
        });
    });

    // Section 2 Buttons
    $('#ind_reg_sec_2_prev').click(() => {
        $('#ind_reg_sec_2').fadeToggle({
            duration: 200,
            done: () => $('#ind_reg_sec_1').fadeToggle()
        });
    });

    $('#ind_reg_sec_2_next').click(() => {
        // TODO: Client-side Validation

        $('#ind_reg_sec_2').fadeToggle({
            duration: 200,
            done: () => $('#ind_reg_sec_3').fadeToggle()
        });
    });


    // Section 3 Buttons
    $('#ind_reg_sec_3_prev').click(() => {
        $('#ind_reg_sec_3').fadeToggle({
            duration: 200,
            done: () => $('#ind_reg_sec_2').fadeToggle()
        });
    });

    $('#ind_reg_sec_3_next').click(() => {
        // TODO: Client-side Validation

        $('#ind_reg_sec_3').fadeToggle({
            duration: 200,
            done: () => $('#ind_reg_sec_4').fadeToggle()
        });
    });

    // Section 4 Buttons
    $('#ind_reg_sec_4_prev').click(() => {
        $('#ind_reg_sec_4').fadeToggle({
            duration: 200,
            done: () => $('#ind_reg_sec_3').fadeToggle()
        });
    });

    $('#ind_reg_sec_4_next').click(() => {
        // TODO: Client-side Validation

        $('#ind_reg_sec_4').fadeToggle({
            duration: 200,
            done: () => $('#ind_reg_sec_5').fadeToggle()
        });
    });

    // Section 5 Button
    $('#ind_reg_sec_5_prev').click(() => {
        $('#ind_reg_sec_5').fadeToggle({
            duration: 200,
            done: () => $('#ind_reg_sec_4').fadeToggle()
        });
    });

    // Block Radio Buttons

    for (const class_name of ['.ind_register_genders', '.ind_reg_edu_levels']) {
        $(class_name).each((_, el) => {

            const radio = $(el).children("input:first");

            $(el).click(() => {
                $(radio).prop("checked", true).change();
            });

            $(radio).change((el) => {
                $(class_name).each((_, el) => {
                    $(el).removeClass("bg-primary text-white").addClass("bg-white text-dark");
                });

                if ($(el.target).is(':checked')) {
                    $(el.target).parent().addClass("bg-primary text-white").removeClass("bg-white text-dark");
                }
            });
        });
    }

    // Language Checkboxes
    $('.ind_reg_langs').each((_, el) => {
        const checkbox = $(el).children("input:first");

        $(el).click(() => {
            $(checkbox).prop("checked", !$(checkbox).is(':checked')).change();
        });

        $(checkbox).change(el => {
            if ($(el.target).is(':checked')) {
                $(el.target).parent().addClass("bg-primary text-white").removeClass("bg-white text-dark");
            } else {
                $(el.target).parent().removeClass("bg-primary text-white").addClass("bg-white text-dark");
            }
        });
    });



    // Auto-Formatting

    /* Suspending
    $('#ind_reg_tel_num').on("change paste keyup", (el) => {
        let current_value = $(el.target).val();
        const regex = /[0-9]{5,}/g;

        // When backspace is pressed
        if (el.keyCode && el.keyCode == 8) {
            // If there are only 5 characters, remove the last dash
            if ($(el.target).val().length == 5) {
                $(el.target).val(current_value.substr(0, 4));
            }
            // Else if there are 4 digits
        } else if ($(el.target).val().length == 4) {
            // Append a dash
            $(el.target).val(current_value + "-");
            // Else if there are 5+ digits
        } else if ($(el.target).val().match(regex)) {
            // Add back the dash
            $(el.target).val(current_value.substr(0, 4) + "-" + current_value.slice(4));
        }
    });
    */
};