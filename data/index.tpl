{% extends '_theme/base.tpl' %}
{% block body %}
<ul>
{% for url, child in meta.children.items() %}
    <li><a href="{{ url }}">{{ child.title or url }}</a></li>
{% endfor %}
</ul>
{% endblock%}
