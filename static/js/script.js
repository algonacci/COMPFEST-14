// Custom Dialog Box Size
$(document).ready(function () {
    window.addEventListener('dfMessengerLoaded', function (event) {
        $r1 = document.querySelector("df-messenger");
        $r2 = $r1.shadowRoot.querySelector("df-messenger-chat");
        $r3 = $r2.shadowRoot.querySelector("df-messenger-user-input");
        var sheet = new CSSStyleSheet;
        sheet.replaceSync(`div.chat-wrapper[opened="true"] { height: 440px }`);
        $r2.shadowRoot.adoptedStyleSheets = [sheet];
    });
});

// Smooth scroll on navbar
var prevScrollpos = window.pageYOffset;
window.onscroll = function () {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("navbar").style.top = "0";
    } else {
        document.getElementById("navbar").style.top = "-120px";
    }
    prevScrollpos = currentScrollPos;
}

// Button Loader
$(document).ready(function() {
    $("#submitForm").click(function() {
        $(this).addClass("loader");

        setTimeout(function() {
            $("#submitForm").removeClass("loader");
        }, 2000);
    })
});