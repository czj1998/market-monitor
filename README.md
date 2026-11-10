# 美股全景监控与科创50 (588000) 决策终端

## 快速上手与 GitHub 部署指南

### 第一步：清空并上传到 GitHub
1. 打开你的 GitHub 仓库：https://github.com/czj1998/market-monitor
2. 如果仓库里有旧文件，先清空。
3. 点击 **Add file** -> **Upload files**，将解压包里的所有文件上传。
   * 注意：如果浏览器未上传隐藏的 `.github` 文件夹，请点击 **Add file** -> **Create new file**，文件名输入 `.github/workflows/deploy.yml`，然后将 `deploy_workflow_code.txt` 里的内容全选复制进去并保存即可！

### 第二步：开启仓库写入权限（必须！）
1. 进入仓库 **Settings** -> 左侧菜单 **Actions** -> **General**。
2. 页面滑到最底部 **Workflow permissions**，勾选 **Read and write permissions** 并点击 **Save** 保存。

### 第三步：开启 GitHub Pages 网页发布
1. 进入仓库 **Settings** -> 左侧菜单 **Pages**。
2. **Branch** 选择 `main` 分支，文件夹保持 `/ (root)`，点击 **Save** 保存。
3. 你的永久访问网址为：`https://czj1998.github.io/market-monitor/`

每天北京时间 07:30，GitHub 会全自动拉取最新美股行情、VIX、芯片龙头，并计算科创50开盘推演更新到网页！
