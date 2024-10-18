# Rule Engine Application by Karan Jadhav

## Overview
This is a simple 3-tier rule engine application that determines user eligibility based on attributes like age, department, income, and spend. The system uses an Abstract Syntax Tree (AST) to represent conditional rules and allows for dynamic creation, combination, and modification of these rules.

## Features
- Create Rule: Allows users to create rules based on specified attributes.
- Combine Rules: Combines multiple rules into a single AST.
- Evaluate Rule: Evaluates the provided data against the rule and returns whether the user is eligible.
- Error Handling: Handles invalid rule strings and data formats, providing meaningful error messages to the user.

## Project Structure
```
project_root/
├── app/                     # Contains the main application code.
│   ├── api.py               # Provides API functions to interact with the rule engine.
│   ├── ast.py               # Defines the AST data structure.
│   ├── database.py          # Handles database initialization and operations.
│   ├── rules.py             # Implements rule creation, combination, and evaluation logic.
│   ├── static/              # Contains static files (CSS, JavaScript).
│   │   ├── css/
│   │   │   └── style.css    # CSS styles.
│   │   └── js/
│   │       └── script.js     # JavaScript files.
│   └── templates/
│       └── index.html       # Main UI template.
└── tests/                   # Contains unit tests.
    ├── test_rules.py        # Tests for rule creation, combination, and evaluation.
    └── test_api.py          # Tests for the API functions.
├── requirements.txt         # Lists the dependencies.
├── main.py                  # The entry point of the application.
└── README.md                # This documentation file.
```

## Design Choices
- 3-Tier Architecture: The application is designed with a 3-tier architecture, separating the UI, API, and backend logic for better maintainability and scalability.
- Abstract Syntax Tree (AST): Utilizes an AST to represent conditional rules, allowing for dynamic creation, combination, and modification.
- Error Handling: Implements comprehensive error handling for invalid rule strings and data formats to ensure robustness.
- UI Design: The UI is clean and user-friendly, providing dynamic feedback for rule evaluation results.

## Instructions

### Prerequisites
- Python 3.6 or higher
- Flask
- SQLite (for database)

### Build and Install

1. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database:
    ```bash
    python -c "from app.database import initialize_database; initialize_database()"
    ```

5. Run the application:
    ```bash
    python main.py
    ```
   Open your web browser and go to `http://127.0.0.1:5000/`.

## Test

### Sample Tests to Try on UI

#### Creating a Rule
Input the following rule in the "Create Rule" text box and press the Create Rule button:
```
((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
```
If successful, a prompt will indicate that the rule is being created, and the relevant AST will be generated.

#### Input a Query to Evaluate
Input the following JSON in the "Data (JSON format):" field and press the Evaluate button:
```json
{
  "age": 50,
  "department": "Sales",
  "salary": 60000,
  "experience": 10
}
```
This will generate the result as True or False.

## Predefined Test Cases
To run the tests or browse the application directly in your web browser, use the following command:
```bash
python -m unittest discover tests
```

---

### Summary of Changes Made:
1. Improved formatting with code blocks for commands and JSON for better readability.
2. Added more explicit instructions for activating the virtual environment.
3. Clarified the step-by-step process in the "Build and Install" section.
4. Used bullet points and indentation for better organization in the "Project Structure" and "Design Choices" sections.

Feel free to adjust any specific wording or formatting according to your preferences!