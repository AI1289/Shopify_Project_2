import ast

allowed_funcs = {"ROUND": round, "MAX": max, "MIN": min}
allowed_nodes = {
    ast.Expression, ast.BinOp, ast.Num, ast.Constant, ast.Name,
    ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd,
    ast.Call
}

def safe_eval(expr, variables=None):
    if variables is None:
        variables = {}
    node = ast.parse(expr, mode='eval')
    for n in ast.walk(node):
        if type(n) not in allowed_nodes:
            raise ValueError(f"Disallowed expression element: {ast.dump(n)}")
        if isinstance(n, ast.Call):
            if not isinstance(n.func, ast.Name) or n.func.id not in allowed_funcs:
                raise ValueError(f"Disallowed function call: {getattr(n.func, 'id', repr(n.func))}")
    safe_globals = {"__builtins__": None, **allowed_funcs}
    safe_globals.update({k: v for k, v in variables.items() if isinstance(v, (int, float))})
    return eval(compile(node, "<ast>", "eval"), safe_globals, {})


import pandas as pd

def apply_formula(df, column_name, expression):
    results = []
    for idx, row in df.iterrows():
        try:
            result = safe_eval(expression, variables=row.to_dict())
            results.append(result)
        except Exception as e:
            results.append(None)
    df[column_name] = results
    return df
