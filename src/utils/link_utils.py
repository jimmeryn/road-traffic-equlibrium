"""
Link utils file
"""
from src.shared.link import Link


def get_link_travel_time(link: Link, flow: int):
    return link.free_flow_time * \
        (1 + link.b * pow((flow / link.capacity), link.power))
