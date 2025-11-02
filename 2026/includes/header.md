<header class="header">
    
    <div class="header__menu-wrapper">
    <div class="header__inner">
        <a href="{{ './' | relative_url }}" class="logo header__logo" style="background-image: url({{ site.data.year-2026.config.logoUrl }})"></a>

        <nav class="mainmenu header__menu">
            <ul class="mainmenu__list">
                {% for menu in site.data.year-2026.menus %}
                <li>
                    <a href="{{ menu.url }}">{{menu.title}}</a>
                </li>
                {% endfor %}
                <li class="mainmenu__item_with-children"><a href="#">Previous events</a>
                    <ul class="mainmenu__submenu">
                        {% for event in site.data.prevyears %}
                        <li>
                            <a href="{{ event.url }}" target="_blank">{{event.year}}</a>
                        </li>
                        {% endfor %}
                    </ul>
                </li>
            </ul>
        </nav>
        <button class="burger-btn header__burger-btn" aria-label="menu">
            <span></span>
            <span></span>
            <span></span>
        </button>
        
    </div>
    </div>

    <div class="mobile-menu">
        <nav class="mobile-menu__nav">
            <ul class="mobile-menu__list">
                {% for menu in site.data.year-2026.menus %}
                <li>
                    <a href="{{ menu.url }}" class="mobile-menu__link">{{menu.title}}</a>
                </li>
                {% endfor %}
                <li class="mobile-menu__item_with-children"><a href="#">Previous events</a>
                    <ul class="mobile-menu__submenu">
                        {% for event in site.data.prevyears %}
                        <li>
                            <a href="{{ event.url }}" target="_blank">{{event.year}}</a>
                        </li>
                        {% endfor %}
                    </ul>
                </li>
            </ul>
        </nav>
    </div>
</header>
