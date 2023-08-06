*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***

Show how to activate the add-on
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/prefs_install_products_form
    Page should contain element  id=ps.diazo.vanilla
    Assign id to element
    ...  xpath=//*[@id='ps.diazo.vanilla']/parent::*
    ...  addons-psdiazovanilla
    Assign id to element
    ...  xpath=//*[@id='ps.diazo.vanilla']/ancestor::form
    ...  addons-enabled

    Highlight  addons-psdiazovanilla
    Capture and crop page screenshot
    ...  setup_select_add_on.png
    ...  id=addons-enabled
