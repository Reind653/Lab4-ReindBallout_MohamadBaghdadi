
# Lab4-ReindBallout_MohamadBaghdadi

### A School Management System using Tkinter and PyQt

This project is a Python-based school management system that utilizes both Tkinter and PyQt frameworks for the user interface (UI). The system allows users to manage students, instructors, courses, and registrations efficiently. It is designed to demonstrate the integration of two different GUI frameworks and showcase how they can be utilized in a single project.

---

## Features

### Tkinter Implementation:
- **Student Management:** Add and manage student information (name, ID, and details).
- **Instructor Management:** Add and manage instructor information (name, ID, and details).
- **Course Management:** Add and manage course information (course title, instructor, etc.).
- **Registration:** Register students for courses using dropdowns for selection.
- **View Data:** View the added students, instructors, and courses, and refresh the list dynamically.
- **Edit & Delete:** Double-click to edit or delete any record in the list.

### PyQt Implementation:
- **Main Window:** A PyQt5-based interface to interact with the school management system.
- **OOP Module Integration:** Utilizes `OOP.py` for organizing the underlying functionality and business logic of the system.
- **Cross-Module Communication:** Smooth interaction between PyQt's GUI components and backend logic through `pyqt_PART3.py` and `OOP.py`.

---

## Folder Structure

- **`pyqt_PART3.py`**: PyQt-based implementation for the School Management System UI.
- **`OOP.py`**: Contains the object-oriented programming logic for managing students, instructors, courses, and registrations.
- **`tkinter_app.py`**: Tkinter-based implementation for the School Management System.
- **`docs/`**: Contains Sphinx-generated HTML documentation and source files.
  - `docs/build/html/`: HTML output for documentation.
  - `docs/source/`: Source `.rst` files for the documentation.
  
---

## Setup and Run

### Prerequisites:
- Python 3.x
- Tkinter (usually included with Python)
- PyQt5:
  ```bash
  pip install PyQt5
  ```

### Running the Tkinter Application:
```bash
python3 tkinter_app.py
```

### Running the PyQt Application:
```bash
python3 pyqt_PART3.py
```

---

## Documentation

The project documentation is generated using Sphinx. You can view the HTML documentation located under `docs/build/html/`. To generate the documentation from source:

1. Navigate to the `docs` directory:
   ```bash
   cd docs
   ```

2. Run the following command to build the HTML documentation:
   ```bash
   make html
   ```

The output will be available under `docs/build/html/`.

---

## Contributing

Feel free to fork this repository, make your changes, and submit a pull request. Collaboration and contributions are welcome!

---

## License

This project is licensed under the MIT License.
