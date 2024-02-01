# Code Folder

> Folder structure options and naming conventions for *Code* folder of **Human Body Heat Transfer**

### Directory layout:

    .
    ├── body_parts               # Body parts models files
    │    ├── cylinder_model.py   # Base Class (contains correlation common to every part)
    │    └── subclasses          # Subclasses representing a specific body part
    │        ├── ...
    │        ├── head.py         #   (1 python file for each class, 
    │        ├── arm.py          #    filename should clearly identify the body part) 
    │        └── ... 
    │
    ├── overall_model            # Overall Body model files (code connecting the body parts)
    └── test                     # Unittest files

### Naming Conventions:

| Type                             | Naming Convention                                                                                                                                                                              | Examples                                                                 |
|:---------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------|
| **Folder**                       | **lowercase letter** separate words with **underscores**                                                                                                                                       | .../**body_parts**                                                       |
| **File**                         | Same as folder, if contains only one class should have **the same name of the class**                                                                                                          | .../**body_model.py**                                                    |
| **Py Class**                     | Use the python convention: <br/><pre>1. **Start** each word with a **capital letter**.<br/>2. **Do not** separate words with underscores.</pre>                                                | Class **BodyModel**:                                                     |
| **Py Class Method / Properties** | Use the python convention: <br/><pre>1. Use **lower case letter** only.<br/>2. Separate words with **underscores**.<br/>3. For private methods/properties start with a double underscore</pre> | **cylinder_leght**=10<br/>**__cylinder_leght**=10<br/>def **try_this**() |
