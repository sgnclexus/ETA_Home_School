# ETA Home to School PROJECT

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installing and Executions](#installing-and-executions)
- [Usage](#usage)

## About <a name = "about"></a>

This project was created to analyze elapsed time arrival from students' home to the school. Using the Google API Directions we determine the average elapsed time of arrival in the students journey home-school.

## Getting Started<a name = "starte"></a>

The technologies we are using are:
- API Google Direction
- Python
    

## Prerequisites <a name = "rerequisites"></a>

To run this project we have used direction api of google maps. In this case you will need to have a google account and at least one project in gcp because you are going to need a api key to execute the api. 

### Inputs (Data)

The program needs the followings files to run:
- Metro_2024_global.csv # Assignment File 
- OpcEdu.csv    # Schools
- CPdescarga.csv    # SEPOMEX info (zip codes info)
- ETA_Schools_Final_LatitudeLongitude.csv # (Final document where we captured final latitude longitude of schools)

### Outputs

The program generates some csv work files you can ommit if you want and the final file and ms excel file .

The files that the program will generate are:

- ScholsRequiredCols.csv  # Schools with required columns created
- ScholsRemovingAfter_CP.csv # Schools with required columns and removing unnecesary data created
- UniqueSchools.csv # Schools Group By function to get unique schools created
- FinalOpcEdu.csv # Schools merged with final latitude longitude file created
- Assigned_Filtered.csv # Assigned Students File created
- AssignedSEPOMEX.csv # Merged info between SEPOMEX and Assigned Students file created
- AllInfoforETA.csv # All info in one file created
- FinalFileToETA.csv # Final file to request api direction created

Last but not the least the program generates a final file in XLSX format, it depends the option you choose:

For assigned students 
- OA_Trayecto_Casa_Escuela.xlsx

For first option selected
- PO_Trayecto_Casa_Escuela.xlsx



## Installing and Executions <a name = "iexecution"></a>

Create virtual environment
```
# Create virtual environment
C:\Users\<user>\AppData\Local\Programs\Python\Python311\python -m venv .\venv
# To activate virtual environment
.\venv\Scripts\activate
```

For Mac
```
python3 -m venv venv
source venv/bin/activate
```


Install requirements 
```
pip install -r .\requirements.txt
```

Google API Direction

We are using this api, more information about in the following link:

https://developers.google.com/maps/documentation/directions/start


Note: Its necessary to put the key in the next line in class latitude_longitude.py
```
# API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
```

A step by step series of examples that tell you how to get a development env running.

Once the virtual environment and the libraries are installed we only need to execute the main program "eta_home_school.py", in this case this program need at least 1 parameter.
The first parameter tell the program the mode execution. The only to modes are:
- -oa When we want to find only assigned 
- -po When it doesn't matter if the student was assigned because it referes to the first option the student selected

```
python .\src\eta_home_school.py -po 
```

You optionally can add a second argument to choose the sample size based on the number of right answers in the exam.

```
python .\src\eta_home_school.py -po 80
```

Project Structure
```
📦ETA_COMIPEMS
 ┣ 📂data
 ┃ ┣ 📜CPdescarga.csv
 ┃ ┣ 📜eta_home_school.txt
 ┃ ┣ 📜ETA_Schools_Final_LatitudeLongitude.csv
 ┃ ┣ 📜Metro_2024_global.csv
 ┃ ┗ 📜OpcEdu.csv
 ┣ 📂src
 ┃ ┣ 📂utils
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┗ 📜Latitude_Longitude.cpython-311.pyc
 ┃ ┃ ┣ 📜Latitude_Longitude.py
 ┃ ┃ ┣ 📜string_formatter.py
 ┃ ┃ ┗ 📜time_format.py
 ┃ ┗ 📜eta_home_school.py
 ┣ 📜AssignedSEPOMEX.csv
 ┣ 📜Assigned_Filtered.csv
 ┣ 📜FinalFile.csv
 ┣ 📜FinalOpcEdu.csv
 ┣ 📜GetETA.csv
 ┣ 📜README.md
 ┣ 📜ScholsRemovingAfter_CP.csv
 ┣ 📜ScholsRequiredCols.csv
 ┣ 📜UniqueSchools.csv
 ┣ 📜UniqueSchoolsAddress.csv
 ┣ 📜Unique_ETAs.csv
 ┗ 📜viendosiquito.csv
```


## Usage <a name = "usage"></a>

Only for educational purpose.
