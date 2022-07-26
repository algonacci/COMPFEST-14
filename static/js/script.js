// Custom Dialog Box Size
$(document).ready(function () {
  window.addEventListener("dfMessengerLoaded", function (event) {
    $r1 = document.querySelector("df-messenger");
    $r2 = $r1.shadowRoot.querySelector("df-messenger-chat");
    $r3 = $r2.shadowRoot.querySelector("df-messenger-user-input");
    var sheet = new CSSStyleSheet();
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
};

// Submit and Display Button Loader
$(document).ready(function () {
  $("#submitFormFlight").click(function () {
    $(this).addClass("loader");

    setTimeout(function () {
      $("#submitFormFlight").removeClass("loader");
    }, 2000);

    $.ajax({
      url: "/flight-fare-predictor",
      type: "POST",
      data: $("#form").serialize(),
    });
  });
});

$(document).ready(function () {
  $("#submitFormTopic").click(function () {
    $(this).addClass("loader");

    setTimeout(function () {
      $("#submitFormTopic").removeClass("loader");
    }, 60000);

    $.ajax({
      url: "/sentiment-analysis/topic",
      type: "POST",
      data: $("#formTopic").serialize(),
    });
  });
});

$(document).ready(function () {
  $("#submitFormUser").click(function () {
    $(this).addClass("loader");

    setTimeout(function () {
      $("#submitFormUser").removeClass("loader");
    }, 60000);

    $.ajax({
      url: "/sentiment-analysis/user",
      type: "POST",
      data: $("#formUser").serialize(),
    });
  });
});

// Upload image and show preview
var loadFile = function (event) {
  var output = document.getElementById("output");
  output.src = URL.createObjectURL(event.target.files[0]);
};
