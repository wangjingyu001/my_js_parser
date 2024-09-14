from setuptools import setup, find_packages
import os

# 读取 README.md 文件内容作为简介
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='my_js_parser',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        # 列出你的库的依赖项
        "lxml",
        "quickjs"
    ],
    py_modules=['my_js_parser.parser'],
    long_description=long_description,  # 详细描述，来自 README.md
    long_description_content_type='text/markdown',  # README 文件的格式
    # 也可以包含其他的元数据，如作者、描述、许可证等
)
