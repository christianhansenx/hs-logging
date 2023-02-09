# **hs-logging - developer guide**
The project is developed in Windows WSL: Ubuntu-20.04</br>
(WSL = Windows Subsystem for Linux)

### **Development environment**
#### Create virtual Python environment
```bash
./create_venv.sh
```
#### Activate the virtual Python environment
```bash
. activate_venv.sh
```
#### Deactivate the virtual Python environment
```bash
deactivate
```
#### Install development dependencies (pip installs)
##### List of installed packages is created as workspace/testing/pip_list_dev_*timestamp*.txt
```bash
./development_dependencies.sh
```
### **Testing**
#### Cleaning Python caches
##### This should only be necessary to execute prior to tests in case of huge changes in code or file structure
```bash
./cache_clean.sh
```
#### Code check (linting)
##### A test report is created as workspace/testing/linting_*timestamp*.html
```bash
./linting.sh
```
#### Module Testing
##### A test report is created as workspace/testing/modules_test_*timestamp*.html
```bash
./module_testing.sh
```
### **PyPi packaging**
https://www.youtube.com/watch?v=tEFkHEKypLI  
https://www.codementor.io/@arpitbhayani/host-your-python-package-using-github-on-pypi-du107t7ku  
https://www.youtube.com/watch?v=5KEObONUkik  
https://stackoverflow.com/questions/61156290/how-to-set-project-links-in-pypi  


***Note:** Before building package, update VERSION in **setup.py***</br>

Build package
```
./pypi_build.sh
```

***Note:** Before uploading to PyPi, delete old builds from **dist** folder.*</br>

Upload to PyPi
```
twine upload dist/* --verbose
```

</br>

## **Code Documentation**

### **Code comment tags**
Some code comments begins with a tag to categorize the purpose of the comment:</br>
**\<code\>** code not in use but could in the future be relevant</br>
**\<link\>** link to code examples, documentation, discussion forums etc.</br>
