import json, re, pathlib

ROOT = pathlib.Path(__file__).parent
data = json.loads((ROOT / "data" / "works.json").read_text(encoding="utf-8"))

SEC_EN = {
    "游戏": "Games",
    "3D 场景": "3D Worlds & Scenes",
    "网页与工具": "Web Pages & Tools",
    "视频与动画（附源码）": "Animation & Film (with source)",
    "video-only": "Video-only Demos",
}
SEC_DESC_EN = {
    "游戏": "Games you can open and play right now, from first-person shooters to an entire destructible Earth.",
    "3D 场景": "Explorable 3D worlds and real-time rendered scenes.",
    "网页与工具": "Useful or stunning web apps and tools.",
    "视频与动画（附源码）": "Animation and film projects with full source included.",
    "video-only": "Creators posted a video but no public link. Click a preview to watch the original post.",
}
SEC_DESC_ZH = {
    "游戏": "可以直接打开开玩的游戏 — 从第一人称射击到整个可破坏的地球。",
    "3D 场景": "可漫游的 3D 世界与实时渲染场景。",
    "网页与工具": "实用或惊艳的网页应用与工具。",
    "视频与动画（附源码）": "附完整源码的动画与短片项目。",
    "video-only": "创作者只发了视频、没有公开链接。点击预览可看原帖视频。",
}

def fmt_likes(n):
    if not n:
        return ""
    if n >= 1000:
        return f"♥ {n/1000:.1f}".rstrip("0").rstrip(".") + "k"
    return f"♥ {n}"

def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")

def row(w, lang):
    title = w.get("title_zh") if lang == "zh" else w["title"]
    if not title:
        title = w["title"]
    desc = (w.get("description_zh") or w["description"]) if lang == "zh" else w["description"]
    likes = fmt_likes(w.get("likes"))
    desc_full = f"{desc} {likes}".strip() if desc else likes
    extras = ""
    for l in (w.get("extra_links") or []):
        m = re.match(r"^(.+?)\s+(https?://\S+)$", l)
        if m:
            extras += f"<br>↳ [{m.group(1)}]({m.group(2)})"
    link = f"[{esc(title)}]({w['url']})" if w.get("url") else f"**{esc(title)}**"
    post = f"[post]({w['post']})" if w.get("post") else "—"
    author = f"[@{w['author']}](https://x.com/{w['author']})" if w.get("author") else "—"
    return f"| {w['id']} | ![{esc(w['title'])}]({w.get('preview','assets/no-preview.svg')}) | **{link}**<br>{esc(desc_full)}{extras} | {author} | {post} |"

def table(items, lang):
    h = ["| # | Preview | Work | Creator | Post |",
         "|---|---------|------|---------|------|"]
    return "\n".join(h + [row(w, lang) for w in items])

def gen(lang):
    live = [w for w in data if w["section"] != "video-only"]
    most = sorted(live, key=lambda w: -(w.get("likes") or 0))[:6]
    secs = []
    for sec in ["游戏", "3D 场景", "网页与工具", "视频与动画（附源码）", "video-only"]:
        items = [w for w in data if w["section"] == sec]
        name = "Video-only Demos" if sec == "video-only" else SEC_EN[sec]
        desc = SEC_DESC_EN[sec] if lang == "en" else SEC_DESC_ZH[sec]
        secs.append((sec, name, desc, items))
    return most, secs

# Build both READMEs
for lang, path in [("en", "README.md"), ("zh", "README.zh-CN.md")]:
    most, secs = gen(lang)
    banner = '<img src="assets/banner.svg" alt="Awesome Fable 5.2" width="820">'
    if lang == "zh":
        tagline = "<h3>用 Claude Fable 5.2 做出的、真正可以打开来玩的东西</h3>"
        badges = '''[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![在线作品](https://img.shields.io/badge/在线作品-57-6b4eff)](#-游戏)
[![视频演示](https://img.shields.io/badge/视频演示-61-ff7a59)](#-仅视频演示)
[![链接验证](https://img.shields.io/badge/链接验证于-2026--11--10-2ea44f)](#-这份清单是怎么做的)
[![网站](https://img.shields.io/badge/交互站点-打开-0a0a0f?style=flat&labelColor=6b4eff&color=0a0a0f)](https://kingll2026.github.io/helium-fable-5.2/)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)

**简体中文** · [English](README.md)'''
        intro1 = "Claude Fable 5.2 在 2026-11-09 发布。发布后两天里，X 上出现了大量用它做的游戏、3D 世界和网页。这份清单只收**能点开就用的作品**：57 个在线作品，每个链接都在 2026-11-10 实际打开验证过；另有 61 个只发了视频的高赞演示，单独放在后面。"
        forknote = "> 🍴 Fork 自 [fengyiqicoder/awesome-fable-5.2](https://github.com/fengyiqicoder/awesome-fable-5.2) — 本仓库在此基础上新增了交互式画廊站点、双语界面和搜索功能。"
        intro2 = "每一项都配了几秒的动图预览，写明作者，并链接回原帖看完整视频。觉得有用就点个 ⭐，作品还在每天增加。"
        gallery = "> 🌐 **不想啃表格？** 完整清单已同步为可交互画廊：支持搜索、中英切换、视频站内播放：**[kingll2026.github.io/helium-fable-5.2](https://kingll2026.github.io/helium-fable-5.2/)**"
        news_title = "## 📰 动态"
        news = """- **2026-11-11**: 交互画廊上线 — 搜索、中英切换、视频播放（[源码](index.html)）。
- **2026-11-10**: 每条作品都配上了动图预览。
- **2026-11-10**: 首次发布 — 57 个在线作品 + 61 个视频演示。"""
        toc_title = "## 📑 目录"
        toc = """- [⭐ 最受欢迎](#-最受欢迎)
- [🎮 游戏](#-游戏) · 22
- [🌍 3D 世界 & 场景](#-3d-世界--场景) · 12
- [🧰 网页 & 工具](#-网页--工具) · 15
- [🎬 动画 & 短片（附源码）](#-动画--短片附源码) · 8
- [📺 仅视频演示](#-仅视频演示) · 61
- [🔗 相关清单](#-相关清单)
- [🧭 这份清单是怎么做的](#-这份清单是怎么做的)
- [🤝 投稿](#-投稿)"""
        ml_title = "## ⭐ 最受欢迎"
        ml_desc = "点赞数最高的六个在线作品。"
        more = "…还有 59 个 — 完整列表见[交互画廊](https://kingll2026.github.io/helium-fable-5.2/)。"
        related_title = "## 🔗 相关清单"
        related = "- [awesome-fable5-2-videos](https://github.com/yihui-dev/awesome-fable5-2-videos) — 专注于视频和背后提示词的姐妹清单。"
        how_title = "## 🧭 这份清单是怎么做的"
        how = """- 全部 118 个作品来自发布后 48 小时内的 X 帖子。
- 每个作品链接都在浏览器中实际打开确认可加载；每个视频都完整看过或抽查过。
- 动图预览（几秒、静音、低清）取自创作者自己的演示视频或在线站点。
- 媒体报道、"现已在 X 上线"广告、工具仓库和纯转发已剔除。署名一律归原作者；仅当创作者本人未发链接时才注明转发者。"""
        contrib_title = "## 🤝 投稿"
        contrib = """发现有漏掉的？开一个 [issue](../../issues/new) 或 PR，附上作品链接和原帖。链接必须能直接打开，作品必须是用 Fable 5.2 做的。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

条目统一加到 [`data/works.json`](data/works.json)，两份 README 都由它自动生成。"""
        lic_title = "## ⚖️ 许可与声明"
        lic = """所有作品版权归创作者本人。本仓库只做索引，仅保留几秒的低清动图预览，不含完整作品或视频；完整视频请移步原帖。创作者可通过 issue 要求撤下预览或条目。与 Anthropic 无关。

本仓库内容遵循 [CC0-1.0](LICENSE) 发布。"""
        credit = '<p align="right">策展人 <strong>Helium</strong> · Fork 自 <a href="https://github.com/fengyiqicoder/awesome-fable-5.2">awesome-fable-5.2</a></p>'
        count_suffix = "件作品"
        anchor = {"游戏":"-游戏","3D 场景":"-3d-世界--场景","网页与工具":"-网页--工具","视频与动画（附源码）":"-动画--短片附源码","video-only":"-仅视频演示"}
    else:
        tagline = "<h3>Things people built with Claude Fable 5.2 that you can actually open and play</h3>"
        badges = '''[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Works](https://img.shields.io/badge/live_works-57-6b4eff)](#-games)
[![Demos](https://img.shields.io/badge/video_demos-61-ff7a59)](#-video-only-demos)
[![Links checked](https://img.shields.io/badge/links_checked-2026--11--10-2ea44f)](#-how-this-list-was-made)
[![Website](https://img.shields.io/badge/interactive_site-open-0a0a0f?style=flat&labelColor=6b4eff&color=0a0a0f)](https://kingll2026.github.io/helium-fable-5.2/)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)

**English** · [简体中文](README.zh-CN.md)'''
        intro1 = "Claude Fable 5.2 shipped on 2026-11-09. Within two days X filled up with games, 3D worlds and web pages made with it. This list collects the ones **you can open right now**: 57 live works, every link opened and checked on 2026-11-10, plus 61 popular video-only demos in a separate section."
        forknote = "> 🍴 Forked from [fengyiqicoder/awesome-fable-5.2](https://github.com/fengyiqicoder/awesome-fable-5.2) — added the interactive gallery site, bilingual UI and search."
        intro2 = "Every entry has a few-second GIF preview, credits its creator and links back to the original post for the full video. If this helps, a ⭐ keeps it coming — new works are still appearing daily."
        gallery = "> 🌐 **Prefer browsing over reading?** The full list is also available as an interactive gallery with search, bilingual UI and inline video playback: **[kingll2026.github.io/helium-fable-5.2](https://kingll2026.github.io/helium-fable-5.2/)**"
        news_title = "## 📰 News"
        news = """- **2026-11-11**: Interactive gallery site launched — search, EN/中文 toggle, video player ([source](index.html)).
- **2026-11-10**: Every entry now has a GIF preview.
- **2026-11-10**: First release — 57 live works + 61 video demos."""
        toc_title = "## 📑 Contents"
        toc = """- [⭐ Most Loved](#-most-loved)
- [🎮 Games](#-games) · 22
- [🌍 3D Worlds & Scenes](#-3d-worlds--scenes) · 12
- [🧰 Web Pages & Tools](#-web-pages--tools) · 15
- [🎬 Animation & Film (with source)](#-animation--film-with-source) · 8
- [📺 Video-only Demos](#-video-only-demos) · 61
- [🔗 Related Lists](#-related-lists)
- [🧭 How This List Was Made](#-how-this-list-was-made)
- [🤝 Contributing](#-contributing)"""
        ml_title = "## ⭐ Most Loved"
        ml_desc = "The six most-liked live works."
        more = "*…and 59 more — see the full list in the [interactive gallery](https://kingll2026.github.io/helium-fable-5.2/).*"
        related_title = "## 🔗 Related Lists"
        related = "- [awesome-fable5-2-videos](https://github.com/yihui-dev/awesome-fable5-2-videos) — A sister list focused on videos and the prompts behind them."
        how_title = "## 🧭 How This List Was Made"
        how = """- All 118 works were collected from X posts in the 48 hours after the 2026-11-09 release.
- Every work link was opened in a browser and confirmed to load; every video was watched or spot-checked.
- GIF previews (a few seconds each, muted, low-res) are recorded from the creator's own demo video or the live site.
- Press coverage, "now available on X" ads, tool repos and reshares were removed. Credit goes to the original creator; a resharer is noted only when the creator posted no link."""
        contrib_title = "## 🤝 Contributing"
        contrib = """Found one we missed? Open an [issue](../../issues/new) or a PR with the work link and the original post. The link must open directly and the work must be made with Fable 5.2. See [CONTRIBUTING.md](CONTRIBUTING.md).

Entries are added to [`data/works.json`](data/works.json) and both READMEs are regenerated from it."""
        lic_title = "## ⚖️ License & Disclaimer"
        lic = """All works belong to their creators. This repository only indexes them, keeping short low-res GIF previews and no full works or videos; watch the full video on the original post. Creators can ask for a preview or entry to be removed via an issue. Not affiliated with Anthropic.

Content in this repository is released under [CC0-1.0](LICENSE)."""
        credit = '<p align="right">Curated by <strong>Helium</strong> · Forked from <a href="https://github.com/fengyiqicoder/awesome-fable-5.2">awesome-fable-5.2</a></p>'
        count_suffix = "WORKS"
        anchor = {"游戏":"-games","3D 场景":"-3d-worlds--scenes","网页与工具":"-web-pages--tools","视频与动画（附源码）":"-animation--film-with-source","video-only":"-video-only-demos"}

    parts = [f'<div align="center">\n\n{banner}\n\n{tagline}\n\n{badges}\n\n</div>\n',
             intro1, forknote, intro2, gallery, "",
             news_title, news, "",
             toc_title, toc, "",
             "---\n",
             ml_title, ml_desc, "",
             table(most, lang), "",
             "---\n"]
    for sec, name, desc, items in secs:
        emoji = {"游戏":"🎮","3D 场景":"🌍","网页与工具":"🧰","视频与动画（附源码）":"🎬","video-only":"📺"}[sec]
        parts += [f'## {emoji} {name} · {len(items)}', desc, "", table(items, lang), "", "---\n"]
    parts += [related_title, related, "",
              how_title, how, "",
              contrib_title, contrib, "",
              lic_title, lic, "",
              credit, "",
              '[![Star History Chart](https://api.star-history.com/svg?repos=kingll2026/Helium-Claude-Fable-5.2&type=Date)](https://star-history.com/#kingll2026/Helium-Claude-Fable-5.2&Date)']
    (ROOT / path).write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {path}: {sum(len(s[3]) for s in secs)} entries")
