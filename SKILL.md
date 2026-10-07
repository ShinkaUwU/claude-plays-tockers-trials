---
name: tft-play
description: Play Teamfight Tactics (TFT) Set 18 "Tocker's Trials" (发条鸟的试炼) PvE mode on Windows with desktop control (computer use). Includes a reliable mouse/keyboard input script, UI coordinates, how to field/bench units and pick up loot, common pitfalls (focus stealing, resolution switching, right-clicks being ignored), and comp/economy experience. Use when the user asks to play TFT / 云顶之弈 / Tocker's Trials, or to click, drag, buy or sell champions in TFT.
---

# Playing Teamfight Tactics (TFT) with desktop control

## 0. Setup

0. **Before the game starts, read `strategy.md` (the comp, leveling schedule and item rules to follow) and `s18-reference.md` in this directory** (cost / traits / role of every S18 champion, plus trait breakpoints). Use it to identify shop and board units instead of hovering each one; only look things up in game for unfamiliar mechanics. When the set changes, regenerate it from Community Dragon data (`https://raw.communitydragon.org/latest/cdragon/tft/en_us.json`, the matching entry in `setData`).
1. Load the computer-use tools. In `request_access`, request all of these at once:
   - `Teamfight Tactics`, `League of Legends` (launchers)
   - The game window process: `tfttencentclient-win64-shipping.exe` on the Chinese (Tencent) server, `tftclient-win64-shipping.exe` on the international (English) client. Requesting a name that doesn't exist makes the whole `request_access` fail, so take a screenshot first and read the hidden process names before requesting.
   - `leagueclientux.exe`, `riot client.exe` (client / end-of-game screens)
2. **Do not use computer-use's own clicks to play the game**: the game window is often treated as "desktop shell in the foreground" and clicks are rejected, and the game does not register its right-clicks. Still use computer-use `screenshot` / `zoom` for looking.
3. Send all input through this skill's script (any Python 3, `py -3`; use `python` if the `py` launcher is missing):

```bash
py -3 "<skill dir>/scripts/tft.py" "CMD ; CMD ; ..."
```

| Command | Effect |
|---|---|
| `r X Y [ms]` | Right press-hold-release (move the Little Legend, open unit info). Hold 150–400 ms |
| `l X Y [ms]` | Left click (buy units, buttons, pick augments/items) |
| `d X1 Y1 X2 Y2` | Left drag (position units, equip items, open anvils, sell units) |
| `dh X1 Y1 X2 Y2 MS` | Drag, then hover over the target for MS ms before releasing (Sprykin rider, Taric pairing: use 2000) |
| `m X Y` | Hover (item / trait tooltips) |
| `k w` | Key press; hover a unit and press `w` = field / bench it |
| `w MS` | Wait |
| `fit` | Stretch the game window's client area over the whole screen |
| `info` | Print screen size, game window position, whether it is in the foreground |

All coordinates are in the **1456×819 screenshot frame** (what `screenshot` reports when the game fills the screen); the script maps them onto the game window's client area. `fg_is_tft True` at the end of the output means the game is in the foreground and input took effect.

## 1. Common pitfalls (read first)

- **Before starting, ask the user to close/minimize the Claude window** so the game owns the full screen. A Claude window floating over the game blocks clicks in that area and steals focus (symptoms: `fg_is_tft False`, clicks that sometimes work, info panels that won't close).
- **Focus stealing**: the Claude desktop app grabs the foreground, and a background window receives no input (right-click moves and clicks all do nothing). The script forces the game to the foreground before every command; if the output says `fg_is_tft False`, run it again.
- **Resolution switching**: the game switches between exclusive fullscreen (2560×1440) and desktop resolution (3840×2160); afterwards the window may be shrunk into the top-left corner (client area 3200×1800). If a screenshot shows the game not filling the screen, run `tft.py "fit"` and screenshot again. The game leaves fullscreen whenever it loses focus (becomes a ~1323×723 window; screenshots are mostly black or show the game in a corner). The script now auto-`fit`s on every run (`autofit`), so whenever a screenshot looks wrong, run any command (e.g. `info`) and screenshot again.
- **Right-clicks on loot / units get "swallowed"**: right-clicking directly on a coin or orb often does nothing. Instead, right-click **empty ground next to the target**, then right-click on the far side so the Little Legend walks through it. If an orb/coin lies on your own unit, drag the unit away first.
- Right-clicking a unit opens its info panel, which covers the right side; left-click empty space (e.g. 1200,450) to close it.
- Dragging an item onto an invalid target shows an "item is invalid on this target" message (e.g. the Alpha Mark only works on Riftbeast units).
- **The whole game has a hard 90-minute cap (most important)**: individual rounds have no timer, but 90 minutes after entering the match the server ends the game (`TFT.log` in `%LOCALAPPDATA%\TFT\Saved\Logs\` shows `updated phase from Gameplay to Idle after 5400668ms`, and `TFTEoGStats.json` has `gameLengthSeconds≈5405`), no matter how many lives are left. All 30 rounds must fit in 90 minutes: **≤3 minutes per round on average (combat is ~40 s, so ≤2 minutes of planning)**. Record the start time (or read the UTC time on the first lines of TFT.log); 1-10 must end by minute 30 and 2-10 by minute 60. If behind, drop optional inspections. Ways to go faster: put pickup + buy + reroll in one command; use `scale 0.5` screenshots for routine checks; don't hover shop cards you can recognize; hover items only once before combining/assigning; don't walk back and forth for a single coin.
- **Never press Esc**: it opens the settings menu (which contains Surrender / Quit). Close settings with the X at top right (1119,124). Close info panels by right-clicking empty ground.
- **SendInput mouse moves may be rejected** (returns 0, error 87) while key events work. The script positions the cursor with `SetCursorPos`; if clicks stop working, hover with `m X Y` first and confirm a highlight before clicking.
- **Orbs in the enemy half can be picked up too**: the Little Legend can walk into the enemy half. Collect every "?" orb and coin on either side.
- **Units/items cannot be placed in the enemy half**: dropping into the enemy half or into the gap between hexes fails (the unit snaps back; items show the invalid-target message). While holding a unit with the left button, your hexes are highlighted — **always drop on the center of one of your hexes**. The front row at y≈320–335 is right against the midline; err downward (toward your side), never upward. y=305 is already the enemy half, so never use a front-row target with y < 325. Always screenshot after dragging to confirm the unit actually landed.
- **When swapping a board unit with a bench unit, drag onto the board unit's feet (the center of the hex it stands on), not the center of its model.** Models are drawn above their hex; dropping on the model's body lands on another hex or a gap and the swap silently fails. Feet are about 25–35 px below the model's center, e.g. a front-row body at y≈300 → target y≈330. Even so, **never put "swap + sell bench slot X" in one command**: if the swap fails, the sell hits the wrong unit (e.g. the card you just bought). Correct order: sell the outgoing board unit (drag it to the shop, or hover + `k w` to bench it), screenshot to confirm, then drag the new unit into the freed hex.
- **A second Blackthorn unit automatically creates a blood-pool hex**: with Blackthorn 2 active, a dark-red blood-pool hex appears on your side; whoever stands on it is the sacrifice and does not fight. After fielding Blackthorn units (e.g. Azir + Malphite), always `zoom` to check that no carry is standing on the pool, and move them off if so.
- When picking up orbs in the enemy half, keep the right-click target away from enemy units, or it opens the enemy's info panel (breaking the "don't inspect enemies" rule) and the Little Legend can't walk there. Targets less than ~60 px from an enemy tend to hit it: `zoom` first to mark enemy positions and keep targets at least 70 px from enemy models — take an extra step if needed.
- **Coins often scatter among your own units** (5–15 gold per round in stages 2–3; opened orbs also spray coins): flat golden ovals are coins; vertical yellow light pillars next to units are just effects. A right-click target on a hex occupied by your own unit opens its info panel instead of walking, so use **centers of empty hexes** (row 2, y≈393, is usually empty) or empty ground in the enemy half as waypoints, so the Little Legend's straight path crosses the coins. If an orb sits on your own unit, drag the unit to an empty hex, right-click its old hex to pick the orb up, then drag the unit back — works first try.

## 2. UI coordinates (1456×819 screenshot frame, game filling the screen)

| Element | Coordinates |
|---|---|
| Fight button | (1185, 763) |
| Buy XP | (255, 730) |
| Reroll shop | (255, 785) |
| 5 shop slots | x = 412 / 565 / 718 / 870 / 1022, y = 750 |
| Bench (9 slot centers) | y = 596, x = 326 / 414 / 501 / 588 / 676 / 764 / 852 / 941 / 1028 |
| Item bench (left column) | x = 22, y ≈ 213 / 253 / 293 / 333 / 373 / 413 / 453 … (+40 per slot) |
| Your board | 4 rows × 7 hexes; centers in the "board hex centers" table below |
| Augment (pick 1 of 3) | card centers x ≈ 420 / 727 / 1035, y ≈ 420 |
| Anvil / forge options | y ≈ 715; 5 options (completed-item anvil, item shop) x = 327 / 527 / 727 / 928 / 1129; 4 options (component anvil, artifact forge) x = 426 / 627 / 828 / 1029 |
| Sell a unit | drag it onto the shop area (700, 760) |
| Open an anvil | drag the anvil from the bench onto the shop area (640, 760) |

**Your board hex centers** (the blue hexes shown while holding a unit; converted from the user's 2000×1125 screenshot by ×0.728). Always use these centers — i.e. the unit's "feet" — as drag targets for positioning/swapping, never the model's center:

| Row (counting from the midline toward you) | y | Hexes 1–7 x (left to right) |
|---|---|---|
| Row 1 (front, at the midline) | 337 | 428 / 515 / 601 / 688 / 775 / 861 / 949 |
| Row 2 | 393 | 464 / 553 / 643 / 732 / 822 / 911 / 1001 |
| Row 3 | 450 | 407 / 499 / 592 / 684 / 777 / 869 / 962 |
| Row 4 (back) | 512 | 441 / 538 / 635 / 731 / 828 / 925 / 1022 |

The top edge of row 1 is at about y=309; above that is the enemy half. Models are drawn above their hex — a unit's body is roughly 30 px above its hex center — so when you see a body in a screenshot, drag to the nearest hex center below it.

> Layout shifts slightly between resolutions; **screenshot before each action**, and `zoom` when needed.
> Before buying, count which slot the card is in and convert to x (slots 1–5 = 412 / 565 / 718 / 870 / 1022).

## 3. Basic routines

- **Field / bench**: hover the unit + `k w`; or drag a bench unit onto a board unit's **feet** (its hex center, not its model center) to swap; then left-drag to reposition.
- **Inspect a unit**: `r X Y 150`, then `zoom` the right info panel (815,15)-(1005,560).
- **Inspect an item**: hover with `m 22 Y`, then `zoom` the top-left area.
- **Buy a unit**: `l <shop x> 750`; a ★★ / ★★★ marker on a shop card means buying it upgrades the unit.
- **Each round**: screenshot → pick up orbs and coins → check new items/units → combine items, upgrade, position → decide whether to buy XP (no rerolls before level 8) and sell unneeded bench units → buy XP / reroll → **write the lineup checklist (below) and save it to the state file** → click Fight → `computer_batch` wait 35–45 s, then screenshot.
- **Before clicking Fight every round, write a lineup checklist in the reply** — no checklist, no Fight:
  ```
  Round X-Y | Level L (units a/b) | Gold G | Lives N
  Board: unit ★ [item1/item2/item3] position (front/back/sacrifice hex/rider) …
  Bench: unit ★ [items] — why it stays (copies needed for next star / who it replaces next round); sell it if there's no reason
  Item bench: …
  Main tank: unit [items] | AD carry: unit [items] | AP carry: unit [items]
  Active traits: trait n (tier) …
  Self-check: ① any duplicate units on board (duplicates count once for traits and waste a slot — replace them) ② all slots used ③ items concentrated on carries/main tank ④ any bench unit without a reason ⑤ manual traits (sacrifice hex, rider, etc.) set up ⑥ ranged backline units in row 4, not row 3
  ```
  Write the full checklist every round; to save time, copy the previous round's and change only the lines that changed — never drop it. Verify stars and items with the right-click info panel, not from memory. Check this list before buying too: **never buy a shop card for a unit that is already 2★ on board/bench unless you are going for its 3★** (at level 7+, 1–2 cost 3★s are nearly impossible; only chase a 3★ if it is the core carry and you already hold 7–8 copies). Conversely, **any final-comp card that isn't 2★ yet must be bought whenever it shows up** (see `strategy.md`).
- **Field new units immediately**: when a duplicator upgrades a unit, a planned card is bought, or leveling adds a slot, field it in the same command, replacing the weakest unit on the board, then screenshot to confirm.
- **Positioning**: tanks and melee units go in row 1 (front). **Ranged backline units (marksmen, casters) go in row 4 (back, y=512), not row 3** — row 3 is in range of enemy melee and splash; only use row 3 when row 4 is full.
- Stage-3 strength reference: 3-6 is a big wave (10+ enemies with 3 items each). A board where only the main tank and two carries hold items loses to it; give extra completed items to other units once the main tank and carries are full.
- **State file (protection against lost context)**: old screenshots get removed from context during the game (shown as `[media removed: request limit]`) and long conversations are auto-summarized; you cannot choose which screenshots stay. So the game state must not live only in screenshots and memory:
  - At game start, create `game_state.md` in the scratchpad directory. First line: start time (the `Pending to Gameplay` time in TFT.log), the 90-minute deadline, and the 1-10 / 2-10 time checkpoints.
  - **Before clicking Fight every round, overwrite the file with the full lineup checklist using Write** (round, level/slots, gold, lives, board, bench, item bench, main tank / carry items, traits, this round's buys/sells and to-dos such as "field X next round", "1 more Draven needed"). Append one line with the round result (won/lost, lives left) to a "History" section.
  - At the start of each round, read the file before taking a screenshot and verify the board against it, not memory. Whenever context has been compressed or you're unsure of the state, read the file first.
- Screenshot budget: routine checks at `scale 0.5–0.6`; only `zoom` the needed area for the shop, item bench and info panel; put multiple coin-pickup moves in one command and screenshot once at the end.
- Batch actions in one command (`;`-separated) with ~`w 500` waits in between.

## 4. Tocker's Trials (S18) experience

### The fixed strategy lives in `strategy.md`

The comp (priority cards and their replacements), leveling schedule, rolling/wand rules and item assignment are in **`strategy.md`** in this directory. Read it before the game; it has the highest priority. Edit that file to play a different comp.

- **Don't inspect enemy units**: no right-clicking enemies, no hovering enemy items — just build your own board. Saves time (90-minute game cap).

- There are **3 stages**, 10 rounds each (1-1…1-10, 2-1…); you start with 3 lives and lose one per lost round.
- Enemy strength rises sharply by stage: from stage 2 enemies carry several completed items, and you need a formed 2–3★ board.
- **Economy principles**:
  - **Interest exists**: at round end you get +1 gold per 10 gold saved (cap as shown in game; the scoreboard shows "Gold Interest"). Think before spending; try to sit at 10/20/30/40/50, don't spend down to 0–2 every round.
  - **Don't hoard junk on the bench**: keep only pairs toward 2★, the unit you will field next, and Alpha Mark / duplicator targets. Sell the rest for gold. A 3★ needs 9 copies — don't hoard 1★s for it.
  - **Choose leveling or rolling, not both**: either stay low (level 5–6), save interest and slow-roll 1–2 costs to 3★, or level fast to 7/8 and play 2★ 3–4 costs. The higher your level, the fewer 1-costs in the shop; leveling while rolling for 1-cost 3★s gets neither.
- Orbs give items, champions, free rerolls, anvils, duplicators, Alpha Marks, etc. — collect them all every round. Coins often lie in a vertical line; walk from one end to the other to grab them all.
- Use **duplicators** (Tiny / Champion Duplicator) on core units you want to star up; give the **Alpha Mark** to a Riftbeast unit (e.g. Krug, Scuttlecrab, Mama Beak).
- The **Golden Item Remover** has unlimited uses — strip items off when changing comps and give them to the new core.
- Concentrate items on a few core units (carries + main tank); don't spread them.
- Gold mostly comes from orbs/augments (but **interest exists**, see economy principles).
- **Shop wands (S18 unique mechanic)**: a random wand appears at the right end of the shop (the ornate card in slot 5). Patterns:
  - **One wand per round**: until you buy a wand, one appears **every two shop refreshes** (both the automatic refresh at round start and manual rerolls count). Once you buy one, no further wand appears that round no matter how much you reroll. So when the strategy says "buy a wand every round", stop rolling for wands once you've bought one.
  - A wand **covers a champion card**: buying the wand reveals the card beneath; if you go into combat without buying it, the wand disappears and also reveals the card. **In both cases, take a new screenshot (zoom the shop) to see whether the revealed card is one you want** — don't act on your memory of the shop before the wand was bought.
  - Read each wand's text in the shop (zoom slot 5) rather than relying on its name. A wand that grants champions may drop them in an orb on the board — walk over to pick it up. If a wand's text says it sacrifices allies, don't buy it; leave that decision to the user.
- Each augment card has a reroll button below it (416/727/1038, 652), one use per card. On the international client, left-clicking an augment card applies it immediately and closes the screen — no confirm click needed.
- **XP required per level** (measured in this mode): 1→2 2, 2→3 2, 3→4 6, 4→5 10, 5→6 20, 6→7 36, 7→8 60, 8→9 68, 9→10 68. You get +2 XP per round automatically. Use this table when costing a level-up, not the normal-mode numbers.
- **Taric pairing**: `dh <ally's feet> <on Taric> 2000` (drag the ally onto Taric, hold 2 seconds, release); on success an orange tether appears between them. The pairing persists after Taric stars up; to change partners, repeat with the new ally.
- Fielding Ivern makes purple Greenfather hexes appear on the board (units standing on them get a bonus).
- The blue bubble on the Little Legend is its own effect, not an orb.
- Elder Dragon takes 2 slots; free 2 slots before fielding it, or you get "This unit requires 2 team slots!".
Some S18 traits only work after a manual action — if you don't do it, the trait is effectively off:
- The "Evolve" pick-one-of-four (Evolve Rapidfire/Spellweaver/Executioner/Ravager) comes from **Kha'Zix's Rival trait**, not a fixed event at 3-2: Kha'Zix stacks on takedowns, and at enough stacks you choose a trait he **permanently gains** (counts toward trait totals); more stacks evolve him again for another trait. To get it, field Kha'Zix early where he can take part in kills, with only 1 Rival on board (no Rengar unless Rival 2). Pick the trait that reaches a new tier and helps the carry.
- **After picking an augment / Evolve, don't click (722,793) again**: the confirm button overlaps shop slot 3, and once the screen closes that click buys the slot-3 card. After choosing, screenshot to confirm the screen is still open before clicking confirm.
- The **Golden Item Remover** dragged onto a unit returns all its items to the item bench; use it repeatedly to reassign items. Hover the item-bench slot before equipping to confirm what it is — don't guess by position. After each use the remover moves to the end of the item bench and returned items are inserted before it, so when stripping two units in a row, hover again to find the remover the second time.
- Three kinds of duplicators: Tiny Champion Duplicator (1-costs only), Lesser Champion Duplicator (≤3-cost), Champion Duplicator (any cost). Holding 2 copies of a 5-cost, a Champion Duplicator makes it 2★ immediately.
- Thief's Gloves take all 3 item slots and can only go on a unit with no items.
- Lux (Avatar) shows her origin directly on the shop card; that origin counts as 2, so it can jump a tier at once (e.g. Blossom 5 → 7).
- The column of golden pods on the left edge of the board is Tocker's progress decoration, not an anvil/orb — don't click it; anvils appear on the bench.
- After winning the final boss at 3-10, the game ends straight back to the client (no results screen). Verify the result: `grep -n "TacticianVictory\|gameLengthSeconds" "$LOCALAPPDATA/TFT/Saved/Logs/TFT.log"`; `ffaStanding:1` plus `health>0` means cleared. Don't click "Skip waiting for stats / start next game" in the client.
For Draven's Bounty Seeker quests, **don't pick "deal XX damage in a single combat"** quests (single-combat damage thresholds are the hardest); pick cumulative damage, attack count or cast count quests. Draven's quests (60 attacks / 6 casts) complete quickly and reward a random 5-cost and two random 4-costs. Interest caps at 5 (at 50 gold) — spend anything above 50. If an orb lies on your own unit's hex, right-clicking opens the unit's info instead of walking; click an empty spot on the extension of the line from the Little Legend through the orb so it walks through the unit and picks up the orb.

## 5. After the game

- After the game you're back in the client; computer-use clicks work in the `leagueclientux.exe` window (the client responds to left-clicks normally).
- Don't start a new game on your own; report the result to the user first.
- **Don't put game records in these md files** (no per-game logs, dates, results, comps, augments, final units or items, no "in game N…" anecdotes) — they only make the files longer. Only add general, reusable rules: UI coordinates, operating pitfalls, game mechanics, and new rules distilled from mistakes, written as the rule itself.
