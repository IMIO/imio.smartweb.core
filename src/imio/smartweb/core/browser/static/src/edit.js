import './edit.less'
jQuery(document).ready(function ($) {
  // Hide / show editor's tools & messages when clicking on "Preview" in Plone toolbar
  $("#contentview-preview a").click(function(e){
    $(".hide-in-preview, #section-byline, #global_statusmessage").toggle("fast");
    e.preventDefault();
  });

  // Move authentic sources menu just before user/personaltools-menulink in Plone toolbar
  var auth_sources = $("#plone-authentic-sources-menu").wrap("<ul class='plonetoolbar-authentic-sources-menu'>").parent();
  $(".personaltools-wrapper").prepend(auth_sources);

  // Move smartweb help menu just before user/personaltools-menulink in Plone toolbar
  var smartweb_help = $("#plone-smartweb-help-menu").wrap("<ul class='plonetoolbar-smartweb-help-menu'>").parent();
  $(".personaltools-wrapper").prepend(smartweb_help);
});

