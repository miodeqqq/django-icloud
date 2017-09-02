iCloud Manager
========================

iCloud Manager is a Django based web application using **`pyiCloud`** library in order to access iPhone's data.

* **Source:**
```
https://github.com/picklepete/pyicloud
```

### Author:

* Maciej Januszewski (maciek@mjanuszewski.pl)
* Current stable version: v1.0
* Release date: 02.09.2017

# Pre-requirements:
#### **Config file (config.txt):**
* Inside `src` directory create `config.txt` file;
* Configuration file must be edited with your iCloud's credentials and Google Maps API Key;

If you don't know how to generate API key:
```
https://developers.google.com/maps/documentation/javascript/get-api-key
```

* Example:
```
icloud_user user@example.com
icloud_password mypassword
gm_api_key POaSyDKdasknNdKX7vac9NzcaM4gyF_KdXX
```

You can edit them later on application site.

### Running:

* **Build images and run project:** 
```
docker build . -t icloud && docker-compose up -d
```

### From now:

* **Application can be found at (auth=admin/admin):** 
```
http://localhost:4000
```