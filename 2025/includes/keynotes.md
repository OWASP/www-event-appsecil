{% if site.data.year-2025.keynotes %} 

<ul class="grid">
{% for keynote in site.data.year-2025.keynotes %}
  <li class="grid__item">
    <img src="{{ keynote.image }}" alt="{{ keynote.name }}" class="grid__cover">
    <h3 class="grid__title">{{ keynote.name }}</h3>
    <p class="grid__description">{{ keynote.description }}</p>
  </li>
{% endfor %} 
</ul>

{% endif %}
