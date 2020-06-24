import random
from uuid import uuid1


def generate_uuid():
    """Generates a uniuqe uuid by masking the node identity
    """
    return uuid1(node=random.randint(0, 2**31 - 1))
