*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}  nelkut-test.fly.dev
${DELAY}  0.5 seconds
${HOME_URL}  http://${SERVER}
${ADD_URL}  http://${SERVER}/add
${INPROCEEDING_URL}  http://${SERVER}/add_inproceeding

*** Keywords ***
Open And Configure Browser
    # jos käytät Firefoxia ja Geckodriveriä käytä seuraavaa riviä sitä alemman sijaan
    # ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
    ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
    Call Method    ${options}    add_argument    --no-sandbox
    # seuraava rivi on kommentoitu toistaiseksi pois
    # Call Method  ${options}  add_argument  --headless
    Open Browser  browser=chrome  options=${options}
    Set Selenium Speed  ${DELAY}

Go To Add Page
    Go To  ${ADD_URL}

Home Page Should Be Open
    Title Should Be  Index

Add Page Should Be Open
    Title Should Be  New Reference

Add Inproceeding Page Should Be Open
    Title Should Be  New Reference

Add Article Page Should Be Open
    Title Should Be  New Reference

Add Book Page Should Be Open
    Title Should Be  New Reference

Go To Main Page
    Go To  ${HOME_URL}
    Home Page Should Be Open

Submit Registration
    Click Button  Register

Set Username
	[Arguments]  ${username}
	Input Text  username  ${username}

Set Password
	[Arguments]  ${password}
	Input Password  password1  ${password}

Login Password
    [Arguments]  ${password}
	Input Password  password  ${password}

Set Password Confirmation
	[Arguments]  ${password}
	Input Password  password2  ${password}