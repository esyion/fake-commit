"""Git 操作封装模块"""
import os
import subprocess
import uuid
from datetime import date
from pathlib import Path

from .config import Settings


class GitClient:
    """Git 操作客户端"""

    def __init__(self, config: Settings):
        self.config = config
        self.repo_path = config.REPO_PATH

    def _run_git(self, *args: str) -> subprocess.CompletedProcess:
        """执行 git 命令"""
        cmd = ["git", "-C", str(self.repo_path)] + list(args)
        result = subprocess.run(cmd,  capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Git error: {result.stderr}")
        return result

    def init_repo(self) -> None:
        """初始化 git 仓库"""
        if not (self.repo_path / ".git").exists():
            self._run_git("init")
            self._run_git("checkout", "-b", self.config.branch)
        else:
            # 检查分支是否存在，不存在则创建
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "rev-parse", "--verify", f"refs/heads/{self.config.branch}"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                self._run_git("checkout", self.config.branch)
            else:
                self._run_git("checkout", "-b", self.config.branch)

    def setup_author(self) -> None:
        """设置 git 作者信息"""
        self._run_git("config", "user.name", self.config.author_name)
        self._run_git("config", "user.email", self.config.author_email)

    def commit(self, message: str, commit_date: date) -> None:
        """创建提交"""
        author_date = f"{commit_date.isoformat()} {self.config.hour}:00:00"

        # 确保有文件变更（每次内容不同，添加 UUID）
        marker_file = self.repo_path / ".commit_marker"
        marker_file.write_text(f"{message} | {uuid.uuid4()}\n")

        self._run_git("add", ".")

        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": self.config.author_name,
            "GIT_AUTHOR_EMAIL": self.config.author_email,
            "GIT_COMMITTER_NAME": self.config.author_name,
            "GIT_COMMITTER_EMAIL": self.config.author_email,
            "GIT_AUTHOR_DATE": author_date,
            "GIT_COMMITTER_DATE": author_date,
        }
        result = subprocess.run(
            ["git", "-C", str(self.repo_path), "commit", "-m", message],
            capture_output=True,
            text=True,
            env=env,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Commit failed: {result.stderr or result.stdout}")

    def get_commit_count(self) -> int:
        """获取提交数量"""
        result = self._run_git("rev-list", "--count", "HEAD")
        return int(result.stdout.strip())

    def run(self) -> int:
        """执行提交生成"""
        self.setup_author()
        self.init_repo()

        total_commits = 0
        for commit_date in self.config.get_date_range():
            commits_count = self.config.get_commits_per_day()
            for _ in range(commits_count):
                message = self.config.format_commit_message(commit_date)
                self.commit(message, commit_date)
                total_commits += 1
        self._run_git("push", "-u", "origin2", self.config.branch)
        return total_commits