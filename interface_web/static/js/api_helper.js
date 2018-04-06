

function send_GET_request(url, content, onready_function) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        onready_function(xhttp);
    };
    xhttp.open('GET', url, true);
    xhttp.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhttp.send(JSON.stringify(content));
}

function send_PUT_request(url, content, onready_function) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        onready_function(xhttp);
    };
    xhttp.open('PUT', url, true);
    xhttp.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhttp.send(JSON.stringify(content));
}


// high-level helpers

function send_brightness(value) {
    // console.log('send new brightness value.');
    var send_url = 'api/brightness';
    var send_content = {
        'value': value,
    };
    send_PUT_request(
        send_url,
        send_content,
        function(xhttp) {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var response = JSON.parse(xhttp.responseText);
                // document.getElementById('xxxx').innerHTML = response;
                console.info('pattern/brightness', response);
            }
        }
    );
}

function get_brightness() {
    var send_url = 'api/brightness';
    var send_content = {};
    send_GET_request(
        send_url,
        send_content,
        function(xhttp) {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var response = JSON.parse(xhttp.responseText);
                console.info('pattern/brightness', response);
                let el = document.getElementById('brightness');
                console.info('el brightness', el);
                el.value = response;
            }
        }
    );
}

function send_pattern_duration(value) {
    // console.log('send new pattern_duration value.');
    var send_url = 'api/pattern_duration';
    var send_content = {
        'value': value,
    };
    send_PUT_request(
        send_url,
        send_content,
        function(xhttp) {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var response = JSON.parse(xhttp.responseText);
                // document.getElementById('xxxx').innerHTML = response;
                console.info('pattern/duration', response);
            }
        }
    );
}

function get_pattern_duration() {
    var send_url = 'api/pattern_duration';
    var send_content = {};
    send_GET_request(
        send_url,
        send_content,
        function(xhttp) {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var response = JSON.parse(xhttp.responseText);
                console.info('pattern/duration', response);
                let el = document.getElementById('pattern_duration');
                console.info('el pattern_duration', el);
                el.value = response;
            }
        }
    );
}
