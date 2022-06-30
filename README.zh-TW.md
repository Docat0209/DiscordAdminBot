
[English](README.md) | 繁體中文

# Discord 管理機器人

這個機器人是設計用來自動管理你的伺服器

你只需要輸入一些簡單的指令便能讓你的伺服器煥然一新

這個機器人適合那些不會管理Discord伺服器的人或是想要更簡單管理伺服器的人


![Logo](https://download.logo.wine/logo/Discord_(software)/Discord_(software)-Logo.wine.png)


## 截圖

![App Screenshot](https://media.discordapp.net/attachments/986465905582161970/991900345531904030/unknown.png)


## 功能

- 動態身分組
- 全自動語音擴展
- 投票
- 隨機分組
- 事件計數器


## 安裝

安裝 python

https://www.python.org/downloads/


透過pip安裝 discord.py

```bash
  pip install discord.py
```

透過pip安裝 emoji

```bash
  pip install emoji
```

透過pip安裝 alive-progress

```bash
  pip install alive-progress
```
## 環境變數

要運行此項目，您需要將以下環境變量添加到`config.py`文件中

`API_KEY`

## 如何啟用

設定完`config.py`之後開啟`server.bat`，便能在Discord上開始使用此機器人了

## 指令/範例

### 注意事項

`*('參數1' '參數2')` 代表你可以重複輸入多組參數在指令裡

`(需要回復訊息)` 代表你需要回復一則訊息才能使用此指令

你可以使用伺服器自訂義表情在指令裡

### 動態身分組

指令

```bash
  &reaction_role *('表情' '@身分組') (需要回復訊息)
```

範例

```bash
  &reaction_role :rocket: @身分組1 :ok_hand: @身分組2
```

### 投票

指令

```bash
  &vote '問題' '小時' *('表情' '選項內容')
```

範例

```bash
  &vote "星期六 或 星期日" 24 *(:ringed_planet: "星期六" :sunny: "星期日")
```

### 隨機分組

指令

```bash
  &random_team *('@使用者 或 字串')
```

範例

```bash
  &random_team @使用者1 @使用者2 @使用者3 @使用者4 @使用者5 @使用者6
```

### 事件計數器

指令

```bash
  &event_host '標題' '目標人數' '小時'
```

範例

```bash
  &event_host "星期日午餐烤肉趴" 10 48
```

## 未來規劃

- 保資料移動到資料庫

- 新增更多功能

- 支援英文

## 更新優化

- 更新 README 檔案

