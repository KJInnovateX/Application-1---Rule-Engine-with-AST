from app.ast import Node
import re

class RuleEngineError(Exception):
    pass

# Helper function to parse a condition like "age >= 30" or "department = 'Sales'"
def parse_condition(condition):
    # Strip parentheses and extra spaces around the condition
    condition = condition.strip().lstrip('(').rstrip(')')

    # Update regex to capture >=, <=, >, <, = and support strings like 'Sales'
    pattern = r"(\w+)\s*(>=|<=|>|<|=)\s*('?\w+'?)"
    match = re.match(pattern, condition.strip())
    if match:
        attribute, operator, value = match.groups()

        # Remove surrounding quotes if value is a string with quotes
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]

        # Try to convert value to an int if it looks like a number
        try:
            value = int(value)
        except ValueError:
            pass

        return Node("operand", value=(attribute, operator, value))
    else:
        raise RuleEngineError(f"Invalid condition format: {condition}")

def create_rule(rule_string):
    # Remove any surrounding parentheses and extra spaces
    rule_string = rule_string.strip()
    if not rule_string:
        raise RuleEngineError("Empty rule string")

    # Define operator precedence (OR has lower precedence than AND)
    operator_precedence = {"AND": 2, "OR": 1}

    def get_operator_precedence(op):
        return operator_precedence.get(op, 0)

    # Split the rule string into tokens of conditions and operators (AND/OR)
    tokens = re.split(r'\s+(AND|OR)\s+', rule_string)

    # Stack to store the nodes and operators
    node_stack = []
    operator_stack = []

    def apply_operator():
        right = node_stack.pop()
        left = node_stack.pop()
        operator = operator_stack.pop()
        node_stack.append(Node("operator", left=left, right=right, value=operator))

    # Process tokens
    for token in tokens:
        token = token.strip()

        if token in ("AND", "OR"):
            # If there's an operator, check operator precedence
            while operator_stack and get_operator_precedence(operator_stack[-1]) >= get_operator_precedence(token):
                apply_operator()
            operator_stack.append(token)
        else:
            # This should be a condition, parse it
            node_stack.append(parse_condition(token))

    # Apply remaining operators
    while operator_stack:
        apply_operator()

    # Return the root of the AST
    return node_stack[0]

def combine_rules(rules):
    if not rules:
        return None

    combined_ast = rules[0]
    for rule in rules[1:]:
        combined_ast = Node("operator", left=combined_ast, right=rule, value="AND")

    return combined_ast

def evaluate_node(node, data):
    if node.node_type == "operand":
        attribute, operator, value = node.value
        if operator == ">":
            return data.get(attribute, None) > value
        elif operator == "<":
            return data.get(attribute, None) < value
        elif operator == "=":
            return data.get(attribute, None) == value
        elif operator == ">=":
            return data.get(attribute, None) >= value
        elif operator == "<=":
            return data.get(attribute, None) <= value
    elif node.node_type == "operator":
        if node.value == "AND":
            return evaluate_node(node.left, data) and evaluate_node(node.right, data)
        elif node.value == "OR":
            return evaluate_node(node.left, data) or evaluate_node(node.right, data)
    return False

def evaluate_rule(ast, data):
    if not isinstance(data, dict):
        raise RuleEngineError("Invalid data format.")
    return evaluate_node(ast, data)

def serialize_ast(node):
    if node is None:
        return None
    return {
        'node_type': node.node_type,
        'value': node.value,
        'left': serialize_ast(node.left),
        'right': serialize_ast(node.right)
    }

def deserialize_ast(node_dict):
    if node_dict is None:
        return None
    return Node(
        node_type=node_dict['node_type'],
        value=node_dict.get('value'),
        left=deserialize_ast(node_dict.get('left')),
        right=deserialize_ast(node_dict.get('right'))
    )
