Manager Endpoints
- Use curl_cffi on the manager endpoint requests 

Fixtures: 
- handle fixtures that get postponed (potentially at rescheduled column in fixtures table)

DB Stuff:
- Convert player_type to int not a string containing integer

General:
- Add versioning to endpoints
- Add "inbound" data model validation for each FPL endpoint we use 