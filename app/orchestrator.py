from app.agents.analytics_agent import analytics_agent
from app.agents.seo_agent import seo_agent


def handle_query(req):
    """
    Central orchestrator that routes the query to the correct agent.
    """
    if req.propertyId:
        return analytics_agent(req.query, req.propertyId)

    return seo_agent(req.query)
