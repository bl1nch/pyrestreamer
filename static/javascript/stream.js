function stream_api_func(url, name, id) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url + "?name=" + name, false );
    xmlHttp.send( null );
    var obj = JSON.parse(xmlHttp.responseText);
    if (id == 'stream_status') {
        if (obj.found) {
            if (obj.online) {
                document.getElementById(id).innerHTML = "online";
                setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
            }
            else {
                document.getElementById(id).innerHTML = "offline";
                setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
            }
        }
        else {
            document.getElementById(id).innerHTML = "not found";
            setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
        }
    }
    else if (id == 'stream_ping') {
        if (obj.found) {
            if (obj.ping) {
                document.getElementById(id).innerHTML = "success";
                setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
            }
            else {
                document.getElementById(id).innerHTML = "fail";
                setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
            }
        }
        else {
            document.getElementById(id).innerHTML = "not found";
            setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
        }
    }
    else if (id == 'stream_stop') {
        if (obj.found) {
            if (obj.success) {
                document.getElementById(id).innerHTML = "success";
                setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
            }
            else {
                document.getElementById(id).innerHTML = "fail";
                setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
            }
        }
        else {
            document.getElementById(id).innerHTML = "not found";
            setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
        }
    }
    else if (id == 'stream_start') {
        if (obj.found) {
            if (obj.success) {
                document.getElementById(id).innerHTML = "success";
                setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
            }
            else {
                document.getElementById(id).innerHTML = "fail";
                setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
            }
        }
        else {
            document.getElementById(id).innerHTML = "not found";
            setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
        }
    }
    else if (id == 'stream_restart') {
        if (obj.found) {
            document.getElementById(id).innerHTML = "done";
            setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
        }
        else {
            document.getElementById(id).innerHTML = "not found";
            setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
        }
    }
    else if (id == 'stream_remove') {
        if (obj.found) {
            if (obj.done) {
                document.getElementById(id).innerHTML = "done";
                setTimeout(() => { document.getElementById(id).innerHTML = ""; window.location.replace("/"); }, "2000");
            }
            else {
                document.getElementById(id).innerHTML = "fail";
                setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
            }
        }
        else {
            document.getElementById(id).innerHTML = "not found";
            setTimeout(() => { document.getElementById(id).innerHTML = ""; }, "2000");
        }
    }
}