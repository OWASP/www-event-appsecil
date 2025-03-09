<header class="header">
    <div class="header__inner">
            <a href="{{ './' | relative_url }}" class="logo header__logo" style="background-image: url({{ site.data.year-2025.config.logoUrl }})"></a>

        <nav class="mainmenu header__menu">
            <ul class="mainmenu__list">
                {% for menu in site.data.year-2025.menus %}
                <li>
                    <a href="{{ menu.url }}">{{menu.title}}</a>
                </li>
                {% endfor %}
                <li class="mainmenu__item_with-children"><a href="#">Previous events</a>
                    <ul class="mainmenu__submenu">
                        {% for event in site.data.prevyears %}
                        <li>
                            <a href="{{ event.url }}">{{event.year}}</a>
                        </li>
                        {% endfor %}
                    </ul>
                </li>
            </ul>
        </nav>
    </div>
</header>
