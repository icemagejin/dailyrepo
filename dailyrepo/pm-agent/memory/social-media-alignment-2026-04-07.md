# Social Media Agent 数据格式对齐记录

## 对齐时间
- 2026-04-07 08:30

## 对齐内容

### PM Agent 需求
AI 日报生成需要以下结构化数据：

#### 数据格式（JSON）
```json
{
  "report_date": "2026-04-07",
  "generated_at": "2026-04-07T08:00:00+08:00",
  "data": {
    "industry_trends": [
      {
        "id": "trend_001",
        "title": "示例标题",
        "summary": "简短摘要",
        "content": "详细内容",
        "source": "twitter/youtube/arxiv",
        "source_url": "原始链接",
        "author": "发布者",
        "publish_date": "2026-04-07T10:00:00+08:00",
        "detected_date": "2026-04-07T08:00:00+08:00",
        "tags": ["ai", "llm", "product"],
        "importance": "high",
        "is_duplicate": false,
        "duplicate_of": null
      }
    ],
    "academic_papers": [
      {
        "id": "paper_001",
        "title": "论文标题",
        "authors": ["作者1", "作者2"],
        "arxiv_id": "2404.xxxxx",
        "abstract": "摘要",
        "key_contributions": [
          "核心贡献1",
          "核心贡献2"
        ],
        "publish_date": "2026-04-06",
        "arxiv_url": "https://arxiv.org/abs/2404.xxxxx"
      }
    ],
    "twitter_trends": [
      {
        "id": "twitter_001",
        "content": "推文内容",
        "author": "账号名",
        "author_handle": "@handle",
        "url": "推文链接",
        "publish_date": "2026-04-07T09:00:00+08:00",
        "likes": 1000,
        "retweets": 500,
        "replies": 100
      }
    ],
    "youtube_videos": [
      {
        "id": "youtube_001",
        "title": "视频标题",
        "channel": "频道名",
        "channel_url": "频道链接",
        "video_url": "视频链接",
        "publish_date": "2026-04-06T20:00:00+08:00",
        "duration": "45:30",
        "views": 50000
      }
    ],
    "producthunt_launches": [
      {
        "id": "ph_001",
        "name": "产品名",
        "tagline": "一句话描述",
        "description": "产品描述",
        "url": "产品链接",
        "launch_date": "2026-04-07",
        "votes": 1000,
        "category": "AI Tools"
      }
    ],
    "a16z_insights": [
      {
        "id": "a16z_001",
        "title": "标题",
        "content": "内容",
        "source_url": "链接",
        "publish_date": "2026-04-07",
        "category": "category"
      }
    ]
  },
  "statistics": {
    "total_items": 150,
    "new_items_today": 139,
    "duplicates_filtered": 11,
    "by_category": {
      "industry_trends": 30,
      "academic_papers": 50,
      "twitter_trends": 40,
      "youtube_videos": 10,
      "producthunt_launches": 5,
      "a16z_insights": 15
    }
  }
}
```

### 关键字段
1. **`publish_date`**：原始发布时间（判断新闻新鲜度）
2. **`detected_date`**：监控到的时间（判断是否为今天的新内容）
3. **`source`**：数据来源
4. **`source_url`**：原始链接
5. **`is_duplicate`**：是否为重复内容（7 天去重）
6. **`tags`**：标签（便于分类）

### 板块映射
- `industry_trends` → 业界趋势
- `academic_papers` → 最新论文
- `twitter_trends` → 热门 X 动态
- `youtube_videos` → 播客推荐（合并到业界趋势）
- `producthunt_launches` → ProductHunt 新产品
- `a16z_insights` → a16z 新热榜单点评

### 输出位置
```
/workspace/work-life-balance/reports/daily/
└── social-media-report-2026-04-07.json
```

### 重要约束
1. **去重机制**：基于 `title` + `source_url` 进行 7 天去重
2. **新鲜度过滤**：标记 `publish_date` 和 `detected_date`
3. **数据完整性**：每个项目必须有足够的 `content` 或 `summary`
4. **分类准确性**：正确分类到对应板块
5. **时间格式**：ISO 8601 格式

## 后续行动
- [ ] 与 Social Media Agent 对齐此格式
- [ ] Social Media Agent 确认可行性
- [ ] 更新 PM Agent 日报生成脚本
- [ ] 测试完整流程
