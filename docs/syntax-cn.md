# 语法规则

本篇文章将为你介绍 Tempson 的模板语法。

## 定界符

Tempson 的语法都是使用定界分割开来。在 Tempson 中有四种定界符，默认的定界符分别为：

- 表达式定界符（变量定界符）：`{{` 和 `}}`
- 块定界符：`{%` 和 `%}`
- 注释定界符：`{*` 和 `*}`
- 原始定界符：`{{{` 和 `}}}`

当然，你也可以自定自定义定界符，只需要在实例 `createDoc` 或 `createFragment` 时传入相应的配置：

```python
delimitersConfig = {
    'leftDelimiters': '{',
    'rightDelimiters':'}'
}

doc = new createDoc('template', delimitersConfig)
```

详细配置说明请查 [配置 Tempson](config-cn.md) 章节。

## 变量和表达式模板

凡是在表达式定界符内的字符，Tempson 一律会将其理解成表达式。在生成 HTML 的时候，Tempson 将会取表达式的值进行渲染。

### 变量

如下的例子中，`{{ a }}` 将会被替代为对应数据对象上 `a` 属性的值。

```python
count = 1
template = '<div>{{ a }}</div>'

doc = createDoc(template)
doc.render({ 'a': count })
```

将会输出：

```html
<div>1</div>
```

### 表达式

```python
count = 1
template = '<div>{{ a + 1 }}</div>'

doc = createDoc(template)
doc.render({ 'a': count })
```

将会输出

```html
<div>2</div>
```

Tempson 提供了完全的 Python 表达式支持。

但是，每个绑定都只能包含**单个表达式**，所以下面的例子都**不会**生效：

```python
# 这是语句，不是表达式
{{ a = 1 }}

# 流控制也不会生效，请使用三元表达式或块定界符
{{ if ok:
     return message
}}
```

> 模板表达式都被放在沙盒中，只能访问全局变量的一个白名单。你不应该在模板表达式中试图访问用户定义的全局变量。

## 块模板

当我们需要判断、循环或者其他流控制时，块模板就会派上用场了。

### 条件判断

如下的例子中，用块定界符把 Python 语法的` if` 语句包含起来，Tempson 会根据 `ok` 的布尔值，来判断渲染哪一个 HTML 片段。别忘了，`if` 语句结束时必须添加一个 `{% endif %}` 块语句。

```python
data = { 'ok': False }
template = '''
<div>
  {% if ok: %}
  <p>Good!</p>
  {% else: %}
  <p>Bad!</p>
  {% endif %}
</div>
'''

doc = createDoc(template)
doc.render(data)
```

将会输出

```html
<div>
  <p>Bad!</p>
</div>
```

同样，Tempson 也完全支持和 Python 里面相同语法的 `if` 语句：

```python
data = { 'ok': False, 'bad': True }
template = '''
<div>
  {% if ok and bad: %}
  <p>Good!</p>
  {% else: %}
  <p>Bad!</p>
  {% endif %}
</div>
'''

doc = createDoc(template)
doc.render(data)
```

将会输出

```HTML
<div>
  <p>Bad!</p>
</div>
```

请注意，和 `if` 语句绑定的数据类型**必须**为 Boolean，否则，Tempson 将会直接把绑定的数据当成 `true` 来渲染，如如下例子所示：

```python
data = { 'ok': 'False' }
template = '''
<div>
  {% if ok: %}
  <p>Good!</p>
  {% else: %}
  <p>Bad!</p>
  {% endif %}
</div>
'''

doc = createDoc(template)
doc.render(data)
```

将会输出：

```html
<div>
  <p>Good!</p>
</div>
```

### 循环

你也可以把 HTML 的片段用 `for` 语句包含起来，配合表达式定界符可以把一个 list 循环渲染出来。和条件渲染一样，`for` 语句结束时必须添加一个 `{% endfor %}` 块语句：

```python
data = { 'nums': [1, 2, 3, 4] }
template = '''
<ul>
  {% for num in nums: %}
  <li>{{ num * num }}</li>
  {% endfor %}
</ul>
'''

doc = createDoc(template)
doc.render(data)
```

将会渲染出：

```html
<ul>
  <li>1</li>
  <li>4</li>
  <li>9</li>
  <li>16</li>
</ul>
```

### 块语法的嵌套

除了判断和循环，在块语法中你还可以写入简单的 Python 语句：

```python
data = { 'nums': [1, 2, 3, 4] }
template = '''
<ul>
  {% for num in nums:%}
  	{% if not num = 2 %}
  	   <li>{{ num * num }}</li>
    {% endif %}
  {% endfor %}
</ul>
'''

doc = createDoc(template)
doc.render(data)
```

将会渲染出：

```html
<ul>
  <li>1</li>
  <li>9</li>
  <li>16</li>
</ul>
```

> 此外，和表达式语句一样，块语句的数据都被放在沙盒中，只能访问全局变量的一个白名单。你不应该在模板表达式中试图访问用户定义的全局变量，也不应该在块语句中试图访问上一个块语句的变量。

## 注释

用注释定界符括起来的内容，Tempson 将不会做任何的处理，同时也不会渲染到最终的页面中，如果你想要在最终的 HTML 中看到注释，请直接使用 HTML 的注释语法。

```python
template = '''
{* Tempson title *}
<h1>Tempson</h1>
'''

doc = createDoc(template)
doc.render(data)
```

将会只输出：

```html
<h1>Tempson</h1>
```

> Tempson 的注释语法是为了在开发时能更好的协作，并且不会影响到最终的输出的 HTML 而生的。

## 原始定界符

在前端开发中，有一个非常常见却又容易被忽视的安全问题—— [XSS 攻击](https://www.wikiwand.com/zh-cn/%E8%B7%A8%E7%B6%B2%E7%AB%99%E6%8C%87%E4%BB%A4%E7%A2%BC)。这个问题在你的数据中包含用户输入的内容时将不可忽视。

在 Tempson 解析和渲染页面的过程中，如果探测到渲染结果可能包含**简单的** XSS 攻击，Tempson 将会对其进行转义，以屏蔽攻击。

如果你不想要 Tempson 对数据进行防 XSS 攻击转义，你可以使用原始定界符，原始定界符的使用方法参考**表达式定界符**。

> Tempson 将仅仅不对内容进行转义，并不代表 Tempson 会直接输出原始定界符中的表达式。
>
> 另外，和表达式定界符一样，Tempson 会执行内部的表达式，且数据都被放在沙盒中，只能访问全局变量的一个白名单。你不应该在模板表达式中试图访问用户定义的全局变量。

