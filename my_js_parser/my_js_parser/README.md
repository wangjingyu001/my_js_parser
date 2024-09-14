# my_js_parser

my_js_parser 是一个用于从包含 JavaScript 代码的字符串中提取 JSON 数据的 Python 库。它可以从复杂的字符串中递归提取出所有嵌套的 JSON 对象，忽略多余的前缀和非 JSON 部分。

# 安装

你可以通过以下方式安装此库：
```
pip install my_js_parser
```

# 使用依赖：
```
lxml==5.2.2
quickjs==1.19.4
```
# 使用方法
## 从 JavaScript 字符串中提取所有 JSON 对象
my_js_parser 提供了 extract_all_json 函数和 parse_html 函数，它可以从一个包含 JavaScript 代码的字符串中提取所有的 JSON 对象


## 深度提取
### 导入模块
首先从 my_js_parser.parser 中导入 parse_html 函数：
```
from my_js_parser.parser import parse_html
```
函数说明
```
parse_html(data: str) -> dict
```
- 参数:
  - data (str): 想要解析的html字符串，其中包含 JSON 对象或者js对象。
- 返回值:
  - 返回一个包含所有提取出来的 JSON 字符串的字典。如果没有找到 JSON 对象，则返回空字典。

示例
```
from my_js_parser.parser import parse_html

# 示例html
js_code = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<script>
  window.INITIAL_STATE={'user': 'JohnDoe', 'age': 30};
window.DATA={'products': ['apple', 'banana', 'orange'], 'prices': [1.2, 0.5, 0.75]};
(function(){ var script = document.currentScript; script.parentNode.removeChild(script); })();

</script>
</body>
</html>

"""

# 提取所有 JSON 对象
json_data = parse_html(js_code)
print(f'parse result : {json_data}')

 
```
输出结果
```
parse result : {'INITIAL_STATE': {'user': 'JohnDoe', 'age': 30}, 'DATA': {'products': ['apple', 'banana', 'orange'], 'prices': [1.2, 0.5, 0.75]}, 'user': 'JohnDoe', 'age': 30, 'products': ['apple', 'banana', 'orange'], 'prices': [1.2, 0.5, 0.75]}
```


## 浅度提取
### 导入模块
首先从 my_js_parser.parser 中导入 extract_all_json 函数：
```
from my_js_parser.parser import extract_all_json
```
函数说明
```
extract_all_json(data: str) -> list[dict]
```
- 参数:
  - data (str): 想要解析的script字符串，其中包含 JSON 对象或者js对象。也可以直接传入html字符串，但是效果可能不会很理想，例如可能提取到很多无关的单个赋值表达式数据。
- 返回值:
  - 返回一个包含所有提取出来的 JSON 的 LIST 。如果没有找到 JSON 对象，则返回空列表。

示例
```
from my_js_parser.parser import extract_all_json

# 示例字符串，包含两个 JSON 对象和 JavaScript 代码
js_code = """
window.INITIAL_STATE={'user': 'JohnDoe', 'age': 30};
window.DATA={'products': ['apple', 'banana', 'orange'], 'prices': [1.2, 0.5, 0.75]};
(function(){ var script = document.currentScript; script.parentNode.removeChild(script); })();
"""

# 提取所有 JSON 对象
json_parts = extract_all_json(js_code)

# 输出提取到的 JSON 对象
for i, json_part in enumerate(json_parts):
    print(f"JSON {i + 1}: {json_part}")

 
 
```
输出结果
```
JSON 1: {'user': 'JohnDoe', 'age': 30}
JSON 2: {'products': ['apple', 'banana', 'orange'], 'prices': [1.2, 0.5, 0.75]}
```

# 注意 
- 使用深度提取的时候，会使用quickjs 来执行js代码，这样可能会导致资源的使用增加，但是会提取到更全面的数据，并且由于返回的是字典对象，对于多次重复的数据，可能造成的结果是前面提取的数据被后面提取的数据覆盖。如果担心这种情况可以使用浅度提取，使用 from lxml import etree 提取到所有的script数据后，使用浅度提取，浅度提取返回list，所以不会有深度提取的那种后面的数据把前面的数据覆盖的问题。

# 贡献
欢迎贡献此库的改进和新功能。
可以加入微信群反馈。
  ![img.png](img.png)

