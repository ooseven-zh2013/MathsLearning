import re

with open('03_命题与逻辑.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到所有 <h2>...</h2> 节的位置
h2_pattern = re.compile(r'<h2>[^<]+</h2>')
matches = list(h2_pattern.finditer(content))

# 每个节的起止位置
sections = []
for i, m in enumerate(matches):
    start = m.start()
    end = matches[i+1].start() if i+1 < len(matches) else len(content)
    sections.append((start, end, m.group()))

print('找到 %d 个节：' % len(sections))
for i, (s, e, tag) in enumerate(sections):
    print('  [%d] %s' % (i, tag))

# 新顺序：0,1,2,3,6,4,5,7,8
# 即：一,二,三,四,七(四种变换),五(命题否定),六(反证法),八,检查点
new_order = [0, 1, 2, 3, 6, 4, 5, 7, 8]

# head 部分（<!DOCTYPE> 到第一个 <h2> 之前）
head_end = sections[0][0]
head = content[:head_end]

# 按新顺序组装
new_content = head
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

for idx, sec_idx in enumerate(new_order):
    s, e, old_tag = sections[sec_idx]
    body = content[s:e]
    # 替换 <h2> 中的标题文字
    new_tag = '<h2>%s</h2>' % new_titles[idx]
    body = body.replace(old_tag, new_tag, 1)
    new_content += body

# 扩建第一节：在 <table> 之前插入命题的两种形式
# 找到第一节中第一个 <table> 的位置
table_pos = new_content.find('<table>')
if table_pos > 0:
    # 在 <table> 前插入新内容
    extra = (
        '<p>命题通常有两种构成形式，理解它们对后续学习非常重要：</p>\n'
        '<table>\n'
        '<thead><tr><th>形式</th><th>结构</th><th>例子</th></tr></thead>\n'
        '<tbody>\n'
        '<tr><td><strong>条件形式</strong></td>\n'
        '<td>如果 $P$，则 $Q$<br>（由<strong>条件</strong> $P$ 和 <strong>结论</strong> $Q$ 构成）</td>\n'
        '<td>"如果下雨，则地面湿"<br>条件：下雨；结论：地面湿</td></tr>\n'
        '<tr><td><strong>判断形式</strong></td>\n'
        '<td>$S$ 是 $P$<br>（由<strong>判断对象</strong> $S$ 和 <strong>对该对象的判断</strong> $P$ 构成）</td>\n'
        '<td>"$\\pi$ 是无理数"<br>判断对象：$\\pi$；判断：是无理数</td></tr>\n'
        '</tbody>\n'
        '</table>\n'
        '<p>💡 两种形式可以互相转换：</p>\n'
        '<blockquote>\n'
        '"$\\pi$ 是无理数" $\\iff$ "如果一个数是 $\\pi$，那么它是无理数"<br>\n'
        '（判断对象变成条件，对该对象的判断变成结论）\n'
        '</blockquote>\n'
        '<p>后续章节中遇到"如果 $P$，则 $Q$"时，都可以这样理解：</p>\n'
        '<ul>\n'
        '<li><strong>条件形式</strong>：$P$（条件）+ $Q$（结论）</li>\n'
        '<li><strong>判断形式</strong>：$P$（判断对象）+ $Q$（对该对象的判断）</li>\n'
        '</ul>\n'
    )
    new_content = new_content[:table_pos] + extra + new_content[table_pos:]

with open('03_命题与逻辑.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('\n重建完成！')
print('新顺序：')
for i, t in enumerate(new_titles):
    print('  [%d] %s' % (i, t))
