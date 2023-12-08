*** Settings ***

Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Register An Account, Add A Reference And Log Out


*** Test Cases ***
As A User I Can See My Saved References After Login
	Page Should Contain  to see saved references.
	Click Link  Login
	Set Username  testuser53
	Login Password  testpassword
	Click Button  Login
	Page Should Contain  testbook


*** Keywords ***
Register An Account, Add A Reference And Log Out
	Go To  ${HOME_URL}
	Home Page Should Be Open
	Click Link  Login
	Click Link  here
	Set Username  testuser53
	Set Password  testpassword
	Set Password Confirmation  testpassword
	Submit Registration
	Page Should Contain  You are logged in.
	Click Button  Add a new reference
	Click Button  Add a reference to a book
	Set Book Input  testbook  testauthor  2023  testpublisher  30  37  testid
	Click Button  Save
	Click Button  Logout

Set Book Input
	[Arguments]  ${title}  ${author}  ${year}  ${publisher}  ${start_page}  ${end_page}  ${cite_id}
	Input Text  title  ${title}
	Input Text  author   ${author}  
	Input Text  year  ${year}   
	Input Text  publisher  ${publisher}  
	Input Text  start_page  ${start_page}  
	Input Text  end_page  ${end_page}  
	Input Text  cite_id  ${cite_id}