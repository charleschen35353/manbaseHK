const business_register_on_load = () => {

    $('#bus_reg_sec_1').show();

    $('#bus_reg_sec_1_next').click(() => {
        // TODO: Client Validate info


        $('#bus_reg_sec_1').fadeToggle({
            duration: 200,
            done: () => {
                $('#bus_reg_sec_2').fadeToggle();
            }
        });
    });

    $('#bus_reg_sec_2_prev').click(() => {
        $('#bus_reg_sec_2').fadeToggle({
            duration: 200,
            done: () => {
                $('#bus_reg_sec_1').fadeToggle();
            }
        });
    });

    $('#bus_reg_sec_2_next').click(() => {
        // TODO: Client Validate info

        $('#bus_reg_sec_2').fadeToggle({
            duration: 200,
            done: () => {
                $('#bus_reg_sec_3').fadeToggle();
            }
        });
    });

    $('#bus_reg_sec_3_prev').click(() => {
        $('#bus_reg_sec_3').fadeToggle({
            duration: 200,
            done: () => {
                $('#bus_reg_sec_2').fadeToggle();
            }
        });
    });
};
