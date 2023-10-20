import './edit.less'
jQuery(document).ready(function ($) {
  // Hide / show editor's tools & messages when clicking on "Preview" in Plone toolbar
  $("#contentview-preview a").click(function(e){
    $(".hide-in-preview, #section-byline, #global_statusmessage").toggle("fast");
    e.preventDefault();
  });

  // Uncheck checked icon
  $("#formfield-form-widgets-svg_icon input").click(function(e){
    var $elm_clicked = $(this);
    if ($(this).attr('checked')) {
      $(this).prop("checked", false );
      $(this).removeAttr("checked");
      $(this).css("box-shadow", "none");
      $(this).css("border-color", "#DEE2ED");
    }
    else {
      $("#formfield-form-widgets-svg_icon input").each(function(index, elm) {
        if ($elm_clicked[0] === elm) {
          $(this).prop("checked", true );
          $(this).attr("checked", "checked");
          $(this).css("border-color", "#007a99");
          $(this).css("box-shadow", "0 0 0 0.25rem rgb(0 122 153 / 25%)");
        }
        else {
          $(this).prop("checked", false );
          $(this).removeAttr("checked");
          $(this).css("box-shadow", "none");
          $(this).css("border-color", "#DEE2ED");
        }
      })
    }
  });
});

jQuery(window).on("load", function(e) {
  // Move authentic sources menu just before user/personaltools-menulink in Plone toolbar
  var auth_sources = $("#plone-authentic-sources-menu").wrap("<ul class='plonetoolbar-authentic-sources-menu'>").parent();
  $(".personaltools-wrapper").prepend(auth_sources);

  // Move smartweb help menu just before user/personaltools-menulink in Plone toolbar
  var smartweb_help = $("#plone-smartweb-help-menu").wrap("<ul class='plonetoolbar-smartweb-help-menu'>").parent();
  $(".personaltools-wrapper").prepend(smartweb_help);
});
