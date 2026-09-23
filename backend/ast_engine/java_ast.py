import re
from typing import Dict, Any, List, Optional
import javalang
from database.models import ASTNode, CodeIntelligenceResponse

def build_java_ast_tree(tree) -> Optional[ASTNode]:
    """Builds visual AST hierarchy from javalang parse tree."""
    if not tree:
        return None

    root_children = []

    # Imports
    for imp in getattr(tree, 'imports', []) or []:
        root_children.append(ASTNode(
            name=f"import {imp.path}",
            node_type="Import",
            line=getattr(imp.position, 'line', None) if hasattr(imp, 'position') and imp.position else None,
            children=[]
        ))

    # Types / Classes
    for type_decl in getattr(tree, 'types', []) or []:
        if isinstance(type_decl, javalang.tree.ClassDeclaration):
            class_children = []

            # Methods and fields
            for member in getattr(type_decl, 'body', []) or []:
                if isinstance(member, (javalang.tree.MethodDeclaration, javalang.tree.ConstructorDeclaration)):
                    m_line = member.position.line if hasattr(member, 'position') and member.position else None
                    method_children = []

                    # Scan method body for statements
                    if hasattr(member, 'body') and member.body:
                        for stmt in member.body:
                            if isinstance(stmt, (javalang.tree.ForStatement, javalang.tree.WhileStatement, javalang.tree.DoStatement)):
                                method_children.append(ASTNode(name="Loop", node_type="Loop", line=getattr(stmt.position, 'line', None) if stmt.position else None, children=[]))
                            elif isinstance(stmt, (javalang.tree.IfStatement, javalang.tree.SwitchStatement)):
                                method_children.append(ASTNode(name="If Condition", node_type="Condition", line=getattr(stmt.position, 'line', None) if stmt.position else None, children=[]))
                            elif isinstance(stmt, javalang.tree.LocalVariableDeclaration):
                                v_names = [v.name for v in stmt.declarators]
                                method_children.append(ASTNode(name=f"var {', '.join(v_names)}", node_type="Variable", line=getattr(stmt.position, 'line', None) if stmt.position else None, children=[]))
                            elif isinstance(stmt, javalang.tree.StatementExpression):
                                method_children.append(ASTNode(name="Method Call / Expr", node_type="MethodCall", line=getattr(stmt.position, 'line', None) if stmt.position else None, children=[]))

                    class_children.append(ASTNode(
                        name=f"{member.name}()",
                        node_type="Method",
                        line=m_line,
                        children=method_children
                    ))

                elif isinstance(member, javalang.tree.FieldDeclaration):
                    f_line = member.position.line if hasattr(member, 'position') and member.position else None
                    v_names = [v.name for v in member.declarators]
                    class_children.append(ASTNode(
                        name=f"field {', '.join(v_names)}",
                        node_type="Variable",
                        line=f_line,
                        children=[]
                    ))

            c_line = type_decl.position.line if hasattr(type_decl, 'position') and type_decl.position else None
            root_children.append(ASTNode(
                name=f"Class {type_decl.name}",
                node_type="Class",
                line=c_line,
                children=class_children
            ))

    return ASTNode(name="CompilationUnit (Root)", node_type="Root", line=1, children=root_children)

def fallback_java_regex_analysis(code: str) -> dict:
    """Fallback structural analysis if syntax errors prevent complete javalang parsing."""
    classes = len(re.findall(r'\bclass\s+[A-Za-z0-9_]+', code))
    methods = len(re.findall(r'\b(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+([A-Za-z0-9_]+)\s*\([^)]*\)\s*\{', code))
    vars_found = len(re.findall(r'\b(?:int|double|float|long|boolean|char|String|[A-Z][A-Za-z0-9_]*)\s+[a-zA-Z0-9_]+(?:\s*=|\s*;)', code))
    loops = len(re.findall(r'\b(for|while)\s*\(', code))
    conditions = len(re.findall(r'\b(if|switch)\s*\(', code))
    imports = len(re.findall(r'\bimport\s+[\w.]+;', code))

    return {
        "classes": max(classes, 1),
        "methods": max(methods, 1),
        "variables": vars_found,
        "loops": loops,
        "conditions": conditions,
        "imports": imports
    }

def analyze_java_ast_intelligence(code: str, error_count: int, warning_count: int) -> CodeIntelligenceResponse:
    """
    Analyzes Java AST structure using javalang, calculates genuine metrics and health score.
    """
    classes_cnt = 0
    methods_cnt = 0
    vars_cnt = 0
    loops_cnt = 0
    conditions_cnt = 0
    imports_cnt = 0
    ast_tree = None

    try:
        tree = javalang.parse.parse(code)
        ast_tree = build_java_ast_tree(tree)

        for _, node in tree:
            if isinstance(node, javalang.tree.ClassDeclaration):
                classes_cnt += 1
            elif isinstance(node, (javalang.tree.MethodDeclaration, javalang.tree.ConstructorDeclaration)):
                methods_cnt += 1
            elif isinstance(node, (javalang.tree.LocalVariableDeclaration, javalang.tree.FieldDeclaration)):
                vars_cnt += len(node.declarators)
            elif isinstance(node, (javalang.tree.ForStatement, javalang.tree.WhileStatement, javalang.tree.DoStatement)):
                loops_cnt += 1
            elif isinstance(node, (javalang.tree.IfStatement, javalang.tree.SwitchStatement)):
                conditions_cnt += 1
            elif isinstance(node, javalang.tree.Import):
                imports_cnt += 1

    except Exception:
        # If code has syntax errors that javalang rejects, use deterministic token scan
        fallback = fallback_java_regex_analysis(code)
        classes_cnt = fallback["classes"]
        methods_cnt = fallback["methods"]
        vars_cnt = fallback["variables"]
        loops_cnt = fallback["loops"]
        conditions_cnt = fallback["conditions"]
        imports_cnt = fallback["imports"]

    score = 100 - (error_count * 35) - (warning_count * 10)
    if conditions_cnt > 6:
        score -= (conditions_cnt - 6) * 2
    health_score = max(0, min(100, score))

    return CodeIntelligenceResponse(
        classes=classes_cnt,
        methods=methods_cnt,
        variables=vars_cnt,
        loops=loops_cnt,
        conditions=conditions_cnt,
        imports=imports_cnt,
        health_score=health_score,
        ast_tree=ast_tree,
        breakdown={
            "errors": error_count,
            "warnings": warning_count,
            "complexity_branches": conditions_cnt + loops_cnt
        }
    )
