import "./view.less";

// Compute, for every section aligned with the text sections container, its
// position within a *virtual* 760px-wide column (see view.less for the
// rationale: a "full" 760px line, alone or as a pair of 1/2, gets symmetric
// margins that both center it and naturally force the next section to wrap
// to a new flex line — no DOM manipulation is involved on purpose, since
// inserting/wrapping elements inside the sortable sections container would
// corrupt SortableJS's sibling-index-based drag-and-drop reordering).
// Exposed on window (this file is bundled by webpack, hence its own module
// scope) so it can be re-run from the separate, non-bundled inline <script>
// tags in viewlets/htmx_js_header.pt (after a width/alignment change) and
// contents/pages/view.pt (after a drag-and-drop reorder).
window.updateTextAlignmentLayout = function updateTextAlignmentLayout() {
  // NOTE: the "span.pat-sortable[data-pat-sortable]" wrapper is only
  // rendered for users with edit rights (contents/pages/view.pt sets
  // tal:omit-tag="not: can_reorder" on it) — for anonymous/non-editor
  // visitors it's entirely absent and .sortable-section divs are direct
  // children of .row instead. Select on the class alone so this works
  // regardless of login/permission state.
  var sortableSections = document.querySelectorAll("div.sortable-section");

  // Clear any correction applied by a previous run before recomputing
  // anything below (see the geometry-correction pass at the end of this
  // function) — otherwise a stale correction could interfere with the
  // fresh measurements taken this time.
  sortableSections.forEach(function (section) {
    section.style.marginLeft = "";
    section.style.transform = "";
  });

  // Sections aligned with the text sections container are accumulated here
  // as they're walked in DOM order, then finalized (flushPending) as soon
  // as a non-text-aligned section is met, the 2-unit virtual line capacity
  // is exceeded, or the end of the list is reached — this is needed to
  // decide, only once a group is complete, whether it fills a full 760px
  // line (a solo 1/1, or a genuine pair of 1/2) or ends up as a lone,
  // unpaired half-width section.
  var pending = [];
  var pendingUnits = 0;

  function flushPending() {
    if (pending.length === 0) return;
    var isFull = pendingUnits >= 2;
    pending.forEach(function (section, index) {
      var isLast = index === pending.length - 1;
      section.classList.toggle("text-align-line-start", index === 0);
      section.classList.toggle("text-align-line-end", isFull && isLast);
      // A lone half-width section (no partner to complete a full 760px
      // line) gets pushed all the way to the right too — margin-right:50%
      // always exactly completes the line's actual width regardless of
      // that width (see view.less) — so nothing else (another "main"- or
      // "text"-aligned section) can share its line.
      section.classList.toggle("text-align-isolated-half", !isFull && isLast);
    });
    pending = [];
    pendingUnits = 0;
  }

  sortableSections.forEach(function (section) {
    if (!section.classList.contains("container-se-text")) {
      flushPending();
      section.classList.remove(
        "text-align-line-start",
        "text-align-line-end",
        "text-align-isolated-half",
      );
      return;
    }
    var units = section.classList.contains("col-sm-12") ? 2 : 1;
    if (pendingUnits + units > 2) {
      // Doesn't fit on the current virtual line (e.g. a lone half-width
      // section followed by a full-width one): finalize the pending group
      // first instead of wrongly treating this section as a continuation.
      flushPending();
    }
    pending.push(section);
    pendingUnits += units;
    if (pendingUnits >= 2) {
      flushPending();
    }
  });
  flushPending();

  // A section starting a fresh virtual line (text-align-line-start) can
  // still end up sharing its actual flex line with an immediately
  // preceding "main"-aligned section: a fixed margin-left (see view.less)
  // cannot guarantee a wrap against an arbitrary, unknown predecessor
  // width — the margin-based trick used elsewhere in this function only
  // works because it controls BOTH ends of a self-contained group of
  // text-aligned sections, which isn't the case here. Only measuring the
  // real rendered layout can detect and fix this, without changing the
  // section's own configured width (760px / half of it).
  document
    .querySelectorAll(".container-se-text.text-align-line-start")
    .forEach(function (section) {
      var prev = section.previousElementSibling;
      if (!prev || prev.classList.contains("container-se-text")) return;
      var prevRect = prev.getBoundingClientRect();
      var sectionRect = section.getBoundingClientRect();
      if (sectionRect.top !== prevRect.top) return; // already on its own line

      var row = section.parentElement;
      var rowRect = row.getBoundingClientRect();
      // Compute the *minimal* extra push needed to overflow past the
      // row's right edge (a 1px buffer), forcing a wrap — NOT an
      // oversized margin spanning the whole row's width, which would
      // inflate this section's layout footprint way beyond the row and
      // break the surrounding layout.
      var overflowNeeded = rowRect.right - sectionRect.right + 1;
      if (overflowNeeded <= 0) return; // shouldn't happen given the check above, but guard anyway

      var currentMarginLeft = parseFloat(getComputedStyle(section).marginLeft) || 0;
      section.style.marginLeft = currentMarginLeft + overflowNeeded + "px";
      var wrappedRect = section.getBoundingClientRect();
      if (wrappedRect.top === prevRect.top) {
        // Safety net: still didn't wrap — bail out rather than leave an
        // inconsistent margin in place.
        section.style.marginLeft = "";
        return;
      }

      // Now alone on its own line: cancel the visual effect of that extra
      // push with a transform — purely visual, it doesn't affect the
      // layout/wrap calculation, so it can't undo the wrap it just
      // forced — so the section still renders flush with the left edge
      // of the virtual 760px column, exactly like every other isolated
      // section.
      var targetLeft = rowRect.left + Math.max(0, (rowRect.width - 760) / 2);
      section.style.transform =
        "translateX(" + (targetLeft - wrappedRect.left) + "px)";
    });
};

document.addEventListener("DOMContentLoaded", function () {
  window.updateTextAlignmentLayout();
  window.addEventListener("resize", window.updateTextAlignmentLayout);
});

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
