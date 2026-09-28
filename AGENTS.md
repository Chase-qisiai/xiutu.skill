# 修图 Skill 项目规则

## 提示词库与同步

- `提示词（未整理）.md` 是当前原始资料；在分类方案确认前，不移动、不重写其中的提示词。
- 项目根目录内的提示词库是唯一维护源；共享 Skill `~/.codex/skills/xiutu` 中的提示词库是运行副本。
- 新增、修改、删除或调整分类时，只先修改项目内维护源，然后运行同步流程，把变更同步到 `~/.codex/skills/xiutu`。
- 禁止只修改 Skill 副本而不回写项目维护源；同步完成后必须检查文件内容和版本/校验信息，确保两边一致。
- 如果维护源与 Skill 副本不一致，以项目维护源为准，并重新执行同步；不要手工拼接两边的差异。
- GitHub 公开仓库是本项目的发布镜像；本地验证通过后，再把 Skill 文件和提示词库变更提交并推送，禁止只在远端手工修改。

同步命令：

```bash
python3 scripts/sync_prompt_library.py \
  --source './提示词（未整理）.md'
```

同步后检查：

```bash
python3 scripts/sync_prompt_library.py \
  --source './提示词（未整理）.md' \
  --check
```

## Skill 名称

- 用户称呼为“修图 Skill / 修图.skill”；Codex 实际目录名使用 `xiutu`，即 `~/.codex/skills/xiutu`。
- “修图”和“xiutu”视为同一个 Skill，不创建两个分叉版本。
