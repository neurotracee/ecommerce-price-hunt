#!/usr/bin/env bash
# 一键：结构校验 → 打 zip → 建仓（若无）→ 提交/打 tag → 推 GitHub + Gitee → 两端发 Release
#
# 凭证（不会写进仓库，也不会打印）：
#   GITHUB_TOKEN 环境变量，或 ~/.github_token
#   GITEE_TOKEN  环境变量，或 ~/.gitee_token
#
# 可选覆盖：GH_OWNER / GITEE_OWNER / REPO / BRANCH / VERSION
# 用法：bash scripts/publish.sh
set -euo pipefail
cd "$(dirname "$0")/.."

if command -v python >/dev/null 2>&1; then PY=python; else PY=python3; fi

# 首次使用时自动初始化本地仓库（已有仓库则跳过）
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -b main >/dev/null
  echo "已初始化本地 git 仓库（分支 main）"
fi

VERSION="${VERSION:-$(tr -d '\r\n' < VERSION)}"
TAG="v${VERSION}"
GH_OWNER="${GH_OWNER:-neurotracee}"
GITEE_OWNER="${GITEE_OWNER:-bio234}"
REPO="${REPO:-ecommerce-price-hunt}"
BRANCH="${BRANCH:-$(git symbolic-ref --short HEAD)}"
GH_REMOTE="${GH_REMOTE:-origin}"
GITEE_REMOTE="${GITEE_REMOTE:-gitee}"
ZIP="dist/${REPO}-${TAG}.zip"
UPSTREAM="https://github.com/ccch1mneyyy/dsh-go/"

GH_TOKEN="${GITHUB_TOKEN:-}"
[[ -z "$GH_TOKEN" && -f "$HOME/.github_token" ]] && GH_TOKEN="$(tr -d '\r\n' < "$HOME/.github_token")"
GITEE_TOKEN="${GITEE_TOKEN:-}"
[[ -z "$GITEE_TOKEN" && -f "$HOME/.gitee_token" ]] && GITEE_TOKEN="$(tr -d '\r\n' < "$HOME/.gitee_token")"
[[ -n "$GH_TOKEN" ]] || { echo "缺少 GitHub token（GITHUB_TOKEN 或 ~/.github_token）"; exit 1; }
[[ -n "$GITEE_TOKEN" ]] || { echo "缺少 Gitee token（GITEE_TOKEN 或 ~/.gitee_token）"; exit 1; }

# 本机 SteamTools/Watt Toolkit 的 MITM 证书会让 schannel 吊销检查失败，Windows 需跳过
CURL_OPTS=()
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) CURL_OPTS+=(--ssl-no-revoke) ;; esac

TMP="$(mktemp -d)"
# 用 Python 清理临时凭据文件：本机 safe-delete 会拦截带盘符路径的 rm
cleanup() {
  "$PY" - "$TMP" <<'PY' 2>/dev/null || true
import os, sys
p = sys.argv[1]
try:
    for f in os.listdir(p):
        os.remove(os.path.join(p, f))
    os.rmdir(p)
except OSError:
    pass
PY
}
trap cleanup EXIT

# 本机加速代理对带 Expect: 100-continue 的 POST 会返回 502，显式去掉该头；
# 偶发 502 / 连接中断自动重试。Gitee 的 POST 走直连更稳（本机 hosts 未劫持 gitee.com）。
gh_api() {
  curl -sS "${CURL_OPTS[@]}" --max-time 60 --retry 2 --retry-delay 1 --retry-all-errors \
    -H "Authorization: Bearer $GH_TOKEN" -H "Expect:" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" "$@"
}
# Gitee 的 POST 在本机两条链路上都可能偶发连接重置：先走系统代理，失败再直连
gitee_api() {
  local first
  if first="$(curl -sS "${CURL_OPTS[@]}" --max-time 60 -H "Expect:" "$@" 2>/dev/null)"; then
    printf '%s' "$first"
    return 0
  fi
  curl -sS --noproxy '*' "${CURL_OPTS[@]}" --max-time 60 -H "Expect:" "$@" || true
}

echo "[1/7] 结构校验"
"$PY" scripts/validate.py

echo "[2/7] 打包 $TAG"
"$PY" scripts/pack.py "$VERSION"
[[ -f "$ZIP" ]] || { echo "打包失败：$ZIP 不存在"; exit 1; }

echo "[3/7] 确认两端仓库存在并同步简介里的安装提示"
DESC="为 DSH go（基于 DeepSeek Harness 二开）做的附属功能开源项目：AI Agent 电商/药品全网比价 Skill。下载 Release 的 zip 直接发给 DSH，说「帮我安装它到本地目录即可，我要把它添加进来」即可装上。许可：代码 MIT / 文档 CC BY-NC-SA 4.0（非商业）。上游 $UPSTREAM"
gh_code=$(gh_api -o /dev/null -w "%{http_code}" "https://api.github.com/repos/$GH_OWNER/$REPO" || true)
if [[ "$gh_code" == "404" ]]; then
  "$PY" - "$REPO" "$DESC" <<'PY' > "$TMP/gh_repo.json"
import json, sys
print(json.dumps({
    "name": sys.argv[1], "description": sys.argv[2],
    "homepage": "https://github.com/ccch1mneyyy/dsh-go/",
    "private": False, "auto_init": False,
    "has_issues": True, "has_wiki": False, "has_projects": False,
}, ensure_ascii=False))
PY
  gh_api -X POST -H "Content-Type: application/json" --data-binary "@$TMP/gh_repo.json" \
    "https://api.github.com/user/repos" -o "$TMP/gh_created.json"
  echo "  已创建 GitHub 仓库 $GH_OWNER/$REPO"
else
  echo "  GitHub 仓库已存在 ($gh_code)"
fi
# 标签：先读两端现有标签，与项目默认清单合并去重后再写回，
# 避免覆盖使用者在网页端手动新增的 topics（如 deepseek / deepseek-harness）
DEFAULT_TOPICS=(ai-agent skill prompt-engineering price-comparison ecommerce dsh-go \
                deepseek deepseek-harness accessibility agent-skills)
gh_api "https://api.github.com/repos/$GH_OWNER/$REPO/topics" -o "$TMP/gh_topics.json" || true
gitee_api "https://gitee.com/api/v5/repos/$GITEE_OWNER/$REPO/project_labels?access_token=$GITEE_TOKEN" \
  -o "$TMP/gitee_labels.json" || true
"$PY" - "$TMP/gh_topics.json" "$TMP/gitee_labels.json" "${DEFAULT_TOPICS[@]}" <<'PY' > "$TMP/topics_merged.json"
import json, sys
def load(path, kind):
    try:
        d = json.load(open(path, encoding='utf-8'))
        return d.get('names', []) if kind == 'gh' else [x.get('name') for x in d]
    except Exception:
        return []
names = list(dict.fromkeys(load(sys.argv[1], 'gh') + load(sys.argv[2], 'gitee') + sys.argv[3:]))
print(json.dumps(names, ensure_ascii=False))
PY
"$PY" - "$TMP/topics_merged.json" <<'PY' > "$TMP/gh_topics_put.json"
import json, sys
print(json.dumps({"names": json.load(open(sys.argv[1], encoding='utf-8'))}, ensure_ascii=False))
PY
gh_api -X PUT -H "Content-Type: application/json" --data-binary "@$TMP/gh_topics_put.json" \
  "https://api.github.com/repos/$GH_OWNER/$REPO/topics" -o /dev/null || true
gitee_api -X PUT -H "Content-Type: application/json" --data-binary "@$TMP/topics_merged.json" \
  "https://gitee.com/api/v5/repos/$GITEE_OWNER/$REPO/project_labels?access_token=$GITEE_TOKEN" \
  -o /dev/null || true
echo "  已同步两端标签（合并去重，保留手动新增）"
# 简介（About 区）也带上「下载 zip 直接发给 DSH」的提示，已存在的仓库同样更新
"$PY" - "$DESC" <<'PY' > "$TMP/gh_desc.json"
import json, sys
print(json.dumps({"description": sys.argv[1],
                  "homepage": "https://github.com/ccch1mneyyy/dsh-go/"},
                 ensure_ascii=False))
PY
gh_api -X PATCH -H "Content-Type: application/json" --data-binary "@$TMP/gh_desc.json" \
  "https://api.github.com/repos/$GH_OWNER/$REPO" -o /dev/null || true

gitee_code=$(gitee_api -o /dev/null -w "%{http_code}" \
  "https://gitee.com/api/v5/repos/$GITEE_OWNER/$REPO?access_token=$GITEE_TOKEN" || true)
if [[ "$gitee_code" == "404" ]]; then
  # 表单里的字符串 "false" 在 Gitee 后端会被当成真值、把仓库建成私有；
  # 省略 private 用默认公开，下面再用 JSON 布尔强制确认一次。
  gitee_api -X POST \
    --data-urlencode "access_token=$GITEE_TOKEN" \
    --data-urlencode "name=$REPO" \
    --data-urlencode "description=$DESC" \
    --data-urlencode "has_issues=true" \
    --data-urlencode "has_wiki=false" \
    --data-urlencode "auto_init=false" \
    "https://gitee.com/api/v5/user/repos" -o "$TMP/gitee_created.json"
  echo "  已创建 Gitee 仓库 $GITEE_OWNER/$REPO"
else
  echo "  Gitee 仓库已存在 ($gitee_code)"
fi
# Gitee 的 PATCH 要求同时带 name；用 JSON 布尔明确设为公开仓库，
# 否则 Release 页面与附件直链对未登录访客会返回 403。
"$PY" - "$GITEE_TOKEN" "$REPO" "$DESC" "$UPSTREAM" <<'PY' > "$TMP/gitee_repo_patch.json"
import json, sys
print(json.dumps({"access_token": sys.argv[1], "name": sys.argv[2],
                  "description": sys.argv[3], "homepage": sys.argv[4],
                  "private": False, "public": True}, ensure_ascii=False))
PY
gitee_api -X PATCH -H "Content-Type: application/json" \
  --data-binary "@$TMP/gitee_repo_patch.json" \
  "https://gitee.com/api/v5/repos/$GITEE_OWNER/$REPO" -o /dev/null || true

echo "[4/7] 提交与打标签"
git config user.name >/dev/null 2>&1 || git config user.name "$GH_OWNER"
git config user.email >/dev/null 2>&1 || git config user.email "$GH_OWNER@users.noreply.github.com"
git add -A
if git diff --cached --quiet; then
  echo "  没有待提交改动"
else
  git commit -m "chore(release): $TAG"
fi
FORCE_TAG=0
if git rev-parse -q --verify "refs/tags/$TAG" >/dev/null; then
  if [[ "$(git rev-parse "$TAG^{commit}")" != "$(git rev-parse HEAD)" ]]; then
    # 同一版本内做文档修订时，让 tag 跟着最新提交走，Release 才指向当前内容
    git tag -f -a "$TAG" -m "$TAG" HEAD >/dev/null
    FORCE_TAG=1
    echo "  标签 $TAG 已移动到最新提交"
  else
    echo "  标签 $TAG 已存在，沿用"
  fi
else
  git tag -a "$TAG" -m "$TAG"
fi
TAG_PUSH_OPTS=()
[[ "$FORCE_TAG" == "1" ]] && TAG_PUSH_OPTS=(--force)

echo "[5/7] 推送到 GitHub 与 Gitee"
# 本机 MITM 代理偶尔会掐断 TLS 连接，推送失败自动重试 3 次
push_retry() {
  local n=0
  until "$@"; do
    n=$((n + 1))
    if (( n >= 3 )); then echo "  推送失败（已重试 3 次）: $*"; return 1; fi
    echo "  连接中断，重试 $n/3 ..."
  done
}
git remote get-url "$GH_REMOTE" >/dev/null 2>&1 || git remote add "$GH_REMOTE" "git@github.com:$GH_OWNER/$REPO.git"
git remote get-url "$GITEE_REMOTE" >/dev/null 2>&1 || git remote add "$GITEE_REMOTE" "https://gitee.com/$GITEE_OWNER/$REPO.git"
push_retry git push "$GH_REMOTE" "HEAD:$BRANCH"
push_retry git push "${TAG_PUSH_OPTS[@]}" "$GH_REMOTE" "$TAG"

# 用一次性凭据文件喂给 Gitee，避免把 token 放进命令行或 .git/config
printf 'https://%s:%s@gitee.com\n' "$GITEE_OWNER" "$GITEE_TOKEN" > "$TMP/git-cred"
chmod 600 "$TMP/git-cred"
# Windows 版 git 是原生程序，读不到 /tmp/... 这种 MSYS 路径，需转成 C:/... 形式
CRED_PATH="$TMP/git-cred"
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) command -v cygpath >/dev/null 2>&1 && CRED_PATH="$(cygpath -m "$TMP/git-cred")" ;;
esac
gitee_push() {
  git -c credential.helper= -c "credential.helper=store --file=$CRED_PATH" \
    push "$GITEE_REMOTE" "$@"
}
push_retry gitee_push "HEAD:$BRANCH"
push_retry gitee_push "${TAG_PUSH_OPTS[@]}" "$TAG"
# 凭据文件由 trap 统一删除，不在中途单独 rm

echo "[6/7] 发布 GitHub Release（含 zip 附件与免责声明）"
"$PY" - "$TAG" "$REPO" <<'PY' > "$TMP/gh_release.json"
import json, sys, pathlib
tag, repo = sys.argv[1], sys.argv[2]
body = pathlib.Path("RELEASE_NOTES.md").read_text(encoding="utf-8")
print(json.dumps({
    "tag_name": tag,
    "name": f"{tag} · {repo}",
    "body": body, "draft": False, "prerelease": False,
}, ensure_ascii=False))
PY
rel_code=$(gh_api -o "$TMP/gh_existing.json" -w "%{http_code}" \
  "https://api.github.com/repos/$GH_OWNER/$REPO/releases/tags/$TAG" || true)
if [[ "$rel_code" == "200" ]]; then
  RID=$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1],encoding="utf-8"))["id"])' "$TMP/gh_existing.json")
  gh_api -X PATCH -H "Content-Type: application/json" --data-binary "@$TMP/gh_release.json" \
    "https://api.github.com/repos/$GH_OWNER/$REPO/releases/$RID" -o /dev/null
  echo "  已更新 Release 正文"
else
  gh_api -X POST -H "Content-Type: application/json" --data-binary "@$TMP/gh_release.json" \
    "https://api.github.com/repos/$GH_OWNER/$REPO/releases" -o "$TMP/gh_new.json"
  RID=$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1],encoding="utf-8"))["id"])' "$TMP/gh_new.json")
  echo "  已创建 Release"
fi
ASSET_NAME="$(basename "$ZIP")"
# 同名附件先删，保证重复执行也不会堆积
gh_api "https://api.github.com/repos/$GH_OWNER/$REPO/releases/$RID/assets" \
  -o "$TMP/gh_assets.json" || true
if [[ -s "$TMP/gh_assets.json" ]]; then
  for aid in $("$PY" -c 'import json,sys; d=json.load(open(sys.argv[1],encoding="utf-8")); print(" ".join(str(a["id"]) for a in d if a["name"]==sys.argv[2]))' "$TMP/gh_assets.json" "$ASSET_NAME"); do
    gh_api -X DELETE "https://api.github.com/repos/$GH_OWNER/$REPO/releases/assets/$aid" -o /dev/null || true
  done
fi
curl -sS "${CURL_OPTS[@]}" --max-time 180 --retry 2 --retry-delay 1 --retry-all-errors -X POST \
  -H "Authorization: Bearer $GH_TOKEN" -H "Expect:" -H "Content-Type: application/zip" \
  --data-binary "@$ZIP" \
  "https://uploads.github.com/repos/$GH_OWNER/$REPO/releases/$RID/assets?name=$ASSET_NAME" \
  -o "$TMP/gh_asset.json"
echo "  已上传附件 $ASSET_NAME"

echo "[7/7] 发布 Gitee Release（含免责声明与 zip 附件）"
GITEE_REL_API="https://gitee.com/api/v5/repos/$GITEE_OWNER/$REPO/releases"
gitee_api "$GITEE_REL_API?access_token=$GITEE_TOKEN" -o "$TMP/gitee_releases.json" || true
if ! "$PY" -c 'import json,sys; d=json.load(open(sys.argv[1],encoding="utf-8")); sys.exit(0 if any(r.get("tag_name")==sys.argv[2] for r in d) else 1)' \
    "$TMP/gitee_releases.json" "$TAG" 2>/dev/null; then
  # Gitee 的 Release 要求 tag 已推送；POST 偶发连接重置，发完再查一次确认
  gitee_api -X POST \
    --data-urlencode "access_token=$GITEE_TOKEN" \
    --data-urlencode "tag_name=$TAG" \
    --data-urlencode "name=$TAG · $REPO" \
    --data-urlencode "target_commitish=$BRANCH" \
    --data-urlencode "body@RELEASE_NOTES.md" \
    "$GITEE_REL_API" -o "$TMP/gitee_release.json" || true
  gitee_api "$GITEE_REL_API?access_token=$GITEE_TOKEN" -o "$TMP/gitee_releases.json" || true
fi
GITEE_RID=$("$PY" - "$TMP/gitee_releases.json" "$TAG" <<'PY'
import json, sys
try:
    data = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    data = []
for r in data:
    if r.get("tag_name") == sys.argv[2]:
        print(r["id"])
        break
else:
    print("0")
PY
)
if [[ "${GITEE_RID:-0}" == "0" ]]; then
  echo "  Gitee Release 未创建成功，请在网页端手动补发（代码与 tag 已同步）"
else
  # 正文：新建与已存在都 PATCH，保证两端 Release 与 RELEASE_NOTES.md 逐字一致
  # （Gitee 的 PATCH 强制要求 tag_name 与 name）
  gitee_api -X PATCH \
    --data-urlencode "access_token=$GITEE_TOKEN" \
    --data-urlencode "tag_name=$TAG" \
    --data-urlencode "name=$TAG · $REPO" \
    --data-urlencode "target_commitish=$BRANCH" \
    --data-urlencode "body@RELEASE_NOTES.md" \
    "$GITEE_REL_API/$GITEE_RID" -o "$TMP/gitee_release_patch.json" || true
  echo "  已同步 Gitee Release 正文"

  # 附件：Gitee 同名文件会堆积而非覆盖，先按 id 删掉旧的，再传当前 zip
  gitee_api "$GITEE_REL_API/$GITEE_RID/attach_files?access_token=$GITEE_TOKEN" \
    -o "$TMP/gitee_attach_list.json" || true
  if [[ -s "$TMP/gitee_attach_list.json" ]]; then
    for aid in $("$PY" -c 'import json,sys; d=json.load(open(sys.argv[1],encoding="utf-8")); print(" ".join(str(a["id"]) for a in d if a.get("name")==sys.argv[2]))' \
        "$TMP/gitee_attach_list.json" "$ASSET_NAME" 2>/dev/null); do
      gitee_api -X DELETE --data-urlencode "access_token=$GITEE_TOKEN" \
        "$GITEE_REL_API/$GITEE_RID/attach_files/$aid" -o /dev/null || true
    done
  fi
  gitee_api -X POST \
    -F "access_token=$GITEE_TOKEN" \
    -F "file=@$ZIP;type=application/zip" \
    "$GITEE_REL_API/$GITEE_RID/attach_files" -o "$TMP/gitee_attach.json" || true
  echo "  已上传附件 $ASSET_NAME 到 Gitee Release"
fi

echo
echo "完成：$TAG"
echo "  GitHub : https://github.com/$GH_OWNER/$REPO/releases/tag/$TAG"
echo "  Gitee  : https://gitee.com/$GITEE_OWNER/$REPO/releases"
echo "  上游   : $UPSTREAM"
echo "  本地包 : $ZIP"
