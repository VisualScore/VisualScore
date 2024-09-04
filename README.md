# VisualScore

VisualScore is a free, open-source program that is re-imagining the future of music notation software. By utilizing the [neoscore](https://github.com/DigiScore/neoscore) Python library and constructing an intuitive graphical user interface around it, VisualScore is democratizing the creation of aleatoric and graphic notation for composers of all levels. It stands as one of the only software programs designed to serve avant-garde artistic practices, delivering unmatched flexibility and innovative capabilities.

## Setting up Neoscore

Step 1: Create python virtual environment with this command: "python -m venv `<virtual-environment-name>`"
-NOTE: may have to use python3 if thats what you have set up locally
Step 2: Enter virtual environment with this command: "source `<virtual-environment-name>`/bin/activate"
Step 3: Run this command to setup dependencies: "pip install -r requirements.txt"

## [Qt/Neoscore Structure Documentation](https://yielding-bucket-c99.notion.site/QT-PyQt5-Neoscore-Documentation-for-Visualscore-e6e2957dbcc24643a1bf6e7c706a9f75?pvs=4)

The above Notion site details the structure of the Neoscore code library. The goal of which is to better understand how PyQt5 and Neoscore interact with each other. Comments and highlights are made to point to where attention should be drawn for building VisualScore's interface.

## 3rd Party Libraries

- Neoscore
- PyQt

## Acknowledgements

VisualScore is made possible by the follow funding sources:

- Peabody Launch Grant
- Johns Hopkins Open Source Programs Office
- Alfred P. Sloan Foundation
