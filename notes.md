Manager Endpoint
- Improve Logging 

Fixtures: 
- handle fixtures that get postponed (potentially at rescheduled column in fixtures table)

DB Stuff:
- Convert player_type to int not a string containing integer

General:
- Add versioning to endpoints
- Evaluate whether its better to have class Config: from_attributes = True in all schemas and use model_validate in services or if its better to do a dump to a dict and pass to the schema directly

League Endpoints:  
- Add pagination to the league endpoint for long standings 
- Make the H2H league output in {manager_id}/leagues endpoint actually do something 
- View all managers in a league - captain, in play, to start, GW net, month total, total points 