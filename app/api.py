# app/api.py
from flask import request, jsonify, render_template
from app.rules import create_rule, combine_rules, evaluate_rule, serialize_ast, deserialize_ast, RuleEngineError
from app.database import save_rule, load_rules, delete_all_rules
import os
import sys

stored_rules = []  # Global variable to keep track of all rules

def init_app(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    # API to create a new rule
    @app.route('/create_rule', methods=['POST'])
    def create_rule_api():
        rule_string = request.json.get('rule_string')
        try:
            # Create the AST from the rule string
            ast = create_rule(rule_string)
            ast_json = serialize_ast(ast)
            
            # Save the rule (string + serialized AST) to the database
            save_rule(rule_string, ast_json)
            
            # Store the serialized AST in memory
            stored_rules.append(ast_json)
            
            return jsonify({"status": "success", "ast": ast_json})
        except RuleEngineError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    # API to combine all stored rules
    @app.route('/combine_rules', methods=['POST'])
    def combine_rules_api():
        if not stored_rules:
            return jsonify({"status": "error", "message": "No rules to combine"}), 400
        
        try:
            # Deserialize all stored rules before combining
            rules = [deserialize_ast(rule) for rule in stored_rules]
            combined_ast = combine_rules(rules)
            
            # Serialize the combined AST
            combined_ast_json = serialize_ast(combined_ast)
            
            # Save the combined rule to the database
            save_rule("combined_rule", combined_ast_json)
            
            return jsonify({"status": "success", "combined_ast": combined_ast_json})
        except RuleEngineError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    # API to evaluate a rule against provided data
    @app.route('/evaluate_rule', methods=['POST'])
    def evaluate_rule_api():
        ast_json = request.json.get('ast')
        data = request.json.get('data')
        try:
            # Deserialize the provided AST
            ast = deserialize_ast(ast_json)
            
            # Evaluate the rule with the given data
            result = evaluate_rule(ast, data)
            
            return jsonify({"status": "success", "result": result})
        except RuleEngineError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    # API to reset (clear) all rules, both in-memory and in the database
    @app.route('/reset_rules', methods=['POST'])
    def reset_rules():
        global stored_rules
        stored_rules = []  # Clear the in-memory stored rules
        delete_all_rules()  # Clear all rules in the database
        return jsonify({'status': 'success', 'message': 'All rules have been reset.'}), 200
