# update_file.py
import shutil
from pathlib import Path
from typing import Dict


def update_file(file_path: str,
                   rules: Dict[str, str],
                   *,
                   backup: bool = False,
                   log_print: bool = True) -> None:
    """
    原地修改 *.py 文件。
    :param file_path:  目标 python 文件
    :param rules:      {行头标识: 替换整行内容} 的字典
                       只要某行以“行头标识”开头（strip 后），就把整行替换成“替换内容”
    :param backup:     是否生成 .bak 备份文件，默认 False
    :param log_print:  是否打印替换详情，默认 True
    """
    file_path = Path(file_path).expanduser().resolve()
    if not file_path.is_file():
        raise FileNotFoundError(file_path)

    # 备份
    if backup:
        shutil.copy(file_path, file_path.with_suffix(file_path.suffix + '.bak'))

    lines = file_path.read_text(encoding='utf-8').splitlines()
    new_lines, hit_flags = [], {k: False for k in rules}

    for lineno, line in enumerate(lines, 1):
        stripped = line.lstrip()
        matched = False
        for head, new_line in rules.items():
            if stripped.startswith(head):
                hit_flags[head] = True
                matched = True
                if log_print:
                    print(f'[replace L{lineno}] {line!r} -> {new_line!r}')
                new_lines.append(new_line)
                break
        if not matched:
            new_lines.append(line)

    # 打印未匹配到的规则
    if log_print:
        for head, hit in hit_flags.items():
            if not hit:
                print(f'[warn] 未匹配到行头标识: {head!r}')

    # 写回
    file_path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    if log_print:
        print(f'[info] 已更新 {file_path}')


# 简单 CLI 演示（可直接当脚本用）
if __name__ == '__main__':
    import json, sys

    if len(sys.argv) != 3:
        print('用法: python update_py_file.py  target.py  \'{"行头标识": "替换整行"}\'')
        sys.exit(1)

    py_file = sys.argv[1]
    rules = json.loads(sys.argv[2])
    update_file(py_file, rules)  # 默认 backup=False, log_print=True