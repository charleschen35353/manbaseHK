const init = () => {
    $('#spinner').css('visibility', 'visible');
    $("html, body").animate({ scrollTop: 0 }, "fast");

    if (document.querySelector('#business_register')) {
        business_register_on_load();
    }
    if (document.querySelector('#individual_register')) {
        individual_register_on_load();
    }

    $('#spinner').css('visibility', 'hidden');
}

const clickedLink = () => {
    $('#spinner').css('visibility', 'visible');
}

init();

// TODO: Add the Form Plugin for Swup

const swup = new Swup();

swup.on('contentReplaced', init);
swup.on('clickLink', clickedLink);
