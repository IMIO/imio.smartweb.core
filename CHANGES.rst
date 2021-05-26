Changelog
=========


1.0a4 (2021-05-26)
------------------

- Add can_toggle_title_visibility property on sections. Use it on Contact section.
  [boulch laulaz]

- Add rich description on all content types
  [boulch]

- Add configurable url for connection to directory authentic source
  [boulch]

- Add contact section (with connection to directory authentic source)
  [boulch, laulaz]

- Views / templates code simplification
  [laulaz]

- Simplify taxonomies setup code & use taxonomy behavior directly
  [laulaz]

- Remove sections editing tools in footers
  [laulaz]

- Add preview action in Plone toolbar to hide editor actions in content
  [boulch]

- Move field "category" in categorization fieldset
  [boulch]

- Hide leadimage caption field everywhere (editform, addform)
  [boulch]


1.0a3 (2021-04-23)
------------------

- improved css for subsite navigation
  [thomlamb]

- Harmonize all sections templates. Rename some css class. Add new css class.
  [boulch, thomlamb]

- Add "row" class in page view template to be bootstrap aware.
  [boulch]

- Get sections bootstrap_css value in get_class pages view (instead of sections templates) to be bootstrap aware.
  [boulch]

- Compile resources
  [laulaz]


1.0a2 (2021-04-22)
------------------

- improved html semantics
  [thomlamb]

- WEBMIGP5-11: Add real values in page taxonomy
  [laulaz]

- Add category viewlet
  [laulaz]

- Add banner viewlet with local hide/show logic
  [boulch, laulaz]

- Change sections titles logic & add button to show / hide titles
  [laulaz]

- Add classes on add/edit forms legends when expanded / collapsed
  [laulaz]

- Add missing bootstrap class option (2/3)
  [laulaz]

- Restrict background image field to administrators
  [laulaz]

- Change folders display views order & default
  [laulaz]

- Allow (only) connected users to see default pages in breadcrumbs
  [laulaz]

- Migrate & improve buildout for Plone 6
  [boulch]

- Fix tests for Plone 6
  [boulch]

- Add basic bootstrap styles for Plone 6
  [thomlamb]

- Migrate default_page_warning template to Plone 6
  [laulaz]

- Add missing translation domain
  [laulaz]

- Add basic style for sortable hover
  This style has disappeared in Plone 6 (>< Plone 5)
  [laulaz]

- Fix add/edit forms no-tabbing feature for Plone 6
  [laulaz]


1.0a1 (2021-04-19)
------------------

- Initial release.
  [boulch]
