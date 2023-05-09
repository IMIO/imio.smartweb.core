import './view.less'
jQuery(document).ready(function ($) {

  // Show full schedule table when clicking on today's schedule
  $(".opening_informations").click(function (e) {
    $(this).siblings(".table_schedule").toggleClass("table_schedule--active");
    // $(this).toggle("fast");
    e.preventDefault();
  });
  $(document).click(function (e) {
    if ($(".table_schedule").hasClass("table_schedule--active")) {
      if (!$(".table_schedule").is(e.target)
        && !$(".opening_informations").is(e.target)
        && !$(".table_schedule td").is(e.target)) {
        $(".table_schedule").toggleClass("table_schedule--active");
      }
    }
  });
  
});
// New navigation

$(document).ready(function () {
  const menu = $('#portal-globalnav');
  const submenu = $('#subsite-navigation');

  $(".close-nav").click(function () {
    closeNav();
  });

  $(document).mouseup(e => {
    if (!menu.is(e.target) // if the target of the click isn't the container...
      && menu.has(e.target).length === 0
      && !submenu.is(e.target)
      && submenu.has(e.target).length === 0
    ) // ... nor a descendant of the container
    {
      closeNav();
    }
  });

  // when you click a toggle show-nav its dropdown menu

  $("li.has_subtree > a").click(function () {


    // MENU
    if ($(this).closest(menu).length > 0) {
      if (!$("#portal-globalnav .show-nav").length > 0) {
        $(menu).toggleClass("activated");
        $(".mask-menu").toggleClass("in");
      }
      $(this).parent().toggleClass("show-nav");
      $(this).parent().find(".show-nav").toggleClass("show-nav");
      $(this).parent().siblings(".show-nav").toggleClass("show-nav")
      $(this).parent().find(".activated").toggleClass(".activated");
      if (!$("#portal-globalnav .show-nav").length > 0) {
        closeNav()
      }
    }

    // SUBMENU
    if ($(this).closest(submenu).length > 0) {
      if (!$("#subsite-navigation .show-nav").length > 0) {
        $(submenu).toggleClass("activated");
          document.body.classList.add('submenu-open-nav-overflow');
          document.documentElement.classList.add('submenu-open-nav-overflow');

      }
      $(this).parent().toggleClass("show-nav");
      $(this).parent().find(".show-nav").toggleClass("show-nav");
      $(this).parent().siblings(".show-nav").toggleClass("show-nav")
      $(this).parent().find(".activated").toggleClass(".activated");
      if (!$("#subsite-navigation .show-nav").length > 0) {
        closeNav()
      }
    }
    return false
  });

  // Prev nav
  $(".prev-nav").click(function () {
    $(this).closest(".show-nav").toggleClass("show-nav")
  });

  // close nav fonction
  function closeNav() {
    menu.removeClass('activated');
    submenu.removeClass('activated');
    document.body.classList.remove('submenu-open-nav-overflow');
    document.documentElement.classList.remove('submenu-open-nav-overflow');
    $('.show-nav').removeClass('show-nav');
    $(".mask-menu").removeClass("in");
  }
});