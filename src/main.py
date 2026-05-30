"""fake-commit 入口点"""

from .cli import cli


def main() -> int:
    """主函数 - 委托给 Click CLI"""
    return cli.main()
