*** Settings ***

Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page


*** Test Cases ***

User Can Add Article Reference
    Click Link  Login
    Click Link  here
    Set Username  testiartikkeli6575123456
    Set Password  testi123
    Set Password Confirmation  testi123
    Submit Registration
    Click Button  Add a new reference
    Click Button  Add a reference to an article
    Set Article Input  Experimental evaluation in computer science: A quantitative study  Tichy, W. F., Lukowicz, P., Prechelt, L., & Heinz, E. A.  1995  Journal of Systems and Software  28  9  18  ARTICLE_TEST
    Click Button  Save
    Page Should Contain  Experimental evaluation
    Click Button  Logout

User Can Add Book Reference
    Click Link  Login
    Click Link  here
    Set Username  testikirja5685123456
    Set Password  testi123
    Set Password Confirmation  testi123
    Submit Registration
    Click Button  Add a new reference
    Click Button  Add a reference to a book
    Set Book Input  Computer Science an overview  Brookshear, J. G.  1996  Addison-Wesley Longman Publishing Co., Inc.  123  126  BOOK_TEST
    Click Button  Save
    Page Should Contain  Brookshear
    Click Button  Logout

User Can Add Inproceeding Reference
    Click Link  Login
    Click Link  here
    Set Username  testiinproceeding5695123456
    Set Password  testi123
    Set Password Confirmation  testi123
    Submit Registration
    Click Button  Add a new reference
    Click Button  Add a reference to an inproceeding
    Set Inproceeding Input  Designing an assessment for introductory programming concepts in middle school computer science	 Grover, S  2020  Proceedings of the 51st ACM Technical Symposium on Computer Science Education  678  684  INPROCEEDING_TEST
    Click Button  Save
    Page Should Contain  Grover

# Click Link Download Bibtex
#     Click Button  Download a BibTex file
#     Home Page Should Be Open    
    

*** Keywords ***
Set Article Input
    [Arguments]  ${title}  ${author}  ${year}  ${journal}  ${volume}  ${start_page}  ${end_page}  ${cite_id}
    Input Text  title  ${title}
    Input Text  author   ${author}  
    Input Text  year  ${year}  
    Input Text  journal  ${journal}  
    Input Text  volume  ${volume}  
    Input Text  start_page  ${start_page}  
    Input Text  end_page  ${end_page}  
    Input Text  cite_id  ${cite_id}
    
Set Book Input
    [Arguments]  ${title}  ${author}  ${year}  ${publisher}  ${start_page}  ${end_page}  ${cite_id}
    Input Text  title  ${title}
    Input Text  author   ${author}  
    Input Text  year  ${year}   
    Input Text  publisher  ${publisher}  
    Input Text  start_page  ${start_page}  
    Input Text  end_page  ${end_page}  
    Input Text  cite_id  ${cite_id}

Set Inproceeding Input
    [Arguments]  ${title}  ${author}  ${year}  ${booktitle}  ${start_page}  ${end_page}  ${cite_id}
    Input Text  title  ${title}
    Input Text  author   ${author}  
    Input Text  year  ${year}  
    Input Text  booktitle  ${booktitle}  
    Input Text  start_page  ${start_page}  
    Input Text  end_page  ${end_page}  
    Input Text  cite_id  ${cite_id}