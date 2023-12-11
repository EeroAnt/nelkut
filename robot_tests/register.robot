*** Settings ***

Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page


*** Test Cases ***

As A User I Can Register An Account
	Click Link  Login
	Click Link  here
	Set Username  testuser5535
	Set Password  testpassword
	Set Password Confirmation  testpassword
	Submit Registration
	Page Should Contain  You are logged in.
