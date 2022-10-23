
from PIL import Image
import feedparser

def transparent(input, output):
    """
    将图片中RGB为0的点变透明

    :param input: 输入图片 (.png)
    :param output: 输出图片 (.png)
    """
    img = Image.open(input)
    img = img.convert('RGBA')
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:  # 输入rgb 0 (纯黑)
            newData.append((255, 255, 255, 0))  # 输出rgb 255
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(output, "PNG")


def count(input):
    """
    查看图片中RGB为0的点的个数

    :param input: 输入图片 (.png)
    """
    img = Image.open(input)
    img = img.convert('RGBA')
    datas = img.getdata()
    count = 0
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            count += 1
    print(count)


def delete_between_str(str, start, end):
    """
    删除str中两字符串之间的内容

    :param str: 输入字符串
    :param start: 开始字符串
    :param end: 结束字符串
    :return: 删除后的字符串
    """
    while True:
        start_index = str.find(start)
        end_index = str.find(end)
        if start_index == -1 or end_index == -1:
            break
        str = str.replace(str[start_index:end_index + len(end)], "")
    return str


def update_table():
    """
    更新书影表格
    """
    rss_movietracker = feedparser.parse("https://www.douban.com/feed/people/222123847/interests")
    entries = rss_movietracker["entries"]  # 获取所有条目
    # 拼接html表格
    html = """
    <table>
        <tr>
            <th>名称</th>
            <th>海报</th>
            <th>时间</th>
        </tr>
    """
    for entry in entries:
        html += f"""
        <tr>
            <td>{entry["title"]}</td>
            <td>{entry["summary"]}</td>
            <td>{entry["published"]}</td>
        </tr>
    """
    html += "</table>"
    html = html.replace("\n", "")  # 去除换行符
    html = delete_between_str(html, "<p>", "</p>")  # 删除图片中的<p></p>
    while True:  # 删除图片中的<br/>
        if "  " in html:
            html = html.replace("  ", " ")
        else:
            break
    # 将html写入README指定位置
    with open("./README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        readme = delete_between_str(readme, "<!-- REMOVE_MARK -->", "<!-- MOVIE_TRACKER_END -->")
        readme = readme.replace("<!-- MOVIE_TRACKER_START -->", "<!-- MOVIE_TRACKER_START -->" + "<!-- REMOVE_MARK -->"
                                + html + "<!-- MOVIE_TRACKER_END -->")
    with open("./README.md", "w", encoding="utf-8") as f:
        f.write(readme)
