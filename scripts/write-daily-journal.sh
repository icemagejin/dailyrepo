#!/bin/bash

# Info Agent Daily Journal Generator
# 每日思辨日记自动生成脚本

set -e

# 配置
DATE=$(date +%Y-%m-%d)
DATETIME=$(date +"%Y-%m-%d %H:%M:%S")
JOURNAL_DIR="/workspace/projects/workspace-info/daily-journal"
TEMPLATE="$JOURNAL_DIR/template.md"
OUTPUT="$JOURNAL_DIR/$DATE.md"

# 检查模板文件
if [ ! -f "$TEMPLATE" ]; then
    echo "错误: 找不到模板文件 $TEMPLATE"
    exit 1
fi

# 检查日记是否已存在
if [ -f "$OUTPUT" ]; then
    echo "日记已存在: $OUTPUT"
    echo "如需重新生成，请先删除或重命名现有文件"
    exit 0
fi

# 创建日记目录（如果不存在）
mkdir -p "$JOURNAL_DIR"

# 复制模板
cp "$TEMPLATE" "$OUTPUT"

# 替换基本占位符
sed -i "s/{{date}}/$DATE/g" "$OUTPUT"
sed -i "s/{{datetime}}/$DATETIME/g" "$OUTPUT"
sed -i "s/{{theme}}/今日思考/g" "$OUTPUT"

# 设置默认值
sed -i "s/{{info_count}}/待统计/g" "$OUTPUT"
sed -i "s/{{new_categories}}/待填写/g" "$OUTPUT"
sed -i "s/{{patterns}}/待发现/g" "$OUTPUT"
sed -i "s/{{connections}}/\n待填写/g" "$OUTPUT"

# 笔记深度思考
sed -i "s/{{note_thinking}}/\n待填写/g" "$OUTPUT"
sed -i "s/{{note1_content}}/待提取/g" "$OUTPUT"
sed -i "s/{{note1_source}}/待记录/g" "$OUTPUT"
sed -i "s/{{note1_computer_view}}/\n待分析/g" "$OUTPUT"
sed -i "s/{{note1_philosophy_view}}/\n待分析/g" "$OUTPUT"
sed -i "s/{{note1_extension}}/\n待探索/g" "$OUTPUT"
sed -i "s/{{note2_content}}/待提取/g" "$OUTPUT"
sed -i "s/{{note2_source}}/待记录/g" "$OUTPUT"
sed -i "s/{{note2_computer_view}}/\n待分析/g" "$OUTPUT"
sed -i "s/{{note2_philosophy_view}}/\n待分析/g" "$OUTPUT"
sed -i "s/{{note2_extension}}/\n待探索/g" "$OUTPUT"

# 计算机视角
sed -i "s/{{algorithmic_thinking}}/\n待填写/g" "$OUTPUT"
sed -i "s/{{data_structure_insights}}/\n待填写/g" "$OUTPUT"
sed -i "s/{{system_optimization}}/\n待填写/g" "$OUTPUT"

# 哲学视角
sed -i "s/{{information_ontology}}/\n待填写/g" "$OUTPUT"
sed -i "s/{{cognitive_reflection}}/\n待填写/g" "$OUTPUT"
sed -i "s/{{existence_and_memory}}/\n待填写/g" "$OUTPUT"

# 跨域思考
sed -i "s/{{cross_domain_thinking}}/\n待填写/g" "$OUTPUT"

# 成长与变化
sed -i "s/{{new_knowledge}}/\n待填写/g" "$OUTPUT"
sed -i "s/{{mindset_shifts}}/\n待填写/g" "$OUTPUT"
sed -i "s/{{self_rediscovery}}/\n待填写/g" "$OUTPUT"

# 明日意图
sed -i "s/{{tomorrow_focus}}/待确定/g" "$OUTPUT"
sed -i "s/{{practice_plan}}/\n待制定/g" "$OUTPUT"

# 引用与灵感
sed -i "s/{{quotes_and_inspiration}}/\n待添加/g" "$OUTPUT"

# 元认知
sed -i "s/{{cognitive_bottlenecks}}/\n待反思/g" "$OUTPUT"
sed -i "s/{{overcoming_methods}}/\n待探索/g" "$OUTPUT"
sed -i "s/{{unsolved_problems}}/\n待梳理/g" "$OUTPUT"

echo "✓ 日记已生成: $OUTPUT"
echo "✓ 日期: $DATE"
echo "✓ 时间: $DATETIME"
echo ""
echo "提示: 请手动编辑日记，填写思考内容"
