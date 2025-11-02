<ul class="about">

{% for item in site.data.year-2026.about-items %}
    <li class="about__item">
        <div class="about__info">
            <h3 class="about__title">{{item.title}}</h3>
            {% for text in item.items %}
                <p>{{text}}</p>
            {% endfor %}
        </div>
        <div class="about__cover">
            <img src="{{item.image}}" class="about__image">
        </div>
    </li>
{% endfor %}
</ul>





