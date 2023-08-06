{% macro h1(contents, size = "26px", weight = "normal", color = "#2d2d2d") -%}
    <h1 style="margin-top:38px;margin-bottom:26px;font-size:{{ size }};font-weight:{{ weight }};color:{{ color }};">{{ contents }}</h1>
{%- endmacro %}

{% macro h2(contents, size = "22px", weight = "normal", color = "#2d2d2d") -%}
    <h2 style="margin-top:30px;margin-bottom:14px;font-size:{{ size }};font-weight:{{ weight }};color:{{ color }};">{{ contents }}</h2>
{%- endmacro %}

{% macro h3(contents, size = "18px", weight = "normal", color = "#2d2d2d") -%}
    <h3 style="margin-top:26px;margin-bottom:12px;font-size:{{ size }};font-weight:{{ weight }};color:{{ color }};">{{ contents }}</h3>
{%- endmacro %}

{% macro link(href, contents, base = True, simple = False) -%}
    {% if base %}{% set href = base_url|default('', True) + href %}{% endif %}
    {% if simple %}
        <a href="{{ href }}">{{ contents }}</a>
    {% else %}
        <a href="{{ href }}" style="color:#1b75bb;text-decoration:none;padding-bottom:1px;">{{ contents }}</a>
    {% endif %}
{%- endmacro %}
{% block html %}{% endblock %}
