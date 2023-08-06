.. include:: content.rst

{% if has_toc %}
{{ table_of_content_header }}
-------------------------------------------------------------------------------
.. toctree::
   :maxdepth: 1

    {% for article in article_list -%}
    {{ article.title }} <{{ article.path }}>
    {% endfor -%}
{% endif -%}