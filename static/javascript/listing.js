function redirect_func(url) {
    window.location.replace(url);
}
function stream_api_all_func(url) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false );
    xmlHttp.onload = () => {
        if (xmlHttp.status == 200)
        alert("Done");
    else
        alert("Fail");
    };
    xmlHttp.send( null );
}
function copy_func(id) {
    var copyText = document.getElementById(id).innerHTML;
    navigator.clipboard.writeText(copyText);
    alert(copyText);
}