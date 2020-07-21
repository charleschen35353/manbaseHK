const login_on_load = () => {
    const fields = [
        'login_account',
        'login_password'
    ];

    const ANIMATION_DURATION = 100;

    // Define a utility scroll-to-top function
    // with the correct duration for UX
    const scrollTop = () => $("html, body").animate({ scrollTop: 0 }, ANIMATION_DURATION);

    $('#login_submit_btn').click((e) => {
        e.preventDefault();

        let error = false;

        for (const field of fields) {
            $(`#${field}`).removeClass('is-valid is-invalid');
            $(`#${field}_error`).empty();
        }

        if ($('#login_account').val().length == 0) {
            error = true;

            $('#login_account').addClass('is-invalid');

            $('#login_account_error').append(
                "<p class='error'>帳號不能為空。</p>"
            );
        } else {
            $('#login_account').addClass('is-valid');
        }

        if ($('#login_password').val().length == 0) {
            error = true;

            $('#login_password').addClass('is-invalid');

            $('#login_password_error').append(
                "<p class='error'>密碼不能為空。</p>"
            );
        } else {
            $('#login_password').addClass('is-valid');
        }

        scrollTop();

        if (error) return;

        $('#login_submit_btn').unbind('click').click();
    });

    $('#form_login').on('keydown', (e) => {
        if (e.which == 13) {
            e.preventDefault();

            $('#login_submit_btn').click();
        }
    });
};

export default login_on_load;