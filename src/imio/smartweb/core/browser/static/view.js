jQuery(document).ready(function ($) {

  // Hide / show editor's tools when clicking on "Preview" in Plone toolbar

  $(".opening_informations").click(function(e){
    $(this).siblings(".table_schedule").toggle("fast");
    $(this).toggle("fast");
    e.preventDefault();
  });
});
