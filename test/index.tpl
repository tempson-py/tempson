<!DOCTYPE html>
<html>
<head>
    <title>Test tempson</title>
</head>
<body>
    <ul>
        {% for item in list %}
            <li>{{ item['name'] }}: {{ item['age'] }}岁</li>
        {% endfor %}
    </ul>
</body>
</html>
