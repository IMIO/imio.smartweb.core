jQuery(document).ready(function ($) {

  // Hide / show editor's tools when clicking on "Preview" in Plone toolbar

  $("#contentview-preview a").click(function(e){
    $(".hide-in-preview").toggle("fast");
    e.preventDefault();
  });

});
