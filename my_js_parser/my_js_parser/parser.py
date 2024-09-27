# The MIT License
#
# Copyright 2014, 2015 Piotr Dabkowski
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the 'Software'),
# to deal in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

from  lxml import etree
import json 
import quickjs
import re

def extract_all_json(script_text):
    json_list = []  # 存储提取的所有 JSON 对象
    start = -1  # 初始化起始位置
    open_braces = 0  # 追踪大括号的匹配情况
    open_brackets = 0  # 追踪方括号的匹配情况

    # 使用正则表达式匹配所有花括号和方括号
    script_label = re.finditer(r'[\{\}\[\]]', script_text)

    for item in script_label:
        if item.group() == '{':
            # 如果遇到左花括号并且没有其他打开的括号时，记录开始位置
            if open_braces == 0 and open_brackets == 0:
                start = item.start()
            open_braces += 1
        elif item.group() == '}':
            open_braces = open_braces - 1 if open_braces>0 else open_braces
            # 当大括号关闭并且没有其他打开的括号时，提取 JSON
            if open_braces == 0 and open_brackets == 0 and start != -1:
                json_list.append(script_text[start:item.end()])
                start = -1  # 重置 start，准备下一个 JSON 对象

        elif item.group() == '[':
            # 如果遇到左方括号并且没有其他打开的括号时，记录开始位置
            if open_braces == 0 and open_brackets == 0:
                start = item.start()
            open_brackets += 1
        elif item.group() == ']':
            open_brackets = open_brackets- 1 if open_brackets > 0 else open_brackets
            # 当方括号关闭并且没有其他打开的括号时，提取 JSON
            if open_braces == 0 and open_brackets == 0 and start != -1:
                json_list.append(script_text[start:item.end()])
                start = -1  # 重置 start，准备下一个 JSON 对象

    result = []
    if json_list:
        for json_part in json_list:
            try:
                # 尝试直接解析 JSON
                data = json.loads(json_part)
                result.append(data)
            except json.JSONDecodeError:
                try:
                    # 将单引号替换为双引号，确保它是有效的 JSON 格式
                    json_part = json_part.replace("'", '"')
                    data = json.loads(json_part)
                    result.append(data)
                except json.JSONDecodeError:
                    pass
    return result  # 如果找不到 JSON，返回空列表


def parse_html(html_content):
    define_vars = r"""
    const window = this;
    const document = {};
    const navigator = {
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    };
    """
    fetch_script = """
    const my_eval_result = (() => {
    const filterKey = ['onratechange', 'onpagehide', 'ondrag', 'scrollY', 'onselect', 'onwebkitanimationend', 'onmousewheel', 'scrollX', 'onplaying', 'ononline', 'pageYOffset', 'outerWidth', 'onerror', 'ondragover', 'ontimeupdate', 'onpause', 'ondeviceorientation', 'onpointerenter', 'ondragstart', 'onmouseleave', 'onreset', 'onpointerover', 'sessionStorage', 'onmouseout', 'onmouseover', 'onloadeddata', 'onloadstart', 'length', 'ongotpointercapture', 'outerHeight', 'onresize', 'ondragleave', 'onprogress', 'ondblclick', 'onmessageerror', 'oninput', 'onclick', 'ondurationchange', 'opener', 'screenX', 'onoffline', 'onpointercancel', 'origin', 'visualViewport', 'onsuspend', 'ontransitionend', 'onanimationend', 'frameElement', 'onunhandledrejection', 'oncancel', 'locationbar', 'onloadedmetadata', 'navigator', 'onkeypress', 'onwebkitanimationstart', 'onstalled', 'onbeforeinstallprompt', 'statusbar', 'oncanplay', 'onkeydown', 'onchange', 'onhashchange', 'onanimationiteration', 'ondeviceorientationabsolute', 'onseeked', 'closed', 'oncanplaythrough', 'onpointerdown', 'ondrop', 'onsubmit', 'ontoggle', 'oninvalid', 'onafterprint', 'personalbar', 'onstorage', 'onwheel', 'screenTop', 'onunload', 'ondragend', 'onwebkittransitionend', 'speechSynthesis', 'screenY', 'onbeforeprint', 'onbeforeunload', 'innerWidth', 'onmousemove', 'external', 'regeneratorRuntime', 'indexedDB', 'isSecureContext', 'onemptied', 'ondevicemotion', 'scrollbars', 'onanimationstart', 'oncontextmenu', 'onpageshow', 'ondragenter', 'onfocus', 'screen', 'onmouseenter', 'document', 'screenLeft', 'onmousedown', 'onseeking', 'menubar', 'onpointerleave', 'onplay', 'onpointerout', 'onwebkitanimationiteration', 'onauxclick', 'onpointerup', 'onabort', 'innerHeight', 'onclose', 'styleMedia', 'onvolumechange', 'oncuechange', 'onload', 'onpopstate', 'onmouseup', 'onscroll', 'toolbar', 'onlanguagechange', 'onblur', 'onmessage', 'localStorage', 'pageXOffset', 'onrejectionhandled', 'onappinstalled', 'onkeyup', 'onlostpointercapture', 'onpointermove', 'onended', 'devicePixelRatio', 'onsearch', 'onwaiting', 'customElements']
    return JSON.stringify(Object.entries(window).reduce((acc, [key, val]) => {
        if (filterKey.includes(key)) {
            return acc
        }
        try {
            JSON.stringify(val);
            acc[key] = val
        } catch (e) {
        }
        return acc;
    }, {}))
    })();"""


    html = etree.HTML(html_content)
    result = {}
    script_list = html.xpath('//script/text()')
    for script_text in script_list:
        script = f"""
            tmp = function() {{
            {define_vars}
            {script_text}
            {fetch_script}
            return my_eval_result
            }}
        """
        try:
            tmp_result = quickjs.Function("tmp", script)()
            js_result = json.loads(tmp_result)
            result.update(js_result)
        except Exception as e:
            pass
            # print("execute js script fail, e: {}".format(str(e)))
        try:
            tmp_result = quickjs.Function("tmp", f"""tmp = function() {{
                return JSON.stringify({script_text})
            }}
    """)()
            js_result = json.loads(tmp_result)
            result.update(js_result)
        except Exception as e:
            pass
            # print("execute js script fail, e: {}".format(str(e)))
        try:
            pattern = r'(?:var|const)\s+(\w+)\s*='
            matches = [_ for _ in re.findall(pattern, script_text)]
            if matches:
                tmp_result = quickjs.Function("tmp", f"""tmp = function() {{
                {define_vars}
                try {{
                    {script_text}
                }} catch {{
                }} finally {{
                    return JSON.stringify({{{", ".join(matches)}}})
                }}
            }}
    """)()
                js_result = json.loads(tmp_result)
                result.update(js_result)
        except Exception as e:
            pass
            # print("execute js script fail, e: {}".format(str(e)))
        try:
            context = quickjs.Context()
            context.eval(f"""
                {define_vars}
                try {{
                    {script_text}
                }} catch {{
                }}
                """)
            globals_js = """
            function getAllGlobalVars() {
                var globalVars = {};
                for (var varName in this) {
                    if (this.hasOwnProperty(varName)) {
                        try {
                            JSON.stringify(this[varName]);
                            globalVars[varName] = this[varName]
                        } catch(e) {
                        }
                    }
                }
                return JSON.stringify(globalVars);
            }
            getAllGlobalVars();
            """
            globals_js_str = context.eval(globals_js)
            global_vars = json.loads(globals_js_str)
            result.update(global_vars)
        except Exception as e:
            pass
        try:
            for item in extract_all_json(script_text):
                result.update(item)
        except Exception as e:
            pass
    return  result


