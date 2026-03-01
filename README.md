<div align="center">

![astrbot_plugin_endfield](https://socialify.git.ci/bvzrays/astrbot_plugin_endfield/image?description=1&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit+Board&pulls=1&stargazers=1&theme=Dark)

# astrbot_plugin_endfield-点亮⭐！

<img src="resources/img/ET logo.svg" width="200" />

基于[森空岛 API](https://skland.com) 及 [终末地协议终端](https://end.shallow.ink) 的 AstrBot **终末地** 插件 · 绑定 / 便签 / 干员面板 / 抽卡分析 / 签到

</div>

## 🛠️ 安装与配置

1. 在 AstrBot 插件管理器中搜索 `astrbot_plugin_endfield` 并安装。
2. 确保在系统环境中已安装并正确配置浏览器依赖以供 Playwright 渲染：`playwright install chromium`
3. 插件配置项（按需设置）：
   - `api_key`：请前往 [协议终端](https://end.shallow.ink) 获取。
   - `auth_client_name`：网页授权登录时的显示名称（默认：`终末地机器人`）
   - `operator_list_bg`：干员列表背景图选择（`random`, `bg1.png`, `bg2.png`）
   - `render_timeout`：单次图片渲染的全局超时限制（毫秒）。

---

## 📂 文件结构与实现

<img width="639" alt="image" src="https://github.com/user-attachments/assets/c653513c-963b-4e53-b961-8a9367f60341" />

### 项目目录
- `main.py`: **插件入口**。负责 AstrBot 指令过滤、权限校验及各模块逻辑编排。
- `core/`: **核心逻辑组件**。
    - `client.py`: API 异步客户端，封装了森空岛与浅墨的所有网络请求逻辑。
    - `user.py`: 用户数据中心，管理账号绑定关系与抽卡分析状态。
    - `render.py`: 渲染助手，基于 HTML 模板的图形化输出封装。
- `data/`: **持久化存储**。使用 local JSON 存储用户的绑定令牌。
- `resources/`: **视觉资产与模板**。
    - `cache/`: 并发下载器缓存目录，存储预处理后的干员立绘与头像。
    - `operator/`, `gacha/`, `stamina/`, `help/`: 采用 **Jinja2** 编写的动态 HTML 模板。
- `_conf_schema.json`: 插件 WebUI 配置项 schema 定义。
- `metadata.yaml`: 记录版本号、作者、仓库等插件元数据。

---

## 🎮 功能一览

| 指令前缀：`/` (或自定义) | 说明 |
| :--- | :--- |
| **基础功能** | |
| `zmd` | 打开帮助菜单 |
| **账号与绑定** | |
| `授权登陆` | 通过森空岛网页进行安全授权登录 |
| `扫码绑定` | 扫描二维码快捷登录 |
| `手机绑定 [手机号]` | 接收验证码登录（不可用） |
| `绑定列表` | 查看当前所有已绑定的账号状态 |
| `切换绑定 [序号]` | 切换当前主账号 |
| `删除绑定 [序号]` | 删除指定账号绑定 |
| **数据查询 (渲染图)** | |
| `便签` | 查询账号数据总览 |
| `理智/订阅理智` | 查询当前理智、日常活跃度、回满时间/自动满值推送 |
| `干员列表` | 查询当前持有的干员图鉴及等级 |
| `<干员名>面板` | 查询单个干员的当前面板（不可用） |
| `抽卡记录` | 查询近期抽卡历史记录 |
| `抽卡分析` | 生成全卡池抽卡数据统计分析图 |
| `签到` | 执行所有账号的森空岛每日签到，每日自动 |
| `日历` | 查看活动版本日历图（自动获取Wiki横幅） |
| `帝江号建设` | 查询基础建设进度 |
| `地区建设` | 查询地区开发进度 |
| `公告/订阅公告` | 获取官方公告列表及推送 |

---

## 🖼️ 功能截图

| `便签` | `理智` |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/d9c07469-f00d-42c2-820a-f46402adf714" width="400"> | <img src="https://github.com/user-attachments/assets/0a723c50-d81d-444f-932e-32918a0ee2ed" width="400"> |

| `干员列表` | `抽卡分析` |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/3355b411-215a-4bf9-b536-e67804e8d122" width="400"> | <img src="https://github.com/user-attachments/assets/5e86a76b-0d06-4f7b-97fc-6b914f57efb3" width="200"> <img src="https://github.com/user-attachments/assets/17d09d14-ad26-4499-8201-ddbcc72acda6" width="100"> |

| `抽卡记录` | `帝江号建设` |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/aacab909-6a04-467a-aeaf-a525558e1ddb" width="400"> | <img src="https://github.com/user-attachments/assets/df71bbdf-febb-4f00-95ba-157f5788629f" width="400"> |

| `地区建设` | `公告` |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/cf3b53b9-fa78-4b71-b682-9077dfafc3c1" width="400"> | <img src="https://github.com/user-attachments/assets/99da9389-1326-487c-b11e-d526d0e251fb" width="400"> |

| `日历` |
| :---: |
| <img src="https://github.com/user-attachments/assets/b3dbe4c9-d916-4abd-aeee-a434a43d4c0f" width="600"> |

---

## 🎨 资源自定义 (背景与头像修改)

你可以通过替换插件目录中的资源文件来自定义生成的渲染图片样式：
路径：`AstrBot/data/plugins/astrbot_plugin_endfield/resources/`

- **理智图背景**：放入 `resources/img/stbg.png`
- **干员列表背景**：放入 `resources/operator/img/opbg.png`
- **随机干员立绘/头像**：放入 `resources/img/operator/` 文件夹下
  - 在生成 `/理智` 图时，系统会默认在此文件夹下随机抽取图片作为右侧展示。支持 `png`, `jpg`, `webp` 格式。

---

## 📝 TODO (后续计划)

- [x] **终末地信息查询** (`帝江号建设`, `地区建设`, `订阅理智`, `日历`)
- [x] **公告系统** (官方公告列表及推送)
- [ ] **抽卡辅助** (全服抽卡统计、模拟抽卡)
- [ ] **Wiki 百科增强** (装备、战术物品、武器百科)
- [ ] **攻略模块** (角色/地图攻略图)
- [ ] **MaaEnd 远程控制** (MaaEnd Client 远程控制与状态监控)
- [ ] **管理员功能** (全员自动签到、强制同步数据)

---

## 💡 常见问题排查

1. 是否已执行 `playwright install chromium` 确保无头浏览器正常。
2. 若图片卡死、发生 500 报错，可进入 `render_cache/` 检查本地渲染情况。

## 📜 更新日志

### 1.6.0 (2026-03-01)
- 新增 `/日历`：支持自动爬取 Wiki 长条横幅背景
- 优化日历布局，增加理智、绑定列表 UI 细节
- 自动签到功能与订阅理智功能（待测试）

### 1.5.0 (2026-03-01)
- 新增 `/帝江号建设`、`/地区建设`
- 重构信赖与心情展示，增加 `短尺背景.png`

## 1.4.0 (2026-02-28)
- 新增官方公告列表渲染功能 (`/公告`)
- 新增官方单条公告详情提取及渲染功能 (`/公告 <序号>`, `/公告最新`)
- 支持了图片动态填充
  
## 1.3.0 (2026-02-27)
- 抽卡分析重构：移除 5 星标记
- 优化渲染稳定性：Playwright 导航超时增加至 30s

## 1.2.0 (2026-02-27)
- 抽卡分析异步化优化
- 便签面板UI重绘
- 干员列表UI修复
- 帮助菜单重绘为图片（`zmd` 指令）
- 优化了图片请求并发逻辑

## 1.1.0 (2026-02-26)
- 修复了理智查询问题
- 增加了干员列表功能
---

## 🤝 鸣谢

本项目参考自 Yunzai 插件 [endfield-plugin](https://github.com/Entropy-Increase-Team/endfield-plugin)。
- 感谢：[@QingYingX](https://github.com/QingYingX) 与 [@浅巷墨黎](https://github.com/dnyo666)
- 感谢 [终末地协议终端](https://end.shallow.ink) 提供的底层封装。

> [!TIP]
> 终末地-协议终端 交流群：[160759479](https://qm.qq.com/q/zZXruW6V4Q)
> astrbot 移植版作者反馈群：[870543663](https://qm.qq.com/q/kPxQZy5gg8)
