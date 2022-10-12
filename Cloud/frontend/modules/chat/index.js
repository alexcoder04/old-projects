document.getElementById("browser").value = navigator.userAgent;
document.getElementById("cookies_enabled").value = navigator.cookieEnabled;
document.getElementById("languages").value = navigator.languages;
const screenData = {
    availHeight: window.screen.availHeight,
    availLeft: window.screen.availLeft,
    availTop: window.screen.availTop,
    availWidth: window.screen.availWidth,
    colorDepth: window.screen.colorDepth,
    height: window.screen.height,
    left: window.screen.left,
    orientation: {
        type: window.screen.orientation.type,
        angle: window.screen.orientation.angle
    },
    pixelDepth: window.screen.pixelDepth,
    top: window.screen.top,
    width: window.screen.width
};
document.getElementById("screen").value = JSON.stringify(screenData);
document.getElementById("os").value = navigator.platform;