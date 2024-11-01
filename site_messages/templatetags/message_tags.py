from django import template

from site_messages.models import Message

register = template.Library()


@register.inclusion_tag("tags/site_messages.html", takes_context=True)
def messages(context):
    messages = Message.get_messages(context.request.session)
    return {"messages": messages}
