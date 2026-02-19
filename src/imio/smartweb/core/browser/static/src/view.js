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
document.addEventListener("DOMContentLoaded", function () {
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

// gestion du menu sticky

document.addEventListener("DOMContentLoaded", function () {
  // Gestion du sticky menu avec deux comportements possibles
  const header = document.querySelector("#portal-header-top");
  if (header) {
    const parentHeader = document.querySelector("#portal-header");
    const isBasicSticky = document.body.classList.contains("menu-sticky");
    const isStickyOnTop =
      document.body.classList.contains("menu-sticky-on-top");

    // Ne rien faire si aucune classe n'est présente
    if (!isBasicSticky && !isStickyOnTop) {
      return;
    }

    // Calculer la hauteur initiale du header (avant qu'il devienne sticky)
    const headerHeight = header.offsetHeight;
    const headerOffset = header.offsetTop;
    let lastScrollTop = 0;
    let accumulatedScroll = 0;

    // Définir la hauteur du header une seule fois
    document.documentElement.style.setProperty(
      "--header-height",
      headerHeight + "px",
    );

    // Fonction pour mettre à jour uniquement la position et la largeur
    function updateHeaderDimensions() {
      if (parentHeader) {
        const parentRect = parentHeader.getBoundingClientRect();
        const parentWidth = parentHeader.offsetWidth;
        const parentLeft = parentRect.left;
        document.documentElement.style.setProperty(
          "--header-width",
          parentWidth + "px",
        );
        document.documentElement.style.setProperty(
          "--header-left",
          parentLeft + "px",
        );
      }
    }

    // Initialiser les dimensions
    updateHeaderDimensions();

    window.addEventListener("scroll", function () {
      const currentScrollTop =
        window.pageYOffset || document.documentElement.scrollTop;

      // Gérer la classe sticky-is-top pour les deux modes
      if (currentScrollTop === 0) {
        header.classList.add("sticky-is-top");
      } else {
        header.classList.remove("sticky-is-top");
      }

      if (isBasicSticky) {
        // Comportement de base : sticky dès qu'on dépasse le header
        if (currentScrollTop > headerOffset) {
          header.classList.add("sticky");
          document.body.classList.add("has-sticky-header");
          updateHeaderDimensions();
        } else {
          header.classList.remove("sticky");
          document.body.classList.remove("has-sticky-header");
        }
      } else if (isStickyOnTop) {
        // Comportement avancé : sticky uniquement au scroll vers le haut
        const scrollingDown = currentScrollTop > lastScrollTop;
        const scrollDelta = Math.abs(currentScrollTop - lastScrollTop);

        // Seuil uniquement pour le scroll vers le haut (évite les micro-mouvements)
        const thresholdUp = 10;
        // Pas de seuil pour le scroll vers le bas (réactivité immédiate)
        const thresholdDown = 1;

        if (currentScrollTop > headerOffset + headerHeight) {
          // Dès qu'on dépasse le header, ajouter has-sticky-header et le garder
          document.body.classList.add("has-sticky-header");

          if (!scrollingDown && scrollDelta > thresholdUp) {
            // Scroll vers le haut avec dépassement du seuil : afficher le menu
            if (currentScrollTop === 0) {
              // Au niveau 0 : utiliser sticky-on-top
              header.classList.add("sticky-on-top");
              header.classList.remove("sticky-demi-active", "sticky-hidden");
            } else {
              // Pas au niveau 0 : utiliser sticky-demi-active
              header.classList.add("sticky-demi-active");
              header.classList.remove("sticky-on-top", "sticky-hidden");
            }
            updateHeaderDimensions();
          } else if (scrollingDown && scrollDelta > thresholdDown) {
            // Scroll vers le bas : cacher le menu immédiatement
            header.classList.add("sticky-hidden");
            header.classList.remove("sticky-on-top", "sticky-demi-active");
          }
        } else {
          // Pas encore dépassé le header : tout enlever
          header.classList.remove(
            "sticky-on-top",
            "sticky-demi-active",
            "sticky-hidden",
          );
          document.body.classList.remove("has-sticky-header");
        }

        lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop;
      }
    });

    // Gérer le redimensionnement de la fenêtre
    window.addEventListener("resize", function () {
      // Retirer temporairement le sticky pour mesurer la hauteur naturelle
      const wasSticky =
        header.classList.contains("sticky") ||
        header.classList.contains("sticky-on-top") ||
        header.classList.contains("sticky-demi-active");
      const wasStickyOnTop = header.classList.contains("sticky-on-top");
      const wasStickyDemiActive =
        header.classList.contains("sticky-demi-active");
      const wasHidden = header.classList.contains("sticky-hidden");

      if (wasSticky || wasHidden) {
        header.classList.remove(
          "sticky",
          "sticky-on-top",
          "sticky-demi-active",
          "sticky-hidden",
        );
      }

      const newHeight = header.offsetHeight;
      document.documentElement.style.setProperty(
        "--header-height",
        newHeight + "px",
      );

      // Restaurer les classes
      if (wasSticky) {
        if (isBasicSticky) {
          header.classList.add("sticky");
        } else if (wasStickyOnTop) {
          header.classList.add("sticky-on-top");
        } else if (wasStickyDemiActive) {
          header.classList.add("sticky-demi-active");
        }
      }
      if (wasHidden) {
        header.classList.add("sticky-hidden");
      }

      updateHeaderDimensions();
    });
  }
});
