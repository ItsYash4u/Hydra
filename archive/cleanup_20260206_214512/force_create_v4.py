
import os

dst = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\dashboard_v4.html"

content = """{% extends 'vertical.html' %}
{% load static %}
{% block title %}Dashboard{% endblock title %}
{% block page_content %}
<div class="alert alert-success">
    <h4>Dashboard Recovered</h4>
    <p>If you see this, the template reloading is working.</p>
</div>
{% endblock page_content %}
"""

print(f"Writing test content to {dst}")
try:
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")
