<div align="center">

# Contributing to FABLE·5.2

Thanks for helping build this list! Add one work per pull request, or open an issue if you'd rather not edit files.

</div>

---

## ✅ What Qualifies

- It was made with **Claude Fable 5.2** (the creator says so in the post).
- The work link opens directly in a browser: a game, 3D scene, web page, tool, or a repo with the source.
- Video-only posts are welcome in the *Video-only Demos* section if they are original work.
- No reshares of an existing entry, no "now available on our platform" announcements.

---

## 📦 What to Include

- Work link
- Link to the original post on X (or elsewhere)
- Creator handle
- One sentence on what it is (English; Chinese welcome too)

---

## 🔧 How to Add an Entry

Entries live in [`data/works.json`](data/works.json). Add your entry at the end of the array:

```json
{
  "id": 124,
  "section": "游戏",
  "title": "My Awesome Game",
  "title_zh": "我的超赞游戏",
  "description": "One sentence in English.",
  "description_zh": "一句话中文说明。",
  "author": "creator_handle",
  "url": "https://example.com/play",
  "extra_links": [],
  "post": "https://x.com/creator_handle/status/1234567890",
  "likes": 0,
  "preview": "assets/gifs/124.gif",
  "videos": []
}
```

Then regenerate both READMEs:

```bash
python gen_readmes.py
```

Finally, open a pull request. GitHub Actions will run `python gen_readmes.py` automatically on every push — no need to commit the generated files yourself.

---

<div align="center">

# 投稿指南

感谢帮忙一起完善这份清单！一次 PR 加一个作品；不想改文件就开 Issue。

</div>

---

## ✅ 收录标准

- 作者说明是用 **Claude Fable 5.2** 做的。
- 作品链接能直接在浏览器打开：游戏、3D 场景、网页、工具，或带源码的仓库。
- 仅视频的原创新作也欢迎，会归入 *仅视频演示* 分类。
- 不收录已有条目的转发、"现已在 X 平台上线"广告。

---

## 📦 需要的信息

- 作品链接
- 原帖链接（X 或其他平台）
- 作者账号
- 一句话说明（英文或中文均可）

---

## 🔧 如何添加条目

条目统一放在 [`data/works.json`](data/works.json) 末尾。添加后运行以下命令重新生成两份 README：

```bash
python gen_readmes.py
```

然后提交 PR。GitHub Actions 会在每次 push 时自动执行生成脚本 — 无需手动提交生成的文件。
