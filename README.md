# tft-play — a Claude Code skill that plays TFT Tocker's Trials

[中文说明见下方](#中文说明)

A [Claude Code](https://claude.com/claude-code) skill that lets Claude play the **Teamfight Tactics Set 18 "Tocker's Trials" PvE mode** on Windows: it reads the game from screenshots (computer use) and sends mouse/keyboard input through a small Python script.

> ## ⚠️ Read this first: account risk
>
> **Riot Games' Terms of Service prohibit automation programs.** Section 7.1 of the [Riot Terms of Service](https://www.riotgames.com/en/terms-of-service) lists, among prohibited conduct, using "unauthorized third party programs, including mods, hacks, cheats, scripts, bots, trainers and automation programs that interact with the Riot Services in any way". Riot's [third-party applications policy](https://support.riotgames.com/en-us/riot/events/third-party-applications) applies to Teamfight Tactics, names "taking actions on your behalf (botting or scripting)" as not allowed, and says penalties range up to permanent suspension. Penalties under the Terms include account suspension or termination and hardware bans. The China server (operated by Tencent) also bans scripts that play the game for you.
>
> This project is exactly such an automation program. Therefore:
>
> - **Never use it in matches against real players** (Normal, Ranked, Hyper Roll, Double Up, or any other PvP queue). That would hurt other players and is the clearest kind of violation.
> - **Even in the PvE mode it was written for, using it is a risk.** Neither Riot's Terms nor its third-party policy makes an exception for PvE, co-op or bot modes. Your account may be suspended or banned.
> - If you run it, use an account you are prepared to lose, at your own risk. The author takes no responsibility for any penalty.
>
> The project is shared for research and education on AI agents and computer use: how a model can plan, act and learn rules from its own mistakes in a real-time desktop app. It is not a tool for gaining an advantage over other players.

## What it does

- Plays a full Tocker's Trials run (3 stages × 10 rounds, 3 lives, 90-minute hard cap) following a fixed comp and leveling plan.
- Uses computer-use screenshots and zooms only to **see** the game; all **input** goes through `scripts/tft.py`, because the game often ignores synthetic clicks from the computer-use tool.
- Keeps a per-game state file so the plan survives context compaction, and writes a lineup checklist before every fight.

It does not read game memory, intercept network traffic or modify game files. It only sends ordinary mouse and keyboard events and reads screenshots and the game's own log file. That does **not** make it allowed (see the warning above).

## Related work

To our knowledge (searched October 2026 across the web, GitHub, YouTube, Bilibili, Reddit and arXiv), this is the first public record of a general-purpose LLM clearing Tocker's Trials **on its own**, seeing the game only through screenshots and acting through mouse/keyboard input with no human executing its moves. Private or poorly indexed attempts may exist. Closest existing work:

- **LLM as advisor, a human plays**: [ChatGPT plays Teamfight Tactics](https://christianyoder.substack.com/p/chatgpt-plays-teamfight-tactics) (GPT-4.1 / o4-mini in PvP lobbies, state read from memory, the author executed the moves); coach tools such as [TFT-Copilot](https://github.com/RookieCLY/TFT-Copilot), [tft-ai-advisor](https://github.com/DaftPunnk/tft-ai-advisor) and [TFT_Agent](https://github.com/minhnhb1304/TFT_Agent).
- **Rule-based automation, no LLM**: [TFT-Hextech-Helper](https://github.com/WJZ-P/TFT-Hextech-Helper) (OpenCV/OCR AFK script that supports Tocker's Trials among other modes).
- **Reinforcement learning in a simulator**: [TFT_GOAT](https://github.com/MielPopsssssss/TFT_GOAT), [TFTMuZeroAgent](https://github.com/Lobotuerk/TFTMuZeroAgent).

What differs here: the agent is fully autonomous in the real client, and its rules were distilled from its own mistakes and written back into the skill files between games.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The skill itself: setup, pitfalls, UI coordinates, per-round routine, mode mechanics |
| `strategy.md` | The comp, leveling schedule, rolling and item rules. **Edit this file to play a different comp**; nothing else depends on it |
| `s18-reference.md` | Set 18 champion costs / traits / roles and trait breakpoints (from Community Dragon data) |
| `scripts/tft.py` | Windows input helper: clicks, drags, hover, keys, window fitting, in a fixed 1456×819 coordinate frame |

## Requirements

- **Windows only**: the input script uses the Windows API through `ctypes`.
- **A 16:9 screen**: all coordinates were measured on 16:9 displays. On 16:10 or ultrawide screens the shop, bench and board positions may not line up, and you will need to re-measure them in `SKILL.md`.
- The TFT client in English (international) or Chinese (CN server).
- Any Python 3 (the skill calls `py -3`; use `python` if you don't have the `py` launcher). Only the standard library is used.
- **Claude Code with computer-use tools available.** The skill sees the game only through screenshots; without computer use it cannot play. On first run Claude will ask you to grant access to the game and client windows.
- **Set 18 only** for the champion data and comp: after a set change, regenerate `s18-reference.md` and edit `strategy.md`. The input script, pitfalls and routine mostly carry over.
- A strong model: a full clear took about 79 minutes of the 90-minute cap with Claude Opus 5.5; weaker or slower models may run out of time or lose.

## Install

Clone it into your Claude Code skills folder (or `<project>/.claude/skills/tft-play/` for a single project):

```bash
git clone https://github.com/ShinkaUwU/claude-plays-tockers-trials.git ~/.claude/skills/tft-play
```

Then start Tocker's Trials in the TFT client and ask Claude to play it. Claude will not start a new game on its own after one finishes.

## Disclaimer

tft-play isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, Teamfight Tactics and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

This software is provided "as is", without warranty of any kind. You are solely responsible for complying with the terms of any game you use it with and for any consequences to your accounts.

---

## 中文说明

这是一个 [Claude Code](https://claude.com/claude-code) skill，让 Claude 在 Windows 上通过截图（computer use）看游戏、用一个 Python 脚本发送鼠标键盘输入，来玩**云顶之弈 S18「发条鸟的试炼」（Tocker's Trials）PvE 模式**。

> ## ⚠️ 使用前必读：封号风险
>
> **Riot Games 的服务条款明确禁止自动化程序。**[Riot 服务条款](https://www.riotgames.com/en/terms-of-service)第 7.1 条把“使用任何未经授权、以任何方式与 Riot 服务交互的第三方程序，包括模组、外挂、作弊器、脚本、机器人、修改器和自动化程序”列为违规行为，处罚包括封停或删除账号、封禁硬件。Riot 的[第三方应用政策](https://support.riotgames.com/en-us/riot/events/third-party-applications)同样适用于云顶之弈，明确不允许“代替玩家操作（挂机或脚本）”，严重时永久封号。国服（腾讯运营）同样禁止代替玩家操作游戏的脚本。
>
> 本项目就属于这类自动化程序，所以：
>
> - **绝对不要在有真人玩家的对局中使用**（匹配、排位、狂暴模式、双人作战等任何 PvP 模式）。这会损害其他玩家的体验，也是最明确的违规。
> - **即使在本项目针对的 PvE 模式中使用，也有封号风险。** Riot 的条款和第三方政策都没有为 PvE、合作或人机模式开例外。
> - 如果要运行，请使用你能接受被封的账号，风险自负。作者不对任何处罚负责。
>
> 本项目仅用于 AI agent / computer use 的研究和学习：展示模型如何在实时桌面应用中规划、操作，并从自己的失误中总结规则。它不是用来对其他玩家取得优势的工具。

### 功能

- 按固定阵容和升级节奏打完整局发条鸟的试炼（3 个阶段 × 10 回合，3 条命，整局 90 分钟上限）。
- computer use 只负责截图和放大**看**游戏；所有**输入**都走 `scripts/tft.py`，因为游戏经常不响应 computer use 自带的点击。
- 每局维护一个状态文件，防止上下文被压缩后丢失局面；每回合开战前写阵容清单。

本项目不读取游戏内存、不拦截网络通信、不修改游戏文件，只发送普通的鼠标键盘事件、读取截图和游戏自己的日志文件。但这**不代表它是被允许的**（见上面的警告）。

### 相关工作

据我们所知（2026 年 10 月在网页、GitHub、YouTube、B 站、Reddit、arXiv 上检索），这是第一个公开记录的、由通用大模型**自主**通关发条鸟的试炼的项目：只通过截图看游戏、通过键鼠输入操作，没有人代为执行。可能存在未公开或未被收录的尝试。最接近的已有工作：

- **大模型给建议、人来操作**：[ChatGPT plays Teamfight Tactics](https://christianyoder.substack.com/p/chatgpt-plays-teamfight-tactics)（GPT-4.1 / o4-mini 打真人对局，读内存获取局面，由作者代为操作）；教练类工具如 [TFT-Copilot](https://github.com/RookieCLY/TFT-Copilot)、[tft-ai-advisor](https://github.com/DaftPunnk/tft-ai-advisor)、[TFT_Agent](https://github.com/minhnhb1304/TFT_Agent)。
- **基于规则的挂机脚本，不用大模型**：[TFT-Hextech-Helper](https://github.com/WJZ-P/TFT-Hextech-Helper)（OpenCV/OCR 视觉识别，支持发条鸟的试炼等模式）。
- **在模拟器里做强化学习**：[TFT_GOAT](https://github.com/MielPopsssssss/TFT_GOAT)、[TFTMuZeroAgent](https://github.com/Lobotuerk/TFTMuZeroAgent)。

本项目的不同之处：在真实客户端中完全自主操作；规则是模型从自己的失误中总结出来、在对局之间写回 skill 文件的。

### 文件

| 文件 | 作用 |
|---|---|
| `SKILL.md` | skill 主体：准备、常见坑、界面坐标、每回合流程、模式机制 |
| `strategy.md` | 阵容、升级节奏、D 牌和装备规则。**想换阵容只改这个文件**，其他文件不依赖它 |
| `s18-reference.md` | S18 英雄费用/羁绊/定位和羁绊档位（来自 Community Dragon 数据） |
| `scripts/tft.py` | Windows 输入脚本：点击、拖拽、悬停、按键、窗口铺满，统一使用 1456×819 坐标系 |

### 环境要求

- **仅支持 Windows**：输入脚本通过 `ctypes` 调用 Windows API。
- **16:9 屏幕**：所有坐标都在 16:9 屏幕上测得。16:10 或带鱼屏上商店、备战席、棋盘的位置可能对不上，需要自己在 `SKILL.md` 里重新测量。
- 云顶之弈客户端为英文（国际服）或中文（国服）。
- 任意 Python 3（skill 调用 `py -3`；没有 `py` 启动器就用 `python`），只用标准库。
- **Claude Code 里要有 computer use 工具。** skill 只靠截图看游戏，没有 computer use 就玩不了。第一次运行时 Claude 会请求访问游戏和客户端窗口的权限。
- **英雄资料和阵容只适用于 S18**：换赛季后需要重新生成 `s18-reference.md`、修改 `strategy.md`；输入脚本、常见坑和每回合流程基本通用。
- 模型要够强：用 Claude Opus 5.5 通关一整局约 79 分钟，离 90 分钟上限不远；更弱或更慢的模型可能打不完或打不过。

### 安装

克隆到 Claude Code 的 skills 目录（只给单个项目用的话，放到 `<项目>/.claude/skills/tft-play/`）：

```bash
git clone https://github.com/ShinkaUwU/claude-plays-tockers-trials.git ~/.claude/skills/tft-play
```

然后在客户端里进入发条鸟的试炼，让 Claude 来玩。一局结束后 Claude 不会自己开下一局。

### 免责声明

本项目未获得 Riot Games 认可，不代表 Riot Games 或任何官方参与制作、管理 Riot Games 相关产品的人员的观点。Riot Games、云顶之弈（Teamfight Tactics）及所有相关内容均为 Riot Games, Inc. 的商标或注册商标。

本软件按“现状”提供，不附带任何形式的担保。是否遵守所用游戏的条款、以及账号因此受到的任何后果，均由使用者自行负责。
