<header>
    <div class="top">
        <a href="{{ './' | relative_url }}" class="logo" style="background-image: url(AppSecIL_logo.png)"></a>
    </div>
	
    <nav>
        <ul class="nav navbar-nav">
            {% for menu in site.data.year-2023.menus %}
            <li>
                <a href="./{{ menu.url }}">{{menu.title}}</a>
            </li>
            {% endfor %}
        </ul>
    </nav>
</header>
