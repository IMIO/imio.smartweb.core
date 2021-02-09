# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s imio.smartweb.core -t test_procedure.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src imio.smartweb.core.testing.IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/imio/smartweb/core/tests/robot/test_procedure.robot
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

Scenario: As a site administrator I can add a Procedure
  Given a logged-in site administrator
    and an add imio.smartweb.Folder form
   When I type 'My Procedure' into the title field
    and I submit the form
   Then a Procedure with the title 'My Procedure' has been created

Scenario: As a site administrator I can view a Procedure
  Given a logged-in site administrator
    and a Procedure 'My Procedure'
   When I go to the Procedure view
   Then I can see the Procedure title 'My Procedure'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add imio.smartweb.Folder form
  Go To  ${PLONE_URL}/++add++imio.smartweb.Folder

a Procedure 'My Procedure'
  Create content  type=imio.smartweb.Folder  id=my-procedure  title=My Procedure

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Procedure view
  Go To  ${PLONE_URL}/my-procedure
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Procedure with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Procedure title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
