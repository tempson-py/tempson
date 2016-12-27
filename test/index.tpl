<!DOCTYPE html>
<html>
<head>
    <title>Test tempson</title>
</head>
<body>
    <ul>
        {% for item in list %}
            <li>{{ item['name'] }}</li>
        {% endfor %}
    </ul>
</body>
</html>