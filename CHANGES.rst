Changelog
=========


1.0.4 (2022-03-16)
------------------

- Improve leaflet css
  [thomlamb]

- Change leaflet tilelayer style
  [thomlamb]


1.0.3 (2022-03-09)
------------------

- Change leaflet style
  [thomlamb]

- Adding info popup on leaflet marker
  [thomlamb]

- Add correct href on search link for tab navigation
  [thomlamb]


1.0.2 (2022-03-08)
------------------

- Add missing init file for faceted widgets
  [laulaz]


1.0.1 (2022-02-25)
------------------

- Removal of the pointer if it is located at Imio (event and library view)
  [thomlamb]

- Added times and fixed date display for event views
  [thomlamb]

- Override eea.facetednavigation select widget template.
  Display label as first value in select fields
  [boulch]

- Add placeholder to faceted text search (xml) + upgrade step
  [boulch]

- Fix : Add a missing tal instruction
  [boulch]

- Use new icons radio widget to select SVG icon for links
  [laulaz]

- Avoid problems with minisite & subsite simultaneous activation (for example,
  through a cached action)
  [laulaz]


1.0 (2022-02-22)
----------------

- Add description in sendinblue section
  [boulch]

- Add conditions on faceted and folder view (with images).
  When we select one of this view and if a content hasn't image we display a no-image class
  [boulch]

- Fix css for news items
  [thomlamb]

- Change event contact icon
  [thomlamb]

- Override social tags generation to get scaled images instead of full size.
  We didn't override syndication to avoid any side effects in RSS / Atom
  [laulaz]


1.0a43 (2022-02-21)
-------------------

- Limitate usage of site search settings to current website search
  [mpeeters]


1.0a42 (2022-02-21)
-------------------

- Fix RelatedItems fields browser in minisite
  [boulch, laulaz]

- Fix bad html link for news items
  [thomlamb]

- Fix removed section subscriber. if we removed a folder, pages with sections stayed in catalog
  [boulch]


1.0a41 (2022-02-16)
-------------------

- Fix loadmore react views
  [thomlamb]

- Update Axios module to 26.0
  [thomlamb]

- Add AbortController to prevent unnecessary requests
  [thomlamb]

- Use `use_site_search_settings` parameters by default to inherit query parameters from site search settings
  for `@search` endpoint
  [mpeeters]


1.0a40 (2022-02-14)
-------------------

- Fix bug with react import img
  [thomlamb]


1.0a39 (2022-02-14)
-------------------

- Fix missing value for placeholder
  [thomlamb]


1.0a38 (2022-02-14)
-------------------

- Fix condition to display search items img
  [thomlamb]


1.0a37 (2022-02-14)
-------------------

- Fix problem with react event map
  [thomlamb]

- Add background image for result search items
  [thomlamb]

- Refactor all js indent
  [thomlamb]

- Add placeholder class on contact logo & leadimage when they are empty
  [laulaz]

- Change/fix max number (30) of possible sections in pages before paging
  [boulch]

- Add new div with a nb-items-batch-[N] class
  to ease stylizing multi items templates (table, carousel)
  [boulch]

- Fix bad css value
  [thomlamb]


1.0a36 (2022-02-11)
-------------------

- Update e-guichet icon file & add new shopping icon
  [laulaz]

- Change default value for batch size in files section
  [laulaz]

- Improve css
  [thomlamb]

- Avoid fetching contact from authentic source multiple times on the same view
  [laulaz]


1.0a35 (2022-02-10)
-------------------

- Use css class & background style also on footers sections
  [laulaz]

- Correction of spelling mistakes
  [thomlamb]

- Get events with new event_dates index
  [laulaz]

- Change footer markup to have only one row
  [laulaz]

- Add new e-guichet icon
  [laulaz]

- Remove GDPR link from footer (it is already in colophon)
  [laulaz]

- Restore removed class to help styling carousel by batch size
  [laulaz]


1.0a34 (2022-02-09)
-------------------

- Fix missing permissions to add footer
  [laulaz]

- Fix default item view for a collection when anonymous
  [laulaz]

- Fix double escaped navigation items in quick accesses
  See https://github.com/plone/plone.app.layout/issues/280
  [laulaz]


1.0a33 (2022-02-08)
-------------------

- Fix search axios to not fetch with no filter set
  [thomlamb]


1.0a32 (2022-02-08)
-------------------

- Change Youtube & Parking base icons, and add Twitter
  [laulaz]

- Add id on sections containers to ease styling
  [laulaz]

- Be sure to reindex the container (& change modification date for cachinig) when
  a page has been modified
  [laulaz]

- Reorder SectionContact template + modify some translations
  [boulch]

- Fix generated url for search results
  [thomlamb]

- Unauthorize to add imio.smartweb.SectionSendinblue on a Page but authorize it on PortalPage.
  [boulch]

- Include source item url for `@search` service results
  [mpeeters]

- Enforce using SolR for `@search` service
  [mpeeters]

- Fix translation domain for event macro
  [laulaz]


1.0a31 (2022-02-04)
-------------------

- Disable sticky map on mobile
  [thomlamb]

- Refactor : Displaying dates from section event is now in a macro to have more html flexibility
  [boulch, laulaz]


1.0a30 (2022-02-03)
-------------------

- Allow to set instance behaviors on page or on procedure objects
  [boulch, laulaz]

- Improve react vue for mobile
  [thomlamb]

- Change static js and css for mobile responsive search
  [thomlamb]

- Simplifying faceted macros
  [boulch]


1.0a29 (2022-02-03)
-------------------

- Fix error in navigation when filtering on workflow state
  [laulaz]

- Adapt faceted macros to discern section video and other contents. Fix video redirect link thanks to css.
  [boulch]


1.0a28 (2022-02-01)
-------------------

- Fix navigation in subsites after navtree_depth property removal
  See https://github.com/plone/plone.app.layout/commit/7e2178d2ae11780d9211c71d8c97e4f81cd27620
  [laulaz]

- Update buildout to use Plone 6.0.0a3 packages versions
  [boulch]

- Allow collections as folders default view
  [laulaz]

- Add links on folder titles in navigation
  [laulaz]

- Fix double escaped navigation items
  See https://github.com/plone/plone.app.layout/issues/280
  [laulaz]


1.0a27 (2022-01-31)
-------------------

- Add upgrade step to check contact itinerary if address is in visible blocks
  [boulch]

- Contact itinerary go out of contact address. Itinerary is displaying thanks to a new visible_blocks option value
  [boulch]

- Improve and resolv bug in load more in react vue
  [thomlamb]

- Add new Sendinblue newsletter subscription section
  [laulaz]

- disabling filter resets on search load (important, to settle a conflict with other react views)
  [thomlamb]

- Precision so that the css of the search is unique to itself
  [thomlamb]


1.0a26 (2022-01-27)
-------------------

- Disable input search limit
  [thomlamb]

- Small correction of rendered data in views and scss
  [thomlamb]

- Fix local search when no text in input
  [thomlamb]


1.0a25 (2022-01-27)
-------------------

- Avoid page reload after gallery spolight close
  [laulaz]

- Fix default value for search filters
  [thomlamb]

- Fix open_in_new_tab option for BlockLinks
  [laulaz]

- Allow some python modules in restricted python (Usefull for collective.themefragments modules)
  [boulch]

- Add offcanvas bootstrap component in a viewlet and inherit from search browserview
  [boulch, thomlamb]

- Always keep (empty) placeholder div in carousel/table templates even if item
  has no image
  [laulaz]

- Fix traceback when section selection target has no description
  [laulaz]


1.0a24 (2022-01-26)
-------------------

- New react build
  [thomlamb]

- Adding loadmore for react vue
  [thomlamb]

- Improved query for search filters
  [thomlamb]

- Link changes for search results.
  [thomlamb]

- Update generated url for search items to match with react vue.
  [thomlamb]

- Fix street address formatting (number after street name)
  [laulaz]

- Add new css class in text section to stylize figure based on their size
  [boulch]

- Add @@is_eguichet_aware view to get e-guichet configuration/connexion status
  [boulch]


1.0a23 (2022-01-19)
-------------------

- Update buildout to use Plone 6.0.0a2 released version
  [laulaz]

- Avoid traceback when trying to display an empty schedule
  [laulaz]

- Add breadcrumb to some select box in smartweb settings.
  [boulch]


1.0a22 (2022-01-13)
-------------------

- Add dynamic style for leaflet. + general styles
  [thomlamb]


1.0a21 (2021-12-16)
-------------------

- Adding load more button for react list element
  [thomlamb]

- Improvement js of the Schedule popup
  [thomlamb]

- Change image size scales (that were too small)
  [laulaz]

- Add events dates in events section
  [laulaz]

- Make HTML section folderish (can contain Images and Files)
  [laulaz]

- Add description on HTML section
  [laulaz]

- Section contact : Share address into 3 parts (street, entity, country) and display these parts into span
  [boulch]

- Javascript refactoring
  [thomlamb]

- Distribution of css in the global file
  [thomlamb]

- Add global style for all component.
  [thomlamb]

- Add removeAccents js for string url
  [thomlamb]

- Add "with-background" css class on sections that have a background image
  [laulaz]

- Add items category in news / events section
  [laulaz]

- Add news items publication date in news section
  [laulaz]

- Add option to display items descriptions in news / events / selection sections
  [laulaz]


1.0a20 (2021-12-06)
-------------------

- Change markup and css classes for carousel / table templates
  [laulaz]

- Set SolR connections for external sources
  [mpeeters]

- Add routing for react search vue.
  [thomamb]


1.0a19 (2021-12-01)
-------------------

- Avoid an unwanted behavior with `path` index combined with SolR and virtual host
  [mpeeters]


1.0a18 (2021-12-01)
-------------------

- Avoid batching on vocabularies : contact categories and entity events
  [laulaz]

- Add plone.shortname behavior on all sections
  [laulaz]

- Restrict search inside minisites
  [laulaz]

- Fix footer viewlet markup to be included in Plone footer
  [laulaz]

- Add faceted layout class to body if a faceted layout is define.
  [boulch]


1.0a17 (2021-11-29)
-------------------

- Move background_style (img background) out of sections (section-container div) and
  put it in pages view (sortable-section div). This simplifying css styling.
  [boulch]

- Split section macros to "manage macros" to manage sections and "title macros" to print sections title + add default Plone "container" css class.
  [boulch]

- Change generated url for the news and event sections for compatibility with react router
  [thomamb]


1.0a16 (2021-11-26)
-------------------

- Add profile to handle bundles last_compilation dates
  [laulaz]

- Add new css styles
  [thomlamb]

- Udpate data for content items view
  [thomlamb]

- Refactor css className
  [thomlamb]

- Add moment js to parsed date
  [thomlamb]

- New build of react vue
  [thomlamb]

- Disallow hiding title on a collapsable section
  [laulaz]

- Fix bootstrap classes for table batches
  [laulaz]

- Can define specific events to get (instead of all events from an agenda)
  [boulch]

- Use Swiper instead of Bootstrap carousel
  [thomlamb, laulaz]


1.0a15 (2021-11-24)
-------------------

- Allow to override / limit icons TTW (portal_resources)
  [laulaz]

- React Routge improvement
  [thomlamb]

- Refactor css className
  [thomlamb]

- fix a problem or react call the endpoint several times
  [thomlamb]

- New react build
  [thomlamb]

- Allow from 1 to 8 links per batch in links section
  [laulaz]

- Add more icons and use English names and titles for icons
  [laulaz]

- Change HTML field help to describe how to use it
  [laulaz]

- Hide icons profile from installer
  [laulaz]

- Fix banner not displaying in minisites
  [laulaz]

- Remove "Hide/Display banner from this item" link on banner in Preview mode
  [laulaz]


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
