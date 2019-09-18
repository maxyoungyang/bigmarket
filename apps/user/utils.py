from apps.user.models import AgentGroup


def create_agent_group(user, name='', desc=''):
    agent_group = AgentGroup()
    agent_group.supplier = user
    agent_group.name = name
    agent_group.desc = desc
    agent_group.save()
    return agent_group
