(function () {
  "use strict";

  // Recipe search on the index page
  var searchInput = document.getElementById("recipe-search");
  if (searchInput) {
    var cards = document.querySelectorAll(".recipe-card");
    var noResults = document.getElementById("no-results");

    var filter = function () {
      var q = searchInput.value.trim().toLowerCase();
      var visible = 0;
      cards.forEach(function (card) {
        var haystack = (card.getAttribute("data-search") || "").toLowerCase();
        var match = q === "" || haystack.indexOf(q) !== -1;
        card.style.display = match ? "" : "none";
        if (match) visible++;
      });
      if (noResults) {
        noResults.classList.toggle("is-visible", visible === 0);
      }
    };

    searchInput.addEventListener("input", filter);
  }

  // Copy URL button on recipe pages
  var copyButtons = document.querySelectorAll("[data-copy-url]");
  copyButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      var url = window.location.href;
      var feedback = button.parentNode.querySelector(".copy-feedback");

      var showFeedback = function (text) {
        if (feedback) {
          feedback.textContent = text;
          feedback.classList.add("is-visible");
          setTimeout(function () {
            feedback.classList.remove("is-visible");
          }, 2000);
        }
      };

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(
          function () {
            showFeedback("Kopiert!");
          },
          function () {
            showFeedback("Kopieren fehlgeschlagen");
          }
        );
      } else {
        var input = document.createElement("input");
        input.value = url;
        document.body.appendChild(input);
        input.select();
        try {
          document.execCommand("copy");
          showFeedback("Kopiert!");
        } catch (e) {
          showFeedback("Kopieren fehlgeschlagen");
        }
        document.body.removeChild(input);
      }
    });
  });
})();
