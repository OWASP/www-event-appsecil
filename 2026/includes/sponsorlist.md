{% if site.data.year-2026.sponsors %} 

{% for tier in site.data.year-2026.sponsors %}
  {% if tier.sponsors %}

  <h2 class="tier-title">{{ tier.tier }}</h2>
  <ul class="sponsor-list">
    {% for sponsor in tier.sponsors %}
      <li class="sponsor-list__item">
        {% if sponsor.url %}
        <a href="{{ sponsor.url }}" target="_blank">
        {% endif %}      
        <img src="/assets/img/Sponsors/{{ sponsor.image }}" alt="{{sponsor.name}}" class="sponsor-list__img sponsor-list__img_tier_{{ tier.tier }}">
        {% if sponsor.url %}
        </a>
        {% endif %}
      </li>
    {% endfor %}
  </ul>
  {% endif %}
{% endfor %} 

{% endif %}
