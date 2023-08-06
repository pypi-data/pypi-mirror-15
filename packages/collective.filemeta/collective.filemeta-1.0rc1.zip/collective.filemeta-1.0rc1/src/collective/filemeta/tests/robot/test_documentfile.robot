# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.filemeta -t test_documentfile.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.filemeta.testing.COLLECTIVE_DOCUMENTFILE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_documentfile.robot
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

Scenario: As a site administrator I can add a DocumentFile
  Given a logged-in site administrator
    and an add documentfile form
   When I type 'My DocumentFile' into the title field
    and I submit the form
   Then a documentfile with the title 'My DocumentFile' has been created

Scenario: As a site administrator I can view a DocumentFile
  Given a logged-in site administrator
    and a documentfile 'My DocumentFile'
   When I go to the documentfile view
   Then I can see the documentfile title 'My DocumentFile'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add documentfile form
  Go To  ${PLONE_URL}/++add++DocumentFile

a documentfile 'My DocumentFile'
  Create content  type=DocumentFile  id=my-documentfile  title=My DocumentFile


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the documentfile view
  Go To  ${PLONE_URL}/my-documentfile
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a documentfile with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the documentfile title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
