
function update_brightness() {
    let slider_brightness = document.getElementById('brightness');
    send_brightness(slider_brightness.value);
}

function update_pattern_duration() {
    let input_pattern_duration = document.getElementById('pattern_duration');
    send_pattern_duration(input_pattern_duration.value);
}


function init() {
    console.group('init..');
    // setup change events
    let slider_brightness = document.getElementById('brightness');
    slider_brightness.addEventListener('input', update_brightness);
    let input_pattern_duration = document.getElementById('pattern_duration');
    input_pattern_duration.addEventListener('change', update_pattern_duration);

    // update current UI with values from server
    get_brightness();
    get_pattern_duration();
    console.log('done.');
    console.groupEnd();
}

document.addEventListener('DOMContentLoaded', function() {
    init();
},false);
