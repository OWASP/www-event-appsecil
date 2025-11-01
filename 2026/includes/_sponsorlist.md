{% assign sponsors = site.data.year-2025.sponsors %}

{% if sponsors.diamond %}
## Diamond Sponsor 
<div class="sponsor-tier">
  {% for sponsor in sponsors.diamond %}
	<span class="sponsor diamond-sponsor">
	  <a href="{{ sponsor.url }}" title="{{ sponsor.name }}" target="_blank">
		{% if sponsor.image == blank %}
		  <p>{{ sponsor.name }}</p>
		{% else %} 
		  <img src="/assets/img/Sponsors/{{ sponsor.image }}"> 
		{% endif %}
	  </a>
	</span>
{% endfor %}
</div>
{% endif %}

{% if sponsors.platinum %}
## Platinum Sponsors
<div class="sponsor-tier">
  {% for sponsor in sponsors.platinum %}
	<span class="sponsor platinum-sponsor">
	  <a href="{{ sponsor.url }}" title="{{ sponsor.name }}" target="_blank">
		{% if sponsor.image == blank %}
		  <p>{{ sponsor.name }}</p>
		{% else %} 
		  <img src="/assets/img/Sponsors/{{ sponsor.image }}"> 
		{% endif %}
	  </a>
	</span>
{% endfor %}
</div>
{% endif %}

{% if sponsors.gold %}
### Gold Sponsors 
<div class="sponsor-tier">
  {% for sponsor in sponsors.gold %}
	  <span class="sponsor gold-sponsor">
		<a href="{{ sponsor.url }}" title="{{ sponsor.name }}" target="_blank">
		  {% if sponsor.image == blank %}
			<span>{{ sponsor.name }}</span>
		  {% else %} 
			<img src="/assets/img/Sponsors/{{ sponsor.image }}">
		  {% endif %}
		</a>
	  </span>
  {% endfor %}
</div>
{% endif %}

{% if sponsors.silver %}
### Silver Sponsors
<div class="sponsor-tier">
  {% for sponsor in sponsors.silver %}
	<span class="sponsor silver-sponsor">
	  <a href="{{ sponsor.url }}" title="{{ sponsor.name }}" target="_blank">
		{% if sponsor.image == blank %}
		  <span>{{ sponsor.name }}</span>
		{% else %} 
		  <img src="/assets/img/Sponsors/{{ sponsor.image }}"> 
		{% endif %}
	  </a>
	</span>
{% endfor %}
</div>
{% endif %}

{% if sponsors.bronze %}
#### Bronze Sponsors
<div class="sponsor-tier">
  {% for sponsor in sponsors.bronze %}
	<span class="sponsor bronze-sponsor">
	  <a href="{{ sponsor.url }}" title="{{ sponsor.name }}" target="_blank">
		{% if sponsor.image == blank %}
		  <span>{{ sponsor.name }}</span>
		{% else %} 
		  <img src="/assets/img/Sponsors/{{ sponsor.image }}"> 
		{% endif %}
	  </a>
	</span>
{% endfor %}
</div>
{% endif %}

{% if sponsors.community %}
#### Community Supporters
<div class="sponsor-tier">
  {% for sponsor in sponsors.community %}
	<span class="sponsor community-sponsor">
	  <a href="{{ sponsor.url }}" title="{{ sponsor.name }}" target="_blank">
		{% if sponsor.image == blank %}
		  <span>{{ sponsor.name }}</span>
		{% else %} 
		  <img src="/assets/img/Sponsors/{{ sponsor.image }}"> 
		{% endif %}
	  </a>
	</span>
{% endfor %}
</div>
{% endif %}

{% if sponsors.alacarte %}
#### A La Carte Sponsorships
<div class="sponsor-tier">
  {% for sponsor in sponsors.alacarte %}
	<span class="sponsor alacarte-sponsor">
	  <span>{{ sponsor.type }}</span>  <hr />
	  <a href="{{ sponsor.url }}" title="{{ sponsor.name }}" target="_blank">
		{% if sponsor.image == blank %}
		  <span>{{ sponsor.name }}</span>
		{% else %} 
		  <img src="/assets/img/Sponsors/{{ sponsor.image }}"> 
		{% endif %}
	  </a>
	</span>
{% endfor %}
</div>
{% endif %}
