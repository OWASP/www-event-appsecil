{% if site.data.year-2025.sponsors %} 

<ul class="grid">
{% for sponsor in site.data.year-2025.sponsors %}
  <li class="grid__item">
    <img src="{{ sponsor.image }}" alt="{{ sponsor.name }}" class="grid__cover">
    <h3 class="grid__title">{{ sponsor.name }}</h3>
    <p class="grid__description">{{ sponsor.description }}</p>
  </li>
{% endfor %} 
</ul>

{% endif %}
