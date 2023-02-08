# **hs-logging**

 **developer guide**

</br>

## **Continuous Integration**
The project is developed in Windows WSL: Ubuntu-20.04</br>
(WSL = Windows Subsystem for Linux)

### **Tools for development**
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

</br>


# **PyPi**
https://www.youtube.com/watch?v=tEFkHEKypLI  

Build package
```
python3 setup.py sdist bdist_wheel
```
Install twine
```
pip3 install twine
```
Upload to PyPi
```
twine upload dist/*
```

</br>
</br>

## **Code Documentation**

### **Code comment tags**
Some code comments begins with a tag to categorize the purpose of the comment:
- **\<code\>** code not in use but could in the future be relevant
- **\<link\>** link to code examples, documentation, discussion forums etc.
