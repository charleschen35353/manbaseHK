const individual_register_on_load = () => {
  const section_1_fields = [
    'ind_register_account',
    'ind_register_password',
    'ind_register_confirm_password',
  ];
  const section_2_fields = [
    'ind_register_c_name',
    'ind_register_e_name',
    'ind_register_nickname',
    'ind_register_hkid',
  ];
  const section_3_fields = [
    'ind_register_tel',
    'ind_register_email',
    // Missing Gender
    'ind_register_dob',
  ];
  const section_4_fields = [
    // Missing Education
    // Missing Languages
  ];

  const fields = [
    ...section_1_fields,
    ...section_2_fields,
    ...section_3_fields,
    ...section_4_fields,
  ];

  const ANIMATION_DURATION = 200;

  // Copying input fields values into respective confirm fields
  // in the last section
  for (const field of fields) {
    $('#confirm_' + field).html($('#' + field).val());

    $('#' + field).on('change paste keyup', (el) => {
      const current_value = $(el.target).val();
      $('#confirm_' + field).html(current_value);
    });
  }

  // Initial Show of Section 1
  $('#ind_reg_sec_1').show();

  // Section 1 Button
  $('#ind_reg_sec_1_next').click(() => {
    let error = false;

    for (el of [
      'ind_register_account',
      'ind_register_password',
      'ind_register_confirm_password',
    ]) {
      $('#' + el).removeClass('is-valid is-invalid');
      $('#' + el + '_error').empty();
    }

    // account must be filled
    // TODO: Is there a lower limit on the account name?
    if ($('#ind_register_account').val().length == 0) {
      error = true;
      $('#ind_register_account').addClass('is-invalid');

      $('#ind_register_account_error').append(
        "<p class='error'>ACCOUNT_NOT_EMPTY_ERROR</p>"
      );
    } else {
      $('#ind_register_account').addClass('is-valid');
    }

    // Password policy
    if ($('#ind_register_password').val().length < 8) {
      error = true;
      $('#ind_register_password').addClass('is-invalid');

      $('#ind_register_password_error').append(
        "<p class='error'>PASSWORD_POLICY_VIOLATED</p>"
      );
    } else {
      $('#ind_register_password').addClass('is-valid');
    }

    // Repeat Password Verification
    if (
      $('#ind_register_confirm_password').val() !=
      $('#ind_register_password').val()
    ) {
      error = true;
      $('#ind_register_confirm_password').addClass('is-invalid');

      $('#ind_register_confirm_password_error').append(
        "<p class='error'>REPEAT_PASSWORD_VERIFICATION_FAILED</p>"
      );
    } else {
      $('#ind_register_confirm_password').addClass('is-valid');
    }

    if (error) return;

    $('#ind_reg_sec_1').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => $('#ind_reg_sec_2').fadeToggle(),
    });
  });

  // Section 2 Buttons
  $('#ind_reg_sec_2_prev').click(() => {
    $('#ind_reg_sec_2').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => $('#ind_reg_sec_1').fadeToggle(),
    });
  });

  $('#ind_reg_sec_2_next').click(() => {
    // TODO: Client-side Validation

    $('#ind_reg_sec_2').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => $('#ind_reg_sec_3').fadeToggle(),
    });
  });

  // Section 3 Buttons
  $('#ind_reg_sec_3_prev').click(() => {
    $('#ind_reg_sec_3').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => $('#ind_reg_sec_2').fadeToggle(),
    });
  });

  $('#ind_reg_sec_3_next').click(() => {
    // TODO: Client-side Validation

    $('#ind_reg_sec_3').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => $('#ind_reg_sec_4').fadeToggle(),
    });
  });

  // Section 4 Buttons
  $('#ind_reg_sec_4_prev').click(() => {
    $('#ind_reg_sec_4').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => $('#ind_reg_sec_3').fadeToggle(),
    });
  });

  $('#ind_reg_sec_4_next').click(() => {
    // TODO: Client-side Validation

    $('#ind_reg_sec_4').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => $('#ind_reg_sec_5').fadeToggle(),
    });
  });

  // Section 5 Button
  $('#ind_reg_sec_5_prev').click(() => {
    $('#ind_reg_sec_5').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => $('#ind_reg_sec_4').fadeToggle(),
    });
  });

  // Block Radio Buttons

  for (const class_name of ['.ind_register_genders', '.ind_reg_edu_levels']) {
    $(class_name).each((_, el) => {
      const radio = $(el).children('input:first');

      $(el).click(() => {
        $(radio).prop('checked', true).change();
      });

      $(radio).change((el) => {
        $(class_name).each((_, el) => {
          $(el)
            .removeClass('bg-primary text-white')
            .addClass('bg-white text-dark');
        });

        if ($(el.target).is(':checked')) {
          $(el.target)
            .parent()
            .addClass('bg-primary text-white')
            .removeClass('bg-white text-dark');
        }
      });
    });
  }

  // Language Checkboxes
  $('.ind_reg_langs').each((_, el) => {
    const checkbox = $(el).children('input:first');

    $(el).click(() => {
      $(checkbox).prop('checked', !$(checkbox).is(':checked')).change();
    });

    $(checkbox).change((el) => {
      if ($(el.target).is(':checked')) {
        $(el.target)
          .parent()
          .addClass('bg-primary text-white')
          .removeClass('bg-white text-dark');
      } else {
        $(el.target)
          .parent()
          .removeClass('bg-primary text-white')
          .addClass('bg-white text-dark');
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

  // Blocking the <ENTER> key from submiting
  $('#individual_register').on('keydown', (e) => {
    if (e.which == 13) {
      e.preventDefault();

      if ($('#ind_reg_sec_1').is(':visible')) {
        $('#ind_reg_sec_1_next').click();
      } else if ($('#ind_reg_sec_2').is(':visible')) {
        $('#ind_reg_sec_2_next').click();
      } else if ($('#ind_reg_sec_3').is(':visible')) {
        $('#ind_reg_sec_3_next').click();
      } else if ($('#ind_reg_sec_4').is(':visible')) {
        $('#ind_reg_sec_4_next').click();
      } else if ($('#ind_reg_sec_5').is(':visible')) {
        $('#individual_register').submit();
      }
    }
  });
};
