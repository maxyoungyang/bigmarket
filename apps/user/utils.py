from apps.user.models import AgentGroup


def create_agent_group(supplier, name='', desc=''):
    agent_group = AgentGroup()
    agent_group.supplier = supplier
    agent_group.name = name
    agent_group.desc = desc
    agent_group.save()
    return agent_group
