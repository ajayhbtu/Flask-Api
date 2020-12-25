# Flask-Api
Excellence Technologies Task


Step 1: Create a Virtual environment using this command --> python -m venv env <br />
Step 2: Activate the environment --> source env/bin/activate  <br />
Step 3: Install all the dependencies using this command --> pip install -r requirements.txt  <br />
step 4: export FLASK_APP=app.py   <br />
step 5: For running the app --> flask run  <br />  <br />


Now, You can test the api's on any plateform. <br /><br />



### Raw MySQL Queries for creating database and tables:

~~~mysql
CREATE database excellenceDB;
~~~~

~~~mysql
CREATE TABLE Users ( 
             userid INT PRIMARY key auto_increment,
             username VARCHAR(100) NOT NULL UNIQUE,
             password VARCHAR(150) NOT NULL
            );
~~~~

~~~mysql
CREATE TABLE Addresses(
             addrId INT auto_increment,
             street VARCHAR(100),
             state VARCHAR(100) NOT NULL,
             country VARCHAR(100) NOT NULL,
             pincode CHAR(10) NOT NULL,
             phone VARCHAR(15) NOT NULL,
             userId INT,
             PRIMARY key (addrId, userId),
             FOREIGN key (userId) REFERENCES Users(userid) 
             ON DELETE CASCADE 
             ON UPDATE CASCADE
            );
~~~~
