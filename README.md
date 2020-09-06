# madoda-manager v3
Download Youtube Video, Convert To Mp3, Remove Tags, Upload to google drive

## how to use
install all requirements
> pip3 install -r requirements.txt

### setup the app
#### copy google drive credentials to 
    ./assets/google_drive/client_ids if is client ids and 
    ./assets/google_drive/service_accounts if service accounts 
(you can use both but client_id has priority) 

#### copy youtube credentials to
    ./assets/youtube/credentials 
(only client_id is acceptable)

> python3 setup.py

#### copy api_key to the host app

### run the app
> python3 main.py