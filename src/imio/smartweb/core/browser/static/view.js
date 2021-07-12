jQuery(document).ready(function ($) {

  // Show full schedule table when clicking on today's schedule

  $(".opening_informations").click(function(e){
    $(this).siblings(".table_schedule").toggle("fast");
    $(this).toggle("fast");
    e.preventDefault();
  });
});
