{% if site.data.year-2026.team %} 

<ul class="grid team-grid">
{% for member in site.data.year-2026.team %}
  <li class="grid__item">
    <img src="{{ member.image }}" alt="{{ member.name }}" class="grid__cover team-grid__cover">
    <h3 class="grid__title team-grid__title">{{ member.name }}</h3>
    <p class="grid__description">{{ member.description }}</p>
  </li>
{% endfor %} 
</ul>

{% endif %}
