document.addEventListener("DOMContentLoaded", function () {
  // Récupérer la langue courante de Plone
  var currentLanguage = document.documentElement.lang || "fr"; // fallback vers 'fr'

  // Dictionnaire de traductions pour les aria-labels
  var translations = {
    fr: {
      next: "Élément suivant",
      prev: "Élément précédent",
      pagination: "Aller à l'élément",
      first: "Premier élément",
      last: "Dernier élément",
    },
    en: {
      next: "Next slide",
      prev: "Previous slide",
      pagination: "Go to slide",
      first: "First slide",
      last: "Last slide",
    },
    de: {
      next: "Nächstes Element",
      prev: "Vorheriges Element",
      pagination: "Gehe zu Element",
      first: "Erstes Element",
      last: "Letztes Element",
    },
    nl: {
      next: "Volgende item",
      prev: "Vorig item",
      pagination: "Ga naar item",
      first: "Eerste item",
      last: "Laatste item",
    },
  };

  // Fonction pour obtenir la traduction
  console.log("Current language:", currentLanguage);
  function getTranslation(key) {
    return translations[currentLanguage]
      ? translations[currentLanguage][key]
      : translations["fr"][key];
  }

  $(".swiper").each(function (index) {
    console.log("Initializing Swiper for element:");
    var batchSize = parseInt($(this).attr("data-nb-results-by-batch"));
    if (isNaN(batchSize)) {
      batchSize = 1;
    }
    var mySwiper = new Swiper($(this)[0], {
      slidesPerView: 1,
      slidesPerGroup: 1,
      spaceBetween: 10,
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      a11y: {
        prevSlideMessage: getTranslation("prev"),
        nextSlideMessage: getTranslation("next"),
        paginationBulletMessage: getTranslation("pagination") + " {{index}}",
        firstSlideMessage: getTranslation("first"),
        lastSlideMessage: getTranslation("last"),
      },
      breakpoints: {
        // when window width is >= 320px
        320: {
          slidesPerView: 1,
          slidesPerGroup: 1,
        },
        // when window width is >= 480px
        576: {
          slidesPerView: batchSize > 1 ? 2 : 1,
          slidesPerGroup: batchSize > 1 ? 2 : 1,
        },
        // when window width is >= 640px
        768: {
          slidesPerView: batchSize > 2 ? 2 : batchSize,
          slidesPerGroup: batchSize > 2 ? 2 : batchSize,
        },
        992: {
          slidesPerView: batchSize > 2 ? 3 : batchSize,
          slidesPerGroup: batchSize > 2 ? 3 : batchSize,
        },
        1200: {
          slidesPerView: batchSize,
          slidesPerGroup: batchSize,
        },
      },
    });
  });
});
