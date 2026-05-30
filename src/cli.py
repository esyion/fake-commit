"""CLI 入口模块"""
from datetime import date, datetime
from pathlib import Path

import click
from pydantic import ValidationError

from .config import Settings
from .git_client import GitClient


@click.command()
@click.option("--author-name", "-n", required=True, help="Git 提交用户名")
@click.option("--author-email", "-e", required=True, help="Git 提交邮箱")
@click.option("--start-date", "-s", default=None, help="开始日期 (YYYY-MM-DD)")
@click.option("--end-date", "-d", default=None, help="结束日期 (YYYY-MM-DD)")
@click.option("--commits-per-day", "-c", default=1, type=int, help="每天提交次数")
@click.option("--branch", "-b", default="main", help="分支名")
@click.option("--random-mode", is_flag=True, help="启用随机提交模式")
@click.option("--random-range", default="1,10", help="随机区间，格式 'min,max'")
@click.option("--repo", "-r", default=".", help="仓库路径")
def cli(
    author_name: str,
    author_email: str,
    start_date: str | None,
    end_date: str | None,
    commits_per_day: int,
    branch: str,
    random_mode: bool,
    random_range: str,
    repo: str,
) -> int:
    """生成假 git 提交历史的 CLI 工具"""
    try:
        # 解析日期
        start = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else date(2026, 1, 1)
        end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else date(2026, 1, 31)

        config = Settings(
            author_name=author_name,
            author_email=author_email,
            start_date=start,
            end_date=end,
            commits_per_day=commits_per_day,
            branch=branch,
            random_mode=random_mode,
            random_range=random_range,
        )

        repo_path = Path(repo)
        click.echo("开始生成提交历史...")
        click.echo(f"作者: {config.author_name} <{config.author_email}>")
        click.echo(f"日期范围: {config.start_date} - {config.end_date}")
        click.echo(f"仓库: {repo_path.absolute()}")

        client = GitClient(config, repo_path)
        count = client.run()

        click.echo(f"完成！共生成 {count} 次提交")
        return 0

    except ValidationError as e:
        click.echo(f"错误: 配置无效 - {e}", err=True)
        return 1
    except FileNotFoundError as e:
        click.echo(f"错误: 仓库路径不存在 - {e}", err=True)
        return 1
    except RuntimeError as e:
        click.echo(f"错误: Git 操作失败 - {e}", err=True)
        return 1
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        return 1
