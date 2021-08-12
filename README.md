# Fusion 360 Package Manager Temaplate

This is a Fusion 360 add-in template that allows the use of third-party python packages.

## Installation

### Requirements
- Fusion 360
- (optional) Python (for manual package installation)

### Install Add-In
1. Download this add-in.
2. Open Fusion 360 and go to `TOOLS > ADD-INS > Add-Ins`. 
3. Click `+` button and select the folder `PackageManagerTemplate/` to install add-in.
4. Select the `PackageManagerTemplate` add-in and click `Run`.

## Usage
### Automatic Installation
List the required packages in the `requirement.txt` file. When the add-in is enabled, `PackageManagerTemplate.py` shell try to import the packages in the `try` statment. If it fails to import, it will try to install the packages in the `requirements.txt` line by line.

### Manual Manipulation
Find the path to Fusion 360 python executable, which could be found in the `mylogger.log`.
Edit `python_path` and `commands` in the last section of `package_manager.py`.

### Log
Any log can be found in `mylogger.log`.