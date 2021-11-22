Changelog
=========


1.0a14 (2021-11-22)
-------------------

- Force endpoints returning values as JSON
  [laulaz]

- Update news root and refactor code
  [thomlamb]

- prettify code and delete useless state
  [thomlamb]

- Add responsible 16:9 ratio on embed videos
  [laulaz]

- Add collapsable option for sections (click on section title opens section body)
  [laulaz]

- Add SVG icon option for block links, with icon resolver and basic icons set
  [laulaz]

- Cleanup useless code
  [laulaz]


1.0a13 (2021-11-17)
-------------------

- Change url for fetch search filters data.
  [thomlamb]


1.0a12 (2021-11-16)
-------------------

- Add blocks / list faceted layouts and (automatic) criteria configuration for
  collections
  [laulaz]

- Add new fields on rest views (event types, contact categories) to filter
  results and adapt endpoints
  [boulch]

- Refactor folder views html code to simplify it & make it more efficient (no
  more waking up of objects)
  [laulaz]

- Remove e_guichet action (replaced by generic account action) and add css class
  on all header actions
  [laulaz]

- Add text on search link for acessibility
  [laulaz]

- Adapt `@search` endpoint to be context based for SolR searches
  [mpeeters]

- Change max results logic for a number of batches (collection / events / news)
  [laulaz]

- Add React search view
  [thomlamb]

- Fix SearchableText indexing for links / video sections (new) descriptions
  [laulaz]

- Define cropping scales for all contents / fields
  [laulaz]

- Add/fix bootstrap classes on table / carousel views for batches
  [laulaz]

- Change image scales for listing (liste) / blocks (vignette) view and table
  view (liste / vignette), depending on batch size
  [laulaz]

- Change image scale (affiche) for sections background images
  [laulaz]

- Use background images (instead of `<img>`) in table template
  [laulaz]

- Add (rich) description on Video section
  [laulaz]

- Change some fields titles
  [laulaz]

- Fix @@search view (use ours instead of collective.solr)
  [laulaz]


1.0a11 (2021-11-05)
-------------------

- Adapt SolR search to reflect removal of `selected_entity` on `DirectoryView` content type
  [mpeeters]

- Implement cross core SolR search
  [mpeeters]

- Add category_and_topics index, vocabulary and configuration related code
  [jimbiscuit, mpeeters]

- CSS fixes / improvements
  [thomlamb]

- Code refactoring
  [laulaz]

- Add React views and machinery
  [thomlamb, duchenean]

- Add cropping support and define cropping scales per content / field
  [laulaz]

- Change viewlets structure
  [laulaz]

- Compute custom body class (minisite / subsite / banner)
  [laulaz]

- Improve all sections / fields / forms / views / templates markup / a11y
  [boulch, laulaz]

- Add locking support for sections
  [laulaz]

- Add collective.anysurfer dependency
  [boulch]

- Change navigation markup (quickaccess, close / prev buttons, etc)
  [laulaz]

- Add new types : EventsView, NewsView, DirectoryView, SectionHTML, SectionMap,
  PortalPage, SectionNews, SectionEvents, SectionCollection, SectionSelection
  [boulch, laulaz]

- Fix schedule display in Contact section (days delta, format & translations)
  [laulaz]

- Put subsite logo & navigation viewlets in a new viewlet manager (to have custom
  html around them). Previous viewlets are also kept separate (& hidden), in
  case we need to split them.
  [laulaz]

- Add itinerary link on contact section
  [laulaz]

- Add logo & lead image on contact section
  [laulaz]

- Change linked contact field description
  [laulaz]

- Cleanup old QuickAccess behavior
  [laulaz]


1.0a10 (2021-07-26)
-------------------

- Improve contacts search (sorted correctly & no batching anymore)
  [laulaz]


1.0a9 (2021-07-16)
------------------

- Update pages / procedures categories taxonomies
  [laulaz]

- Override basic widget template to move description up to input field (jbot)
  [boulch]

- Fix : dont display blocks title if display block is False.
  [boulch]

- Display subcontacts from imio.directory.Contact into section contact view.
  [boulch]

- Fix missing `Add new` menu on folderish sections
  [laulaz]


1.0a8 (2021-07-12)
------------------

- Display schedule in section contact
  [boulch]

- Fix subsite and minisite permissions
  [boulch]


1.0a7 (2021-07-07)
------------------

- Add imio.smartweb.common (imio.smartweb.topics behavior with topics vocabulary)
  [boulch]

- Add link to imio.gdpr legal text in Footer
  [boulch]

- Add custom permissions to manage Subsite and Minisite
  [boulch]

- Authorize adding `Message` (from collective.messagesviewlet) content types in imio.smartweb.Folder
  [boulch]


1.0a6 (2021-06-11)
------------------

- Override plone logo viewlet to display minisite logo
  [boulch]

- improve sections and pages indexing
  [laulaz]

- Add new section : imio.smartweb.SectionSelections
  [boulch]

- Add quick_access_items behavior on imio.smartweb.Folder
  [boulch]

- Change minisite properties & dependency with subsite
  [laulaz]

- Fix : Can not add minisite in another minisite
  [boulch]

- Add bold text in description
  [boulch]


1.0a5 (2021-06-03)
------------------

- Subsite logo is a link to subsite root
  [boulch]

- Enable minisite only on a container in PloneSite root
  [boulch]

- Can not enable subsite on minisite
  [boulch]

- Can not enable minisite on a subsite
  [boulch]

- Added style for correct background display
  [thomlamb]

- Add Minisites
  [boulch, laulaz]

- Hide Title for SectionText
  [boulch, laulaz]

- Remove workflows for SectionFooter and SectionContact
  [boulch, laulaz]

- Reorder SectionContact
  [boulch, laulaz]


1.0a4 (2021-05-26)
------------------

- Add can_toggle_title_visibility property on sections. Use it on Contact section.
  [boulch, laulaz]

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

- Move field category in categorization fieldset
  [boulch]

- Hide leadimage caption field everywhere (editform, addform)
  [boulch]


1.0a3 (2021-04-23)
------------------

- improved css for subsite navigation
  [thomlamb]

- Harmonize all sections templates. Rename some css class. Add new css class.
  [boulch, thomlamb]

- Add row class in page view template to be bootstrap aware.
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
