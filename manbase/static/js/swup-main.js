import individual_register_on_load from './modules/individual_register.js';
import business_register_on_load from './modules/business_register.js';

const init = () => {
    $('#spinner').css('visibility', 'visible');
    $("html, body").animate({ scrollTop: 0 }, 100);

    if (document.querySelector('#business_register')) {
        business_register_on_load();
    }
    if (document.querySelector('#individual_register')) {
        individual_register_on_load();
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
