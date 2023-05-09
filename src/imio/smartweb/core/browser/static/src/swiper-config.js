document.addEventListener("DOMContentLoaded", function() { 
  $('.swiper').each(function (index) {
    var batchSize = parseInt($(this).attr('data-nb-results-by-batch'));
    if (isNaN(batchSize)) {
      batchSize = 1
    }
    var mySwiper = new Swiper($(this)[0], {
      slidesPerView: 1,
      slidesPerGroup: 1,
      spaceBetween: 10,
      pagination: {
        el: '.swiper-pagination',
        clickable: true
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
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
          slidesPerGroup: batchSize > 1 ? 2 : 1
        },
        // when window width is >= 640px
        768: {
          slidesPerView: batchSize > 2 ? 2 : batchSize,
          slidesPerGroup: batchSize > 2 ? 2 : batchSize
        },
        992: {
          slidesPerView: batchSize > 2 ? 3 : batchSize,
          slidesPerGroup: batchSize > 2 ? 3 : batchSize
        },
        1200: {
          slidesPerView: batchSize,
          slidesPerGroup: batchSize
        }
      }
    });
  });
});
