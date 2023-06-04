# simple-logging-server

## Context 

This is a simple logger server implementation using Flask.

## Structure
Here, I've used Postgres as relational DB

DB structure used:

```
TABLE logs
  - id 
  - user_id
  - unix_ts
  - event_name
```

## How to use this repository
- Clone the repository from github.
- move to repository folder
- start the docker-compose
  ```bash
  $ docker-compose up
  ```
  ### Prerequisites:
   - Docker
   - Docker compose

## APIs 

1. ### Create Account
   ```
   Method: POST
   Path: "/log"
   Desciption: Add an event log to the database
   ```


   - Request Payload:
   ```python
    {
        "id": int,
        "unix_ts": int,
        "user_id": int,
        "event_name": str,
    }
   ```


   - Response Data:
   ```python
   {
     "Accepted"
   }
   ```

## Testing the API 
- On a saparate shell, run 
  ```bash
  $ docker-compose up test-logging
  ```

## Scope of Improvements
- Using a task scheduler to handle data movement from buffer to database
- Adding streams to prevent data loss
- Using ORMs to handle the database updates
