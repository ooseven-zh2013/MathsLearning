import re

with open('03_命题与逻辑.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到第一个 <h2> 之前的内容（head 部分）
first_h2_pos = content.find('<h2>')
head = content[:first_h2_pos]

# 提取所有节（每个 <h2>...</h2> 到下一个 <h2> 或文件结尾）
h2_iter = re.finditer(r'<h2>[^<]+</h2>', content)
sections = []
starts = [m.start() for m in re.finditer(r'<h2>[^<]+</h2>', content)]
ends = starts[1:] + [len(content)]
for s, e in zip(starts, ends):
    sections.append(content[s:e])

print('共 %d 个节' % len(sections))
for i, sec in enumerate(sections):
    m = re.search(r'<h2>([^<]+)</h2>', sec)
    print('  [%d] %s' % (i, m.group(1) if m else '无'))

# 新顺序：0,1,2,3,6,4,5,7,8
new_order = [0, 1, 2, 3, 6, 4, 5, 7, 8]
new_sections = [sections[i] for i in new_order]

# 更新每个节的 h2 编号
new_titles = [
    '一、什么是命题？（扩建）',
    '二、逻辑联结词：把命题串起来',
    '三、充分条件与必要条件',
    '四、充要条件（$\iff$）',
    '五、四种基本的命题变换',   # old 6 -> new 5
    '六、命题的否定 vs 否命题（容易混淆！）',  # old 4 -> new 6
    '七、反证法',          # old 5 -> new 7
    '八、在数学证明中的运用',
    '✅ 检查点',
]

for i in range(len(new_sections)):
    # 替换 h2 标签中的节号
    new_sections[i] = re.sub(
        r'<h2>[^<]+</h2>',
        '<h2>%s</h2>' % new_titles[i],
        new_sections[i],
        count=1
    )

# 扩建第一节：在 <table> 之前插入命题的两种形式
# 找到第一节中 </p>\n<p>💡 判断标准 之前的位置
sec0 = new_sections[0]
insert_pos = sec0.find('</p>\n<p>💡 <strong>判断标准</strong>')
if insert_pos == -1:
    insert_pos = sec0.find('💡 <strong>判断标准</strong>')
    # 往前找到段落开始
    insert_pos = sec0.rfind('<p>', 0, insert_pos)

extra = (
    '<p>命题通常有两种形式，后面的学习会反复用到：</p>'
    '<table>'
    '<thead><tr><th>形式</th><th>结构</th><th>例子</th></tr></thead>'
    '<tr><td><strong>条件形式</strong></td>'
    '<td>如果 $P$，则 $Q$<br>（由<strong>条件</strong> $P$ 和 <strong>结论</strong> $Q$ 构成）</td>'
    '<td>"如果下雨，则地面湿"<br>条件：下雨；结论：地面湿</td></tr>'
    '<tr><td><strong>判断形式</strong></td>'
    '<td>$S$ 是 $P$<br>（由<strong>判断对象</strong> $S$ 和 <strong>对该对象的判断</strong> $P$ 构成）</td>'
    '<td>"$\\pi$ 是无理数"<br>判断对象：$\\pi$；判断：是无理数</td></tr>'
    '</table>'
    '<p>💡 两种形式可以互相转换：</p>'
    '<blockquote>'
    '"$\\pi$ 是无理数" $\\iff$ "如果一个数是 $\\pi$，那么它是无理数"<br>'
    '（判断对象变成条件，对该对象的判断变成结论）'
    '</blockquote>'
    '<p>后续章节中，当你看到"如果 $P$，则 $Q$"时，都可以这样理解：</p>'
    '<ul>'
    '<li><strong>条件形式</strong>：$P$（条件）+ $Q$（结论）</li>'
    '<li><strong>判断形式</strong>：$P$（判断对象）+ $Q$（对该对象的判断）</li>'
    '</ul>'
    '<hr>'
)

if insert_pos > 0:
    new_sec0 = sec0[:insert_pos] + extra + sec0[insert_pos:]
    new_sections[0] = new_sec0
    print('第一节扩建完成')
else:
    print('警告：未找到插入位置，第一节未扩建')

# 修复第六节（命题的否定 vs 否命题）中对逆否命题的引用
# 原句：原命题 $\equiv$ 逆否命题（真假相同），但原命题和否命题没有这种关系！
# 现在四种命题变换在第五节讲了，所以引用是没问题的，只需确认。
# 另外检查点中引用第四节（充要条件）的内容，现在还是第四节，没问题。

# 拼接新文件
new_content = head + ''.join(new_sections)

with open('03_命题与逻辑_rebuild.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('重建完成，输出到 03_命题与逻辑_rebuild.html')
print('请检查后替换原文件')
