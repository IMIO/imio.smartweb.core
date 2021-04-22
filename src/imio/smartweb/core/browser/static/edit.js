jQuery(document).ready(function ($) {

  // Toggle on add / edit forms fieldsets

  // 1. hide default fieldset legend (ckass : expanded)
  $("form.tabbed-form-with-toggle fieldset:first legend").hide();
  $("form.tabbed-form-with-toggle fieldset:first legend").addClass("expanded");

  // 2. hide all fieldsets content except first (class : collapsed)
  $("form.tabbed-form-with-toggle fieldset:not(:first) legend").siblings().hide();
  $("form.tabbed-form-with-toggle fieldset:not(:first) legend").addClass("collapsed");

  // 3. add toggle on all fieldsets legends & toggle expanded / collapsed classes
  $("form.tabbed-form-with-toggle fieldset:not(:first) legend").click(function(){
     var legend = $(this);
     var changed_class = false;
     $(this).siblings().slideToggle("fast", function() {
         if (!changed_class) {
            legend.toggleClass("collapsed");
            legend.toggleClass("expanded");
            changed_class = true;
        }
     });
  });
});
