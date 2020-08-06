import individual_register_on_load from './modules/individual_register.js';
import business_register_on_load from './modules/business_register.js';
import login_on_load from './modules/login.js';
import add_job_listing from './modules/add_job_listing.js';

const init = () => {
    $('#spinner').css('visibility', 'visible');
    $("html, body").animate({ scrollTop: 0 }, 100);

    if (document.querySelector('#business_register')) {
        business_register_on_load();

        // Delay the script by 1 second so it avoids the race condition on FIREFOX
        setTimeout(() => {
            grecaptcha.render('recaptcha', {
                sitekey: '6LftibMZAAAAAETVT1059c9ue_KF7Ftbt7LSl7rW'
            })
        }, 1000);
    }

    if (document.querySelector('#individual_register')) {
        individual_register_on_load();

        // Delay the script by 1 second so it avoids the race condition on FIREFOX
        setTimeout(() => {
            grecaptcha.render('recaptcha', {
                sitekey: '6LftibMZAAAAAETVT1059c9ue_KF7Ftbt7LSl7rW'
            })
        }, 1000);
    }

    if (document.querySelector('#form_login')) {
        login_on_load();
    }

    if (document.querySelector('#business_post_job')) {
        add_job_listing();
    }
    if (document.querySelector('#add_listing_form')) {
        add_job_listing();
    }

    $('#spinner').css('visibility', 'hidden');

    gtag('event', 'page_view', { 'send_to': 'UA-41948260-3' });

    $('.navbar-brand').click(() => {
        $('#main-nav').collapse('hide');
    });

    $('#main_content').click(() => {
        $('#main-nav').collapse('hide');
    });

    $('.nav-item').each((_, el) => {
        $(el).click(() => {
            $('#main-nav').collapse('hide');
        });
    })
}

const showSpinner = () => {
    $('#spinner').css('visibility', 'visible');
}

init();

const swup = new Swup({
    plugins: [new SwupFormsPlugin(), new SwupGaPlugin()],
    cache: false,
    containers: ["#swup"]
});

swup.on('contentReplaced', init);
swup.on('clickLink', showSpinner);
swup.on('submitForm', showSpinner);
swup.on('samePage', () => $('#spinner').css('visibility', 'hidden'));
