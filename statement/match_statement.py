import re
import xml.etree.ElementTree as XMLTree

from statement.abstract_branch_statement import AbstractBranchStatement
from statement.abstract_statement import AbstractStatement


class MatchStatement(AbstractBranchStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)

    def allows_template(self):
        return True

    def execute(self):
        from pathlib import Path
        match_node = self.current_node()
        expr_key, expr_value = next(iter(match_node.attrib.items()))
        match expr_key:
            case "expr":
                self.logger.warning("DEPRECATED: In <match> statement, you should replace 'expr' attribute by 'value'.")
                expr_attr = self.format_str(expr_value)
            case "value":
                expr_attr = self.format_str(expr_value)
            case "eval":
                expr_attr = eval(self.format_str(expr_value))
            case _:
                raise RuntimeError(f"Bad expression attribute: '{expr_key}'")
        assert match_node.text is None or len(match_node.text.strip()) == 0
        found_case_node = None
        default_case_node = None
        if len(match_node) == 0:
            raise RuntimeError("case nodes are missing in match node.")
        for case_node in match_node:
            if case_node.tag != "case":
                raise RuntimeError(f"In 'match', bad child node type: {case_node.tag}.")
            case_value = case_node.attrib.get('value', None)
            if case_value is not None:
                formatted_case_value = self.format_str(case_value)
                if expr_attr == formatted_case_value:
                    found_case_node = case_node
                    break
                continue
            case_eval = case_node.attrib.get('eval', None)
            if case_eval is not None:
                eval_formatted_case_value = eval(self.format_str(case_eval))
                if expr_attr == eval_formatted_case_value:
                    found_case_node = case_node
                    break
                continue
            case_regex = case_node.attrib.get('regex')
            if case_regex is None:
                case_regex = case_node.attrib.get('expr', None)
                if case_regex is not None:
                    self.logger.warning("DEPRECATED: "
                                        "In <case> statement, you should replace 'expr' attribute by 'regex'.")
            if case_regex is not None:
                if re.fullmatch(self.format_str(case_regex), expr_attr):
                    found_case_node = case_node
                    break
                continue
            if default_case_node is not None:
                raise RuntimeError("A match node cannot have two default case nodes.")
            default_case_node = case_node
        if found_case_node is not None:
            self.current_main_statement().treat_children_nodes_of(found_case_node)
        elif default_case_node is not None:
            self.current_main_statement().treat_children_nodes_of(default_case_node)

    def check_not_template_attributes(self, nb_template_attributes: int):
        if "value" in self.current_node().attrib:
            raise RuntimeError(f"The attribute 'value' is unexpected when calling a 'match' template.")
        if "expr" in self.current_node().attrib:
            raise RuntimeError(f"The attribute 'expr' is unexpected when calling a 'match' template.")
        if "eval" in self.current_node().attrib:
            raise RuntimeError(f"The attribute 'eval' is unexpected when calling a 'match' template.")

    def post_template_run(self, template_statement):
        if len(self.current_node()) > 0:
            raise RuntimeError("No child statement is expected when calling a 'match' template.")
