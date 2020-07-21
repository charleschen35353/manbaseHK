import moment from '../../node_modules/moment/dist/moment.js';

moment.locale('zh-hk');

const individual_register_on_load = () => {
  // Defining the string fields
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

  const ANIMATION_DURATION = 100;

  // Define a utility scroll-to-top function
  // with the correct duration for UX
  const scrollTop = () => $("html, body").animate({ scrollTop: 0 }, ANIMATION_DURATION);

  // Define a function which checks if a gender is selected
  const checkGenderSelection = () => {
    let selected = false;

    $('.ind_register_genders').each((_, el) => {
      $(el).removeClass('border-danger');

      if ($(el).children("input:first").is(":checked")) {
        selected = true;
      }
    })

    if (!selected) {
      $('.ind_register_genders').each((_, el) => {
        $(el).addClass('border-danger');
      })
    }

    return selected;
  }

  // Copying input fields values into respective confirm fields
  // in the last section
  for (const field of fields) {
    $(`#confirm_${field}`).html($('#' + field).val());

    $(`#${field}`).on('change paste keyup', (el) => {
      const current_value = $(el.target).val();
      $(`#confirm_${field}`).html(current_value);
    });
  }

  // Auto convert the HKID letter to upper case
  $('#ind_register_hkid').on('change paste keyup', el => {
    $(el.target).val($(el.target).val().toUpperCase());
  })


  // Block Radio Buttons
  for (const field_name of ["ind_register_gender", "ind_register_edu_level"]) {
    $(`.${field_name}s`).each((_, el) => {
      const radio = $(el).children('input:first');
      const label = $(el).children("label:first");

      // Initial Copy
      if (radio.is(":checked")) {
        $(`#confirm_${field_name}`).html(label.html());
        radio.parent().addClass('bg-primary text-white').removeClass('bg-white text-dark');
      }

      $(el).click(() => {
        $(radio).prop('checked', true).change();
      });

      $(radio).change((el) => {
        $(`#confirm_${field_name}`).html(label.html());
        $(`.${field_name}s`).each((_, el) => {
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

    if (checkbox.is(':checked')) {
      checkbox.parent().addClass('bg-primary text-white').removeClass('bg-white text-dark');
    }

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

  // Initial Show & focus of Section 1
  $('#ind_reg_sec_1').show();
  $('#ind_register_account').focus();

  // Section 1 Button
  $('#ind_reg_sec_1_next').click(() => {
    let error = false;

    for (const el of section_1_fields) {
      $(`#${el}`).removeClass('is-valid is-invalid');
      $(`#${el}_error`).empty();
    }

    // account must be filled
    // TODO: Is there a lower limit on the account name?
    if ($('#ind_register_account').val().length == 0) {
      error = true;
      $('#ind_register_account').addClass('is-invalid');

      $('#ind_register_account_error').append(
        "<p class='error'>帳號不能為空。</p>"
      );
    } else {
      $('#ind_register_account').addClass('is-valid');
    }

    // Password policy
    if ($('#ind_register_password').val().length < 8) {
      error = true;
      $('#ind_register_password').addClass('is-invalid');

      $('#ind_register_password_error').append(
        "<p class='error'>您的密碼必須有至少 8 個字元。</p>"
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
        "<p class='error'>您重複輸入的密碼必須與上面的相同。</p>"
      );
    } else {
      $('#ind_register_confirm_password').addClass('is-valid');
    }

    scrollTop();

    if (error) return;

    $('#ind_reg_sec_1').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => {
        $('#ind_reg_sec_2').fadeToggle();
        $('#ind_register_c_name').focus();
      },
    });
  });

  // Section 2 Buttons
  $('#ind_reg_sec_2_prev').click(() => {
    scrollTop();

    $('#ind_reg_sec_2').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => {
        $('#ind_reg_sec_1').fadeToggle();
        $('#ind_register_account').focus();
      },
    });
  });

  $('#ind_reg_sec_2_next').click(() => {
    let error = false;

    const hkid_regex = /([A-Z]){1,2}\d{4}/;

    for (const field of section_2_fields) {
      $(`#${field}`).removeClass('is-valid is-invalid');
      $(`#${field}_error`).empty();
    }

    if ($('#ind_register_c_name').val().length == 0) {
      error = true;
      $('#ind_register_c_name').addClass('is-invalid');

      $('#ind_register_c_name_error').append(
        "<p class='error'>您必須提供您的中文全名。</p>"
      );
    } else {
      $('#ind_register_c_name').addClass('is-valid');
    }

    // No Validation for English Name and Nick Name
    $('#ind_register_e_name').addClass('is-valid');
    $('#ind_register_nickname').addClass('is-valid');

    if (!(hkid_regex.test($('#ind_register_hkid').val()))) {
      error = true;
      $('#ind_register_hkid').addClass('is-invalid');

      $('#ind_register_hkid_error').append(
        "<p class='error'>您的身分證號碼無效。請核對並重新輸入。</p>"
      );
    } else {
      $('#ind_register_hkid').addClass('is-valid');
      $('#ind_register_hkid_error').empty();
    }

    scrollTop();

    if (error) return;

    $('#ind_reg_sec_2').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => {
        $('#ind_reg_sec_3').fadeToggle();
        $('#ind_register_tel').focus();
      },
    });
  });

  // Section 3 Buttons
  $('#ind_reg_sec_3_prev').click(() => {
    scrollTop();
    $('#ind_reg_sec_3').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => {
        $('#ind_reg_sec_2').fadeToggle();
        $('#ind_register_c_name').focus();
      },
    });
  });

  $('#ind_reg_sec_3_next').click(() => {
    let error = false;
    const email_regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

    for (const field of section_3_fields) {
      $(`#${field}`).removeClass('is-valid is-invalid');
      $(`#${field}_error`).empty();
    }

    // Must provide a valid phone number
    if ($('#ind_register_tel').val().length != 8 || !(['5', '6', '7', '8', '9'].includes($('#ind_register_tel').val().charAt(0)))) {
      error = true;
      $('#ind_register_tel').addClass('is-invalid');

      const error_msg = $('#ind_register_tel').val().length != 8 ? '聯絡電話必須是 8 個數字。' : '您的電話必須是有效的香港電話號碼。';

      $('#ind_register_tel_error').append(
        `<p class='error'>${error_msg}</p>`
      );
    } else {
      $('#ind_register_tel').addClass('is-valid');
    }

    // Must provide a valid email address
    if (!(email_regex.test($('#ind_register_email').val()))) {
      error = true;

      $('#ind_register_email').addClass('is-invalid');

      $('#ind_register_email_error').append(
        "<p class='error'>您必須提供有效的電子郵箱地址。</p>"
      );
    } else {
      $('#ind_register_email').addClass('is-valid');
    }

    if (!(checkGenderSelection())) {
      error = true;

      $('#ind_register_gender_error').append(
        "<p class='error'>請選擇您的性別。</p>"
      );
    } else {
      $('#ind_register_gender_error').empty();
    }

    // Date Of Birth must be present, and applicants must be at least 15 years old
    let input_dob = moment($('#ind_register_dob').val(), "YYYY-MM-DD", true);
    let valid_age = moment().subtract(15, "years");

    if (!(input_dob.isValid() && input_dob < valid_age)) {
      error = true;

      $('#ind_register_dob').addClass('is-invalid');

      const error_msg = input_dob.isValid() ? '對不起，您必須年滿 15 歲，方能申請 Man<span class="text-primary">base</span> 賬號。' : '您輸入的出生日期無效。請重新輸入。';

      $('#ind_register_dob_error').append(
        `<p class='error'>${error_msg}</p>`
      );
    } else {
      $('#ind_register_dob').addClass('is-valid');
    }

    scrollTop();

    if (error) return;

    $('#ind_reg_sec_3').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => {
        $('#ind_reg_sec_4').fadeToggle();
        $('.ind_register_edu_levels')[0].focus();
      },
    });
  });

  // Section 4 Buttons
  $('#ind_reg_sec_4_prev').click(() => {
    scrollTop();

    $('#ind_reg_sec_4').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => {
        $('#ind_reg_sec_3').fadeToggle();
        $('#ind_register_tel').focus();
      },
    });
  });

  $('#ind_reg_sec_4_next').click(() => {
    // TODO: Client-side Validation

    $('#ind_register_other_lang').addClass('is-valid');

    // Update Language Label
    updateLangLabel();

    // Fill in Empty Confirm Values
    $(".ind-reg-confirm").each((_, element) => {
      if ($(element).html() == '') {
        $(element).html("<span class='text-info'>未填寫</span>");
      }
    });

    scrollTop();

    $('#ind_reg_sec_4').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => {
        $('#ind_reg_sec_5').fadeToggle();
      },
    });
  });

  // Section 5 Button
  $('#ind_reg_sec_5_prev').click(() => {
    scrollTop();

    $('#ind_reg_sec_5').fadeToggle({
      duration: ANIMATION_DURATION,
      done: () => {
        $('#ind_reg_sec_4').fadeToggle();
        $('.ind_register_edu_levels')[0].focus();
      },
    });
  });

  const updateLangLabel = () => {
    let selected = [];

    $('.ind_reg_langs').each((_, el) => {
      if ($(el).children('input:first').is(':checked')) {
        selected.push($(el).children('label:first').html());
      }
    });

    if ($('#ind_register_other_lang').val() != '') {
      selected.push($('#ind_register_other_lang').val());
    }

    $('#confirm_ind_register_lang').html(selected.join(", "));
  }

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

export default individual_register_on_load;