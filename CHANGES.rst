Changelog
=========


1.2.8 (2023-11-23)
------------------

- Fix (lead) image sizes URLs for text section & migrate old values
  [boulch, laulaz]


1.2.7 (2023-11-22)
------------------

- Fix image scales URLs for gallery view thumbnails
  [laulaz]

- WEB-3992 : Uncheck icon when clincking on checked icon (in edit form of imio.smartweb.BlockLink)
  [boulch]


1.2.6 (2023-11-21)
------------------

- Fix tests after scales dimensions change
  [laulaz]


1.2.5 (2023-11-20)
------------------

- Rebuild React to fix js errors
  [thomlamb]

- WEB-4017 : Add Number 2 for items per batch
  [thomlamb]

- Fix last upgrade steps: when run from command line, we need to adopt admin
  user to find private objects
  [laulaz]

- Fix wrong type name in `imio.smartweb.CirkwiView` type profile
  [laulaz]

- WEB-4014 : Display "websites" urls instead of labels (facebook, website, instagram, ...)
  [boulch]

- WEB-4012 : Restored filter on related contacts field
  [boulch]


1.2.4 (2023-10-30)
------------------

- Handle image orientation on faceted map layout
  [laulaz]

- Remove unused Photo Gallery from collections layouts
  [laulaz]


1.2.3 (2023-10-29)
------------------

- Migrate deprecated image scales from Section Contact / Gallery
  [laulaz]

- Migrate "Is in portrait mode" option to orientation behavior for Section Contact
  [laulaz]

- Handle image orientation on Collection & Foler types
  [laulaz]

- Remove unused `gallery_view.pt` template
  [laulaz]

- Change order of orientation options (default first)
  [laulaz]

- Handle orientation in REST views images & fix galleries
  [laulaz]

- Change default orientation to landscape
  [laulaz]


1.2.2 (2023-10-26)
------------------

- WEB-3985 : Fix condition to load image or logo in contact view
  [thomlamb]

- WEB-3985 : Fix logo scale URL (no orientation there) for Directory view
  [laulaz]

- WEB-3985 : Fix React build
  [thomlamb]


1.2.1 (2023-10-25)
------------------

- WEB-3985 : Fix traceback when cropping scale information is not present on image change
  [laulaz]


1.2 (2023-10-25)
----------------

- WEB-3985 : New portrait / paysage scales & logic.
  We have re-defined the scales & sizes used in smartweb.
  We let the user crop only 2 big portrait / paysage scales and make the calculation behind the scenes for all
  other smaller scales.
  We also fixed the cropping information clearing on images changes.
  A new orientation behavior allow the editor to choose with type of image he wants.
  [boulch, laulaz]

- Fix css for Event content view
  [thomlamb]


1.1.30 (2023-10-24)
-------------------

- Adaptation of react to show or hide the map
  [thomlamb]

- WEB-3999 : Keep order of contacts in its view through manualy sorted related_contacts in edit form
  [boulch]


1.1.29 (2023-10-18)
-------------------

- SUP-32814 : Add new external content plugins : GiveADayPlugin
  see : https://github.com/IMIO/imio.smartweb.core/commit/a4dfca2
  [boulch]

- WEB-4000 : Add display_map Bool field on directory and events views
  [boulch]


1.1.28 (2023-10-13)
-------------------

- WEB-3803 : Add upgrade step : collective.pivot.Family content type can be add in an imio.smartweb.Folder
  [boulch]

- WEB-3998 : Set requests timeout to 8'' when we populate RemoteContacts vocabulary
  [boulch]


1.1.27 (2023-10-11)
-------------------

- Add <div> in view_argis.pt template to fix map displaying
  [thomlamb, jhero]


1.1.26 (2023-10-10)
-------------------

- Add missing upgrade step to add leadimage behavior on external content section
  [boulch]

- Fix some translations in external content plugins
  [boulch]


1.1.25 (2023-10-09)
-------------------

- SUP-32169 : Add new external content plugins : ArcgisPlugin
  [boulch]


1.1.24 (2023-10-09)
-------------------

- WEB-3986 : Fix : email must be open thank to "mailto:" tag instead of "tel:"
  [boulch]

- WEB-3984 : Remove deprecated cropping annotations on banner
  [boulch, laulaz]

- WEB-3984 : Don't get banner scale anymore. Get full banner image directly
  [boulch, laulaz]

- WEB-3984 : Remove banner field from cropping editor
  [laulaz]


1.1.23 (2023-09-06)
-------------------

- WEB-3983 : Fix contacts bootstrap grid
  [boulch]

- WEB-3980 : Fix help and authentic sources menus double displaying in folder_contents view
  [boulch]

- fix calculating image size on loading (add async in useEffect)
  [thomlamb]

- WEB-3981 : Add Cognitoforms as an external section
  [boulch]

- WEB-3932 : Transform contact section to contactS section
  [laulaz, boulch]


1.1.22 (2023-08-29)
-------------------

- Add smartweb content types icons (Message, MessagesConfig)
  [boulch]

- Delete useless css for edition
  [thomlamb]


1.1.21 (2023-08-29)
-------------------

- Add smartweb content types icons
  [laulaz, boulch]

- Show help & authentic sources menus only if product is installed
  [laulaz, boulch]

- Update compiled resources to fix help menu
  [boulch]

- Refactor Plausible
  [remdub]


1.1.20 (2023-08-28)
-------------------

- Fix display of hours on events react view
  [thomlamb]

- Refactor React contact view
  [thomlamb]

- Refactor section text : image_size field is no more required because field is now hidden!
  [boulch]

- WEB-3957 : Add new "Please help!" menu in Plone toolbar
  [boulch]

- Display logo if no image in react contact card.
  Display blurry background if image is in portrait
  [thomlamb]

- Fix of the calculation of the batch zise, ​​addition instead of concatenation
  [thomlamb]

- WEB-3972 : Add "elloha" plugin in external content section
  [boulch]


1.1.19 (2023-08-07)
-------------------

- WEB-3956 : Update folder modification date when its layout changed to fix cache
  [boulch]

- WEB-3934 : Hide image_size field
  [boulch]

- WEB-3953 : Remove cropping from background_image field
  [boulch]

- WEB-3952 : Disable image cropping on section text
  [laulaz, boulch]

- Make "Image cropping" link conditional
  [laulaz]

- Disable image cropping on Slide content type
  [laulaz]

- Fix condition for image placeholder on React vue
  [thomlamb]


1.1.18 (2023-06-19)
-------------------

- Removal of unnecessary css in sections contact and gallery
  [thomlamb]

- Add new browserview for Plausible
  [remdub, boulch]

- Change some icons : SectionHTML and SectionExternalContent
  [boulch]

- MWEBTUBA : Add new section : imio.smartweb.SectionExternalContent (Manage embeded contents)
  [boulch]


1.1.17 (2023-05-31)
-------------------

- New React build
  [thomlamb]

- Use hash in gallery images URL for directory, events and news rest views
  (based on modification date) to allow strong caching.
  [boulch, laulaz]


1.1.16 (2023-05-25)
-------------------

- Fix faceted map size after page loading.
  [thomlamb]

- Adapt `@search` endpoint to handle multilingual
  [mpeeters]


1.1.15 (2023-05-22)
-------------------

- Fixed console error following unnecessary loading of js for swiper
  [thomlamb]

- Avoid image cropping for banner scale (will have infinite height)
  [laulaz]

- Cleanup `folder_contents` properties & add warning about Sections
  [laulaz]

- Store hash in an annotation to refresh "dynamic" sections
  [boulch, laulaz]

- WEB-3868 : Remove useless code (included in Plone 6.0.4)
  See https://github.com/plone/plone.base/pull/37
  [laulaz]

- Migrate to Plone 6.0.4
  [boulch]

- Update static icon for better css implements
  [thomlamb]

- SUP-30074 : Fix broken RelationValue "AttributeError: 'NoneType' object has no attribute 'UID'
  [boulch]


1.1.14 (2023-04-25)
-------------------

- Fix image display condition
  [thomlamb]

- Fix json attributes to get the scaling pictures of news
  [boulch]


1.1.13 (2023-04-24)
-------------------

- Compile resources
  [boulch]


1.1.12 (2023-04-14)
-------------------

- WEB-3868 : Forbid creating content with same id as a parent field
  [laulaz]

- Don't use `image_scales` metadata anymore to get images scales URLs because we
  had problems with cropped scales (they were not indexed).
  We now use a hash in URL (based on modification date) to allow strong caching.
  See https://github.com/collective/plone.app.imagecropping/issues/129
  [laulaz, boulch]


1.1.11 (2023-04-05)
-------------------

- WEB-3913 : Leadimages should not appear on rest views
  [boulch]


1.1.10 (2023-03-31)
-------------------

- WEB-3901 : Get fullsize picture if scale is not present (section collection)
  [boulch]

- WEB-3908 : Call new @events endpoint to get events occurrences
  [boulch]


1.1.9 (2023-03-17)
------------------

- WEB-3898 : Prevent error (error while rendering imio.smartweb.banner) if a content has his id = "banner"
  [boulch]


1.1.8 (2023-03-15)
------------------

- WEB-3888 : We overrided link_input template widget to allow any link format in external tab (without browser blocking)
  [boulch]

- WEB-3769 : Get fullsize picture if scale is not present (ex: picture too small)
  [boulch]

- SUP-27477 : Fix internal link in herobanner
  [boulch]


1.1.7 (2023-03-07)
------------------

- Improved react views to better match bootstrap media queries and fix no wrap buttons
  [thomlamb]

- Fix no display img in news view
  [thomlamb]

- Migrate to Plone 6.0.2
  [boulch]

- WEB-3865 : Ordering news section and events section in their views thanks to a manualy order in their widgets
  [boulch]

- Avoid auto-appending new lines to Datagrid fields when clicked
  [laulaz]

- Fix annuaire, agenda, news sections with current language
  [boulch]


1.1.6 (2023-02-22)
------------------

- WEB-3863 : Fix some dates displaying
  [boulch]

- WEB-3858 : Fix displaying of authentic sources menu
  [boulch]


1.1.5 (2023-02-20)
------------------

- Delete lorem in React vue
  [thomlamb]

- Fixed accessibility nav attribute
  [thomlamb]

- Fixed faceted map
  [boulch]

- WEB-3837 : Can define specific news to get (instead of all news from news folders)
  [boulch]

- Adding display block on active dropdown
  [thomlamb]

- Fix traduction ID for React
  [thomlamb]


1.1.4 (2023-01-31)
------------------

- Fix loader on React vue + add visual loader
  [thomlamb]


1.1.3 (2023-01-30)
------------------

- WEB-3819 : Update permission : local manager can manage their subsites
  [boulch]


1.1.2 (2023-01-27)
------------------

- Adding react-translated and translate static React txt
  [thomlamb]

- Fix "zope.schema._bootstrapinterfaces.ConstraintNotSatisfied" in smartweb settings
  [boulch]

- Add new content type : imio.smartweb.CirkwiView
  [boulch, laulaz]

- Add authentic sources menu in toolbar
  [boulch, laulaz]

- WEB-3755 : Adapt empty (without section) procedure message
  [boulch, laulaz]

- Bring current-language attribute in rest views templates (useful for translations in JS)
  [boulch]

- Handle search result types depending on available authentic sources for site
  [Julien]

- Replacement of hard coded urls for images
  [thomlamb]


1.1.1 (2023-01-12)
------------------

- Use generated image scale urls to increase image caching
  [boulch, laulaz]

- Forbid minisite to be copied / moved inside another minisite
  [laulaz]

- Allow querying contact category with React filter (A) while also querying
  multiple categories defined in directory REST endpoint (B, C): A and (B or C)
  [laulaz]

- Enable autopublishing behavior on all types
  [laulaz]

- Handle events occurences in REST endpoint
  [laulaz]

- Multilingual: handle language in requests for REST views, handle LRF navigation
  roots (minisites, footers, default pages, vocabularies), fix language selector
  viewlet
  [laulaz]

- Add upgrade step to change content types icons
  [laulaz]

- Fix JS / CSS bundles names (restore old names : '-' instead of '.' separator)
  [laulaz]


1.1 (2022-12-23)
----------------

- Update to Plone 6.0.0 final
  [boulch]

- WEB-3795 : Add Proactive trigger code to chatbot.
  [remdub]


1.0.27 (2022-11-23)
-------------------

- Add check for multiple categories directory views
  This is used to decide if the field will be changed to single category
  [laulaz]


1.0.26 (2022-11-22)
-------------------

- WEB-3729 : Add site admin permission on action for managing taxonomies on specific contents
  [boulch]

- WEB-3777: Make nb_results field work on React views (as batch size)
  [laulaz, thomlamb]


1.0.25 (2022-10-28)
-------------------

- WEB-3771 : Harmonize procedure button label
  [boulch]

- WEB-3777 : Fix DirectoryEndpoint filter by category
  [boulch, laulaz]

- WEB-3759 : Add portrait class even if there is no lead image to set placeholder with a good size
  [boulch]


1.0.24 (2022-10-20)
-------------------

- Fix problem with images url in logo
  [boulch]


1.0.23 (2022-10-20)
-------------------

- Fix problem with images urls in collections
  [boulch]


1.0.22 (2022-10-18)
-------------------

- Fix problem with images urls in faceted navigation
  [laulaz]

- WEB-3766 : Ensure displaying pages / footers even if sections in error (+ display section in error)
  [boulch, laulaz]

- WEB-3764 : Fix : We Ensure we always compare Decimal
  [boulch]


1.0.21 (2022-10-07)
-------------------

- Waiting for authentics sources Plone6betaX to get automaticaly images scale hash on objects
  [boulch]


1.0.20 (2022-10-05)
-------------------

- Fix React-moment: replace 'day' by 'minute' in sratOf fuction to fix bad hours display in news view
  [thomlamb]

- Add fullobjects=1 to get inner events and inner directory contents
  [boulch]

- Adding section files download and gallery in react content view
  [thomlamb]

- Update svg plone-icon for better compatibility with color css
  [thomlamb]

- Use unique scale path (with hash) for better cache management
  [boulch, laz]


- Memoize EventsTypesVocabulary because that almost never change !
  [boulch]

- WEB-3684 : Add fullobjects=1 to get inner news contents
  [boulch]
- Use custom spotlight to avoid bad gallery refresh
  [boulch]

- Migrate to Plone 6.0.0b1 : ensure all needed attributes are allowed (otherwise
  action expressions doesn't work anymore), consider new SVG / icons logic in
  tests, use new simplified resources registry
  [laulaz, boulch]


1.0.19 (2022-09-08)
-------------------

- WEB-3750 : Fix topics, categories and facilities items in selectboxes view when there is no preset selected categories
  [boulch]


1.0.18 (2022-09-06)
-------------------

- Fix css to display none accueil item in nav
  [thomlamb]


1.0.17 (2022-09-01)
-------------------

- WEB-3741 : Fix items in selectbox contact categories in rest view @search-filters endpoint ("match" with items in edit selectbox)
  Fix contacts results depends of selected category in rest view (@search endpoint)
  [boulch]

- WEB-3732 : Add smartweb settings to customize sendinblue subscribing button (text and position)
  [boulch]

- Fix bad position for swipper-button in herobanner
  [thomlamb]

- Ensure navigation elements don't use an already reserved/existing css Class
  [boulch]

- WEB-3730 : By default, Plone open external (Section text / Tiny) links in new tab
  [boulch]


1.0.16 (2022-08-02)
-------------------

- Fix rich description display on contact section
  [laulaz]


1.0.15 (2022-07-25)
-------------------

- WEB-3687: Add botpress viewlet in footer
  [remdub]

- Change class and css to make herobanner slider work
  [thomlamb]


1.0.14 (2022-07-14)
-------------------

- Avoid error on broken objects (reindex_all_pages upgrade step)
  [laulaz]


1.0.13 (2022-07-14)
-------------------

- Adding button for add news,events,contacts
  [thomlamb]

- Avoid traceback if a selection item relation is broken
  [laulaz]

- Use rich description on contact sections
  [laulaz]

- [WEB-3674]Fix itinerary links
  [remdub]

- [WEB-3661]Set b_size to 100 on search results
  [remdub]

- Add collective.faceted.map with custom template & markers popups
  [boulch, laulaz]

- Allow pages to be geolocalized (latitude/longitude indexes) via their first map section
  [laulaz]

- Use new registry settings to store URL of news/events/contact proposal form
  [laulaz]


1.0.12 (2022-06-07)
-------------------

- Adapt code to ease development with local sources
  [mpeeters]
- [WEB-3663] Fix contact schedule. Use Decimal instead of float. ( float("8.30") = 8.3.  8h03 != 8h30 )
  [boulch]

- Update static css for edit view
  [thomlamb]

- Fix NaN value for batchsize in swiper
  [thomlamb]

- Ban required URL when Footer or HeroBanner modified
  [boulch, laulaz]

- Omit some fields in slide section layout fieldset
  [boulch]


1.0.11 (2022-05-17)
-------------------

- Update display for date in news view
  [thomlamb]

- Add video,social,web url for news view
  [thomlamb]

- Update regex for routing items
  [thomlamb]

- Add carousel and gallery in contact view
  [boulch]

- Fix batch size (40) for pages pagination
  [laulaz]

- Add new content type : imio.smartweb.SectionPostit
  [boulch, laulaz]


1.0.10 (2022-05-10)
-------------------

- Add description for directory items
  [thomlamb]

- Fix css for react items
  [thomlamb]

- Adaptation of the jsx to be able to render the markdown to html
  [thomlamb]

- Adapt `@search` endpoint to exclude expired elements and events in the past
  [mpeeters]

- Remove forced placeholder for image in react pages
  [thomlamb]


1.0.9 (2022-05-02)
------------------

- Remove duplicate / useless new icons & change default workinfos icon
  [laulaz]


1.0.8 (2022-05-02)
------------------

- Add new icons
  [boulch]

- Fix section edition display for herobanner / content-core / footer
  [laulaz]

- HeroBanner can't be a folder default view
  [boulch]


1.0.7 (2022-04-25)
------------------

- Improve slide view html
  [thomlamb]

- Clean core css
  [thomlamb]

- Fix herobanner when there is a default (portal)page on site root or on partner sites
  [boulch, laulaz]

- Hide unwanted upgrades from site-creation and quickinstaller
  [boulch]

- Move local manager role and sharing permissions to imio.smartweb.common
  Use new common.interfaces.ILocalManagerAware to mark a locally manageable content
  [boulch]

- Add hero banner feature
  [boulch]


1.0.6 (2022-03-29)
------------------

- Fix: Change Leaflet Tilelayer map for fix bad attribution url
  [thomlamb]


1.0.5 (2022-03-28)
------------------

- Add local permissions and a "Local Manager" role.
  Permissions : imio.smartweb.core.CanEditMinisiteLogo, imio.smartweb.core.CanManageSectionHTML
  [boulch]

- Updated queries for search to only run with specific filters
  [thomlamb]

- Handle inline SVG images for portal logo and minisite logo
  [laulaz]

- Add show_items_lead_image attributes on files section.
  Add no-image css class in table template when there is no image to display
  [boulch]

- Add sections to procedure content type to be similar as page content type
  [boulch]

- Add a portrait mode on section contact leadimage
  [boulch]

- Exclude parents (folders) messages to traverse into partners sites
  [boulch]

- Exclude Footers from parent listings by default
  [laulaz]


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
