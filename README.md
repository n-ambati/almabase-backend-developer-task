# Almabase Backend Developer Task - Find Duplicate Profiles

## Assumptions
* Data will be provided to the program in JSON format.
* The output from the program is in JSON format.
* The input to the program (i.e. profiles and the fields to compare) will be provided in the `data.json`.
* The output of the program (i.e. profiles that are being compared, total matching score, matching attributes, non matching attributes and ignored attributes) will be saved as `result.json`.

## Folder Structure
- **utils.py** contains functions to interact with the json files.
- **duplicate_finder.py** contains the actual logic to calculate similarity score between two profiles.
- **main.py** is a wrapper module that streamlines the process flow.
- **data.json** acts as the input data.
- **result.json** acts as the output data from the script.

## Steps to execute
* Download or clone the repository.
* Make sure python3.7 or greater is installed.
* Create a virtual environment.
```$ python -m venv venv```
Note: Use `python3` if `python` points to python2
* Activate the virtual environment.
```
#On MacOSX / Linux
$ source venv/bin/activate

#On Windows
$ venv\Scripts\activate
```
* Install the requirements.
```pip install -r requirements.txt```
* Execute `main.py`.
