jQuery(document).ready(function ($) {

  // Hide / show editor's tools & messages when clicking on "Preview" in Plone toolbar

  $("#contentview-preview a").click(function(e){
    $(".hide-in-preview, #section-byline, #global_statusmessage").toggle("fast");
    e.preventDefault();
  });

});
