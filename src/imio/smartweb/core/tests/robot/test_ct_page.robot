# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s imio.smartweb.core -t test_page.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src imio.smartweb.core.testing.IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/imio/smartweb/core/tests/robot/test_page.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Page
  Given a logged-in site administrator
    and an add Page form
   When I type 'My Page' into the title field
    and I submit the form
   Then a Page with the title 'My Page' has been created

Scenario: As a site administrator I can view a Page
  Given a logged-in site administrator
    and a Page 'My Page'
   When I go to the Page view
   Then I can see the Page title 'My Page'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Page form
  Go To  ${PLONE_URL}/++add++Page

a Page 'My Page'
  Create content  type=Page  id=my-page  title=My Page

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Page view
  Go To  ${PLONE_URL}/my-page
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Page with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Page title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
