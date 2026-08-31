import "./edit.less";
jQuery(document).ready(function ($) {
  // Hide / show editor's tools & messages when clicking on "Preview" in Plone toolbar
  $("#contentview-preview a").click(function (e) {
    $(".hide-in-preview, #section-byline, #global_statusmessage").toggle(
      "fast",
    );
    e.preventDefault();
  });

  // Uncheck checked icon
  $("#formfield-form-widgets-svg_icon input").click(function (e) {
    var $elm_clicked = $(this);
    if ($(this).attr("checked")) {
      $(this).prop("checked", false);
      $(this).removeAttr("checked");
      $(this).css("box-shadow", "none");
      $(this).css("border-color", "#DEE2ED");
    } else {
      $("#formfield-form-widgets-svg_icon input").each(function (index, elm) {
        if ($elm_clicked[0] === elm) {
          $(this).prop("checked", true);
          $(this).attr("checked", "checked");
          $(this).css("border-color", "#007a99");
          $(this).css("box-shadow", "0 0 0 0.25rem rgb(0 122 153 / 25%)");
        } else {
          $(this).prop("checked", false);
          $(this).removeAttr("checked");
          $(this).css("box-shadow", "none");
          $(this).css("border-color", "#DEE2ED");
        }
      });
    }
  });

  // Move statistics action menu entry as the first element in personaltools menu
  var $stat_link = $("li:has(a[href*='@@stats'])");
  $("#collapse-personaltools li:eq(0)").after($stat_link);
});

jQuery(window).on("load", function (e) {
  // Move authentic sources menu just before user/personaltools-menulink in Plone toolbar
  var auth_sources = $("#plone-authentic-sources-menu")
    .wrap("<ul class='plonetoolbar-authentic-sources-menu'>")
    .parent();
  $(".personaltools-wrapper").prepend(auth_sources);

  // Move smartweb help menu just before user/personaltools-menulink in Plone toolbar
  var smartweb_help = $("#plone-smartweb-help-menu")
    .wrap("<ul class='plonetoolbar-smartweb-help-menu'>")
    .parent();
  $(".personaltools-wrapper").prepend(smartweb_help);
});

// Show/hide image_scale field based on alignment value (SectionText form)
document.addEventListener("DOMContentLoaded", function () {
  const alignmentSelect = document.getElementById("form-widgets-alignment");
  if (!alignmentSelect) return;

  const imageScaleField = document.getElementById(
    "formfield-form-widgets-image_scale",
  );
  const imageScaleSelect = document.getElementById("form-widgets-image_scale");
  if (!imageScaleField || !imageScaleSelect) return;

  function toggleImageScale() {
    const show =
      alignmentSelect.value === "top" || alignmentSelect.value === "bottom";
    imageScaleField.style.display = show ? "" : "none";
    if (!show) {
      imageScaleSelect.value = "section_text";
    }
  }

  alignmentSelect.addEventListener("change", toggleImageScale);
  toggleImageScale();
});

// Show/hide "viewport" image_scale option based on section width (SectionText form)
document.addEventListener("DOMContentLoaded", function () {
  const bootstrapSelect = document.getElementById(
    "form-widgets-bootstrap_css_class",
  );
  const imageScaleSelect = document.getElementById("form-widgets-image_scale");
  if (!bootstrapSelect || !imageScaleSelect) return;

  const viewportOption = imageScaleSelect.querySelector(
    'option[value="section_text_viewport"]',
  );
  if (!viewportOption) return;

  function toggleViewportOption() {
    const isFullWidth =
      bootstrapSelect.value === "col-sm-12" ||
      bootstrapSelect.value === "--NOVALUE--";
    if (!isFullWidth) {
      if (imageScaleSelect.value === "section_text_viewport") {
        imageScaleSelect.value = "section_text";
      }
      viewportOption.disabled = true;
      viewportOption.hidden = true;
    } else {
      viewportOption.disabled = false;
      viewportOption.hidden = false;
    }
  }

  bootstrapSelect.addEventListener("change", toggleViewportOption);
  toggleViewportOption();
});

// Show only the field matching the chosen source (SectionEvents / SectionNews
// forms). Both sections offer two mutually exclusive sources -- a whole
// agenda/news folder, or a hand-picked selection -- and the radio decides
// which one the view uses, so the unused field is only noise here.
document.addEventListener("DOMContentLoaded", function () {
  // linking_rest_view belongs to the container source only: a hand-picked
  // selection comes from the whole entity and links to the control panel's
  // default view, so the linking view plays no part and is hidden too.
  const SOURCES = [
    {
      source: "events_source",
      fields: {
        agenda: ["linking_rest_view", "related_events"],
        selection: ["specific_related_events"],
      },
    },
    {
      source: "news_source",
      fields: {
        newsfolder: ["linking_rest_view", "related_news"],
        selection: ["specific_related_newsitems"],
      },
    },
  ];

  SOURCES.forEach(function (config) {
    const name = 'input[name="form.widgets.' + config.source + '"]';
    const radios = document.querySelectorAll(name);
    if (!radios.length) return;

    const wrappers = {};
    Object.keys(config.fields).forEach(function (value) {
      wrappers[value] = config.fields[value]
        .map(function (field) {
          return document.getElementById("formfield-form-widgets-" + field);
        })
        .filter(Boolean);
    });

    function toggleSourceFields() {
      const checked = document.querySelector(name + ":checked");
      const selected = checked ? checked.value : null;
      Object.keys(wrappers).forEach(function (value) {
        wrappers[value].forEach(function (wrapper) {
          wrapper.style.display = value === selected ? "" : "none";
        });
      });
    }

    radios.forEach(function (radio) {
      radio.addEventListener("change", toggleSourceFields);
    });
    toggleSourceFields();
  });
});

// Cascade the agenda / news folder <select> on the chosen linking view.
// An EventsView (resp. NewsView) displays one agenda (resp. news folder) plus
// the agendas/folders populating it, so related_events / related_news must be
// limited to that scope. A vocabulary only ever sees the saved value, hence
// this client-side pass. The hand-picked pickers are NOT cascaded: they offer
// the whole entity on purpose, and their items link to the site's default
// view. Only one of the two forms is ever rendered at once, so the loop below
// finds one target and skips the other.
document.addEventListener("DOMContentLoaded", function () {
  const linking = document.getElementById("form-widgets-linking_rest_view");
  if (!linking) return;

  const CASCADES = [
    {
      endpoint: "@@scoped-agendas",
      target: "form-widgets-related_events",
    },
    {
      endpoint: "@@scoped-newsfolders",
      target: "form-widgets-related_news",
    },
  ];

  function currentLinkingUid() {
    // the contentbrowser stores one or more UIDs separated by ";"
    return (linking.value || "").split(";")[0] || "";
  }

  CASCADES.forEach(function (cascade) {
    const related = document.getElementById(cascade.target);
    if (!related) return;

    // 1. Repopulate the <select> whenever the linking view changes.
    linking.addEventListener("change", function () {
      const uid = currentLinkingUid();
      if (!uid) return;
      const base = document.body.getAttribute("data-portal-url") || "";
      fetch(
        base +
          "/" +
          cascade.endpoint +
          "?linking_rest_view=" +
          encodeURIComponent(uid),
        {
          credentials: "same-origin",
          headers: { Accept: "application/json" },
        },
      )
        .then(function (response) {
          return response.json();
        })
        .then(function (items) {
          const previous = related.value;
          // z3c.form renders the no-value entry with the --NOVALUE-- token,
          // never an empty value. Destroying it and assigning "" would leave
          // the <select> on selectedIndex -1, with no way to clear the field
          // short of reloading the page.
          const placeholder = related.querySelector(
            'option[value="--NOVALUE--"]',
          );
          related.innerHTML = "";
          if (placeholder) related.appendChild(placeholder);
          items.forEach(function (item) {
            const option = document.createElement("option");
            option.value = item.id;
            option.textContent = item.text;
            related.appendChild(option);
          });
          const stillThere = items.some(function (item) {
            return item.id === previous;
          });
          related.value = stillThere
            ? previous
            : placeholder
              ? placeholder.value
              : "";
          jQuery(related).trigger("change");
        })
        .catch(function () {
          /* leave the current options in place */
        });
    });
  });
});
