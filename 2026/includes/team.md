{% if site.data.year-2025.team %} 

<ul class="grid">
{% for member in site.data.year-2025.team %}
  <li class="grid__item">
    <img src="{{ member.image }}" alt="{{ member.name }}" class="grid__cover">
    <h3 class="grid__title">{{ member.name }}</h3>
    <p class="grid__description">{{ member.description }}</p>
  </li>
{% endfor %} 
</ul>

{% endif %}
