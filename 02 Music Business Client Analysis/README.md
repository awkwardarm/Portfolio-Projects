# Notes On Privacy
The .csv files for *project_hours* and *time_tracking* have been pre-processed for privacy:  
-Client and project names have been replaced with unique IDs.  
-All financial data is MinMax scaled across all columns with values ranging from from 0 to 1.

# Column Descriptions

`client_id`: unique ID for each client  
`project_id`: unique ID for each project  
`fund_date`: date deposit received to start project. Projects are funded 50% upfront and 50% on delivery.  
`start_date`: date work on project began  
`finish_date`: date of receipt of final payment for project  
`days_to_start`: days between fund_date and start_date  
`days_to_finish`: days between start_date and finish_date  
`price`: scaled price client paid for project  
`total_additional_payments`: additional payments made by client for project  
`expenses`: scaled expenses Tryba Music incurred on project  
`total_after_fees`: scaled income received after marketplace and transaction fees and expenses  
`project_hourly`: scaled hourly rate for project  
`total_hours`: total hours accumulated for project  
`status`: Active, Paused, or Done  
`project type`:  category of project  
`master_ownership`: How much of the master recording does Tryba Music own?  
`song_ownership` How much of the song does Tryba Music own?  

*boolean columns:*  

`time_tracked`: where the hours tracked for this project?  
`soundbetter`: did this project come from soundbetter.com marketplace?  
`spec_project`: was this project speculative?  
`experienced_client`: in the judgement of Tryba Music, is this client "experienced?"  
`difficult_client`: in the judgement of Tryba Music, is this client "difficult?"  
`backend_belief`: in the judgement of Tryba Music, was there belief that the project would make money from exploiting the copyright?  
`backend_money_made`: did the copyright from the project generate income for Tryba Music?  
`sync_license`: did the project incur any synchronization licenses?  
`fully_produced`: was a master recording created from the project?  
`songwriter`: did Matthew Tryba participate as a songwriter in the project that was not a work for hire?  