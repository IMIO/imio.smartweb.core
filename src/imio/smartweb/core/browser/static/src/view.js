import "./view.less";
jQuery(document).ready(function ($) {
  // Show full schedule table when clicking on today's schedule
  $(".opening_informations").click(function (e) {
    $(this).siblings(".table_schedule").toggleClass("table_schedule--active");
    e.preventDefault();
  });
  $(document).click(function (e) {
    if ($(".table_schedule").hasClass("table_schedule--active")) {
      if (
        !$(".table_schedule").is(e.target) &&
        !$(".opening_informations").is(e.target) &&
        !$(".table_schedule td").is(e.target)
      ) {
        $(".table_schedule").toggleClass("table_schedule--active");
      }
    }
  });

  if (
    window.location.href.indexOf("@@siteadmin-smartweb-controlpanel") !== -1
  ) {
    if ($("div.container div.statusmessage-error").length > 0) {
      $("div.container div.statusmessage-info").remove();
    }
  }
});

// New navigation
$(document).ready(function () {
  const menu = $("#portal-globalnav");
  const menuInert = $("#portal-globalnav > li > .has_subtree");
  const submenuInert = $("#subsite-navigation li > .has_subtree");

  const submenu = $("#subsite-navigation");

  // ✅ On applique inert par défaut car le menu est fermé initialement
  menuInert.attr("inert", "");
  submenuInert.attr("inert", "");

  $(".close-nav").click(function () {
    closeNav();
  });

  $(document).mouseup((e) => {
    if (
      !menu.is(e.target) &&
      menu.has(e.target).length === 0 &&
      !submenu.is(e.target) &&
      submenu.has(e.target).length === 0
    ) {
      closeNav();
    }
  });

  // Gestion des clics pour ouvrir les menus
  $("li.has_subtree > a").click(function () {
    // MENU
    if ($(this).closest(menu).length > 0) {
      if (!$("#portal-globalnav .show-nav").length > 0) {
        $(menu).toggleClass("activated");
        $(".mask-menu").toggleClass("in");

        // ✅ Quand on active, on enlève inert
        menuInert.removeAttr("inert");
      }
      $(this).parent().toggleClass("show-nav");
      $(this).parent().find(".show-nav").toggleClass("show-nav");
      $(this).parent().siblings(".show-nav").toggleClass("show-nav");
      $(this).parent().find(".activated").toggleClass(".activated");
      if (!$("#portal-globalnav .show-nav").length > 0) {
        closeNav();
      }
    }

    // SUBMENU
    if ($(this).closest(submenu).length > 0) {
      if (!$("#subsite-navigation .show-nav").length > 0) {
        $(submenu).toggleClass("activated");
        document.body.classList.add("submenu-open-nav-overflow");
        document.documentElement.classList.add("submenu-open-nav-overflow");

        // ✅ Quand on active, on enlève inert
        submenuInert.removeAttr("inert");
      }
      $(this).parent().toggleClass("show-nav");
      $(this).parent().find(".show-nav").toggleClass("show-nav");
      $(this).parent().siblings(".show-nav").toggleClass("show-nav");
      $(this).parent().find(".activated").toggleClass(".activated");
      if (!$("#subsite-navigation .show-nav").length > 0) {
        closeNav();
      }
    }
    return false;
  });

  $(".prev-nav").click(function () {
    $(this).closest(".show-nav").toggleClass("show-nav");
  });

  // Fermeture du menu au focusout
  menu.on("focusout", function () {
    setTimeout(function () {
      if (!menu.has(document.activeElement).length) {
        closeNav();
      }
    }, 0);
  });

  // ✅ Fonction de fermeture avec inert
  function closeNav() {
    menu.removeClass("activated");
    submenu.removeClass("activated");
    document.body.classList.remove("submenu-open-nav-overflow");
    document.documentElement.classList.remove("submenu-open-nav-overflow");
    $(".show-nav").removeClass("show-nav");
    $(".mask-menu").removeClass("in");

    // ✅ On réactive inert pour bloquer le focus clavier
    menuInert.attr("inert", "");
    submenuInert.attr("inert", "");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const headerActions = document.getElementById("header-actions");
  const target = document.getElementById("portal-globalnav-collapse");

  if (!headerActions || !target) return;

  const originalParent = headerActions.parentNode;
  const nextSibling = headerActions.nextSibling;

  function moveHeaderActions() {
    if (window.innerWidth <= 991) {
      if (!target.contains(headerActions)) target.appendChild(headerActions);
    } else {
      if (headerActions.parentNode !== originalParent) {
        if (nextSibling && nextSibling.parentNode === originalParent) {
          originalParent.insertBefore(headerActions, nextSibling);
        } else {
          originalParent.appendChild(headerActions);
        }
      }
    }
  }

  moveHeaderActions();
  window.addEventListener("resize", moveHeaderActions);
});
