{% if site.data.year-2027.team %} 

<ul class="grid team-grid">
{% for member in site.data.year-2027.team %}
  <li class="grid__item">
    <img src="{{ member.image | relative_url }}" alt="{{ member.name }}" class="grid__cover team-grid__cover" loading="lazy" decoding="async">
    <h3 class="grid__title team-grid__title">{{ member.name }}</h3>
    <p class="grid__description">{{ member.description }}</p>
  </li>
{% endfor %} 
</ul>

{% endif %}
