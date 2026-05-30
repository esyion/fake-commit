"""Git 操作封装模块"""
import os
import subprocess
from datetime import date, datetime
from pathlib import Path

from .config import Settings


class GitClient:
    """Git 操作客户端"""

    def __init__(self, config: Settings):
        self.config = config
        self.repo_path = config.repo_path

    def _run_git(self, *args: str) -> subprocess.CompletedProcess:
        """执行 git 命令"""
        cmd = ["git", "-C", str(self.repo_path)] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Git error: {result.stderr}")
        return result

    def init_repo(self) -> None:
        """初始化 git 仓库"""
        if not (self.repo_path / ".git").exists():
            self._run_git("init")
            self._run_git("checkout", "-b", self.config.branch)
        else:
            # 确保在正确的分支
            self._run_git("checkout", self.config.branch)

    def setup_author(self) -> None:
        """设置 git 作者信息"""
        os.environ["GIT_AUTHOR_NAME"] = self.config.author_name
        os.environ["GIT_AUTHOR_EMAIL"] = self.config.author_email
        os.environ["GIT_COMMITTER_NAME"] = self.config.author_name
        os.environ["GIT_COMMITTER_EMAIL"] = self.config.author_email

    def commit(self, message: str, commit_date: date) -> None:
        """创建提交"""
        author_date = f"{commit_date.isoformat()} {self.config.hour}:00:00"
        os.environ["GIT_AUTHOR_DATE"] = author_date
        os.environ["GIT_COMMITTER_DATE"] = author_date

        # 确保有文件变更
        marker_file = self.repo_path / ".commit_marker"
        marker_file.write_text(f"{message}\n")

        self._run_git("add", ".")

        result = subprocess.run(
            ["git", "-C", str(self.repo_path), "commit", "-m", message],
            capture_output=True,
            text=True,
            env={**os.environ, "GIT_AUTHOR_DATE": author_date, "GIT_COMMITTER_DATE": author_date},
        )
        if result.returncode != 0:
            raise RuntimeError(f"Commit failed: {result.stderr}")

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
            for _ in range(self.config.commits_per_day):
                message = self.config.format_commit_message(commit_date)
                self.commit(message, commit_date)
                total_commits += 1

        return total_commits