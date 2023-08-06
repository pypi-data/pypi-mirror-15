{{ package.name }}
{{ "=" * package.name|length }}

.. automodule:: {{ package.fullname }}
    :members:

sub packages and modules
------------------------

.. toctree::
   :maxdepth: 1

    {% for pkg in package.sub_packages.values() -%}
    {% if not isignored(pkg) -%}
    {{ pkg.name }} <{{ pkg.name }}/__init__>
    {% endif -%}
    {% endfor -%}
    {% for mod in package.sub_modules.values() -%}
    {% if not isignored(mod) -%}
    {{ mod.name }} <{{ mod.name }}>
    {% endif -%}
    {% endfor -%}