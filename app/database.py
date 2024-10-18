import sqlite3

# Initialize the SQLite database and create the rules table if it doesn't exist
def initialize_database():
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rules (
                 id INTEGER PRIMARY KEY,
                 rule_string TEXT,
                 ast BLOB)''')
    conn.commit()
    conn.close()

# Save a rule (rule string and its AST) into the database
def save_rule(rule_string, ast):
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()
    # Insert the rule string and serialized AST into the database
    c.execute("INSERT INTO rules (rule_string, ast) VALUES (?, ?)", (rule_string, repr(ast)))
    conn.commit()
    conn.close()

# Load all rules from the database
def load_rules():
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()
    # Fetch all rules (both rule_string and serialized AST) from the database
    c.execute("SELECT rule_string, ast FROM rules")
    rules = c.fetchall()
    conn.close()
    return rules

# Delete all rules from the database
def delete_all_rules():
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()
    # Clear the entire 'rules' table
    c.execute("DELETE FROM rules")
    conn.commit()
    conn.close()

# Call this to initialize the database when the application starts
initialize_database()
