jQuery(document).ready(function ($) {

  // Toggle on add / edit forms fieldsets
  // 1. hide default fieldset legend
  $("form.tabbed-form-with-toggle fieldset:first legend").hide();
  // 2. hide all fieldsets content except first
  $("form.tabbed-form-with-toggle fieldset:not(:first) legend").siblings().hide();
  // 3. add toggle on all fieldsets legends
  $("form.tabbed-form-with-toggle fieldset:not(:first) legend").click(function(){
     $(this).siblings().slideToggle("fast");
  });

});
