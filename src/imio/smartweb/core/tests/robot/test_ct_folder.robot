# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s imio.smartweb.core -t test_folder.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src imio.smartweb.core.testing.IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/imio/smartweb/core/tests/robot/test_folder.robot
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

Scenario: As a site administrator I can add a Folder
  Given a logged-in site administrator
    and an add Folder form
   When I type 'My Folder' into the title field
    and I submit the form
   Then a Folder with the title 'My Folder' has been created

Scenario: As a site administrator I can view a Folder
  Given a logged-in site administrator
    and a Folder 'My Folder'
   When I go to the Folder view
   Then I can see the Folder title 'My Folder'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Folder form
  Go To  ${PLONE_URL}/++add++Folder

a Folder 'My Folder'
  Create content  type=Folder  id=my-folder  title=My Folder

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Folder view
  Go To  ${PLONE_URL}/my-folder
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Folder with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Folder title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
