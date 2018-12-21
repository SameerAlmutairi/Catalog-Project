# FSND Project (2) - Catalog 

By Sameer Almutairi

### Project overview
> This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates categories and their items. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

## How to Run the program
### 1. Software Installation
* Vagrant: https://www.vagrantup.com/downloads.html
* Virtual Machine: https://www.virtualbox.org/wiki/Downloads
* Download a FSND virtual machine: https://github.com/udacity/fullstack-nanodegree-vm 
* Unix-style terminal program:
  * OSX & Linux users : use installed <b>terminal</b>
  * Windows users: download Git Bash: https://git-scm.com/download/win

Once you get the above software installed, follow the following instructions :

* Extract the FSND file (downloaded inside Downloads Folder):
```console
YourMachineName:~ $ cd Downloads
YourMachineName:Downloads$ unzip -a fullstack-nanodegree-vm-master.zip
```
* Then run the following instructions to lunch vagrant:
```console
YourMachineName:Downloads$ cd fullstack-nanodegree-vm-master
YourMachineName:fullstack-nanodegree-vm-master$ cd vagrant
YourMachineName:vagrant$ vagrant up
YourMachineName:vagrant$ vagrant ssh
```
### 2. Downloading and Running The Project
   * Prerequisites
    - Python
    - HTML
    - CSS
    - Flask FrameWork use:
      `pip install flask`
    - SQLAlchemy use:
          `pip3 install SQLAlchemy`
    - oauth2client use:
          `pip3 install oauth2client`
  * Inside the vagrant create <b>“catalog-project“</b> folder:
    ```console
    vagrant@vagrant:~$ cd /vagrant
    vagrant@vagrant:/vagrant$ mkdir catalog-project
    vagrant@vagrant:/vagrant$ cd catalog-project
    vagrant@vagrant:/vagrant/catalog-project$ 
    ```
  *  Download or clone this project inside <b>“catalog-project“</b> folder using:
    ```console
    vagrant@vagrant:/vagrant/catalog-project$ git clone https://github.com/SameerAlmutairi/Catalog-Project.git
    ```
     > _need to install git in your machine to run the previous command_
 * Setup application database using this command:
    ```console
    vagrant@vagrant:/vagrant/catalog-project$ python catalog_DB.py
    ```
  *  Insert default database data using this command:
    ```console
    vagrant@vagrant:/vagrant/catalog-project$ python catalog_DB_Data.py
    ```
  *  Run the app using this command:
    ```console
    vagrant@vagrant:/vagrant/catalog-project$ python app.py
    ```
  * You can access the app locally using: [https://localhost:5000](https://localhost:5000)
  * To login using google: [https://localhost:5000/login](https://localhost:5000/login)

### 3. Using Google Login
1. go to [Google Dev Console](https://console.developers.google.com/)
2. Sign up or Login
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Item-Catalog' or any name
7. Authorized JavaScript origins = 'http://localhost:5000'
8. Authorized redirect URIs = 'http://localhost:5000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the data-clientid in header.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
12. Place JSON file in catalog directory
13. Run application
14. To login using google: [https://localhost:5000/login](https://localhost:5000/login)

### 3. JSON Endpoints
   * Catalog JSON: /catalog/JSON - Displays the whole catalog with all Categories and all items.
   * Categories JSON: /catalog/<int:catalog_id>/<int:item_id>/JSON - Displays  specific item and its photos
