
import os
import stat

path = r"c:\Users\AYUSH\Downloads\admin\Greeva\greeva\templates\base.html"

content = """{% load static i18n %}
<!DOCTYPE html>
{% get_current_language as LANGUAGE_CODE %}
<html lang="{{ LANGUAGE_CODE }}" data-bs-theme="{{ request.user.theme_preference|default:'light' }}" {% block html_attribute %}{% endblock html_attribute %}>

<head>
  <meta charset="utf-8" />
  <title>{% block title %}{% endblock title %} | Greeva - Responsive Bootstrap 5 Admin Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta content="A fully featured admin theme which can be used to build CRM, CMS, etc." name="description" />
  <meta content="Coderthemes" name="author" />

  <!-- App favicon -->
  <link rel="icon" href="{% static 'images/favicon.ico' %}" />

  {% block css %}

  {% block extra_css %}{% endblock extra_css %}

  <script src="{% static 'js/config.js' %}"></script>

  <link href="{% static 'css/app.min.css' %}" rel="stylesheet" />
  <link href="{% static 'css/auth.css' %}" rel="stylesheet" />

  <link href="{% static 'css/icons.min.css' %}" rel="stylesheet" />

  {% endblock css %}

</head>

<body {% block body_attribute %}{% endblock body_attribute %}>

  {% block content %}

  {% endblock content %}

  {% block modal %}
  {% include "auth/modals.html" %}
  {% endblock modal %}

  {% block extra_javascript %}{% endblock extra_javascript %}
  <script src="{% static 'js/auth.js' %}"></script>
</body>

</html>"""

try:
    # Remove read-only if present to allow write
    os.chmod(path, stat.S_IWRITE)
except:
    pass

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

# Set Read-Only
os.chmod(path, stat.S_IREAD)
print("File rewritten and set to Read-Only.")
