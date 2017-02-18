.. code:: django

  {# Load the tag library #}
  {% load propeller %}

  {# Load CSS and JavaScript #}
  {% propeller_css %}
  {% propeller_javascript %}

  {# Display django.contrib.messages as Bootstrap alerts #}
  {% propeller_messages %}

  {# Display a form #}
  <form action="/url/to/submit/" method="post" class="form">
    {% csrf_token %}
    {% propeller_form form %}
    {% buttons %}
      <button type="submit" class="btn btn-primary">
        {% propeller_icon "star" %} Submit
      </button>
    {% endbuttons %}
  </form>

  {# Read the documentation for more information #}
