"""
Link utils file
"""


def create_link_key(from_node: int | float, to_node: int | float):
    return f"{int(from_node)}_{int(to_node)}"
