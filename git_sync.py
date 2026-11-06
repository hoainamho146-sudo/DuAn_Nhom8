#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOOL TỰ ĐỘNG ĐỒNG BỘ GIT (AUTO PULL - MERGE - RESOLVE - PUSH)
Dành cho Nhóm 8 - Tránh xung đột code (Merge Conflicts)
"""

import os
import sys
import subprocess
import datetime
import re

# Màu sắc hiển thị Terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def log_info(msg):
    print(f"{BLUE}[INFO]{RESET} {msg}")

def log_success(msg):
    print(f"{GREEN}[SUCCESS]{RESET} {msg}")

def log_warn(msg):
    print(f"{YELLOW}[CẢNH BÁO]{RESET} {msg}")

def log_error(msg):
    print(f"{RED}[LỖI]{RESET} {msg}")

def run_cmd(cmd, check=False):
    """Thực thi lệnh shell và trả về (status, stdout, stderr)"""
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def get_current_branch():
    code, out, _ = run_cmd("git rev-parse --abbrev-ref HEAD")
    return out if code == 0 else "main"

def has_local_changes():
    code, out, _ = run_cmd("git status --porcelain")
    return len(out) > 0

def get_conflicted_files():
    code, out, _ = run_cmd("git diff --name-only --diff-filter=U")
    if code == 0 and out:
        return [f.strip() for f in out.splitlines() if f.strip()]
    
    # Kiểm tra thêm status
    code, out, _ = run_cmd("git status --porcelain")
    conflicts = []
    for line in out.splitlines():
        if line.startswith("UU ") or line.startswith("AA ") or line.startswith("UD ") or line.startswith("DU "):
            conflicts.append(line[3:].strip())
    return conflicts

def resolve_modify_delete_conflicts():
    """Tự động xử lý khi 1 bên xóa file còn mình sửa file (như index.html)"""
    code, out, _ = run_cmd("git status --porcelain")
    resolved = False
    for line in out.splitlines():
        # UD: ta sửa, remote xóa; DU: ta xóa, remote sửa
        if line.startswith("UD ") or "deleted by them" in line.lower():
            fname = line.split()[-1]
            log_warn(f"Phát hiện file '{fname}' bị xóa trên GitHub nhưng có code của bạn. Đang giữ lại code của bạn...")
            run_cmd(f"git add '{fname}'")
            resolved = True
        elif line.startswith("DU ") or "deleted by us" in line.lower():
            fname = line.split()[-1]
            log_warn(f"File '{fname}' bị remote sửa nhưng bạn xóa. Đang chấp nhận file từ remote...")
            run_cmd(f"git checkout --theirs '{fname}' && git add '{fname}'")
            resolved = True
    return resolved

def auto_fix_conflict_in_file(filepath, strategy="ours"):
    """
    Tự động xử lý conflict marker (<<<<<<<, =======, >>>>>>>)
    strategy:
      - 'ours': Giữ code của mình
      - 'theirs': Giữ code của đồng đội trên GitHub
      - 'union': Giữ cả code của mình và đồng đội
    """
    if not os.path.exists(filepath):
        return False

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if "<<<<<<<" not in content or "=======" not in content or ">>>>>>>" not in content:
            return False

        # Pattern nhận diện conflict block
        pattern = re.compile(r'<<<<<<<[^\n]*\n(.*?)=======\n(.*?)>>>>>>>[^\n]*\n', re.DOTALL)

        def replacer(match):
            ours_code = match.group(1)
            theirs_code = match.group(2)
            if strategy == "ours":
                return ours_code
            elif strategy == "theirs":
                return theirs_code
            elif strategy == "union":
                return ours_code + "\n" + theirs_code
            return match.group(0)

        new_content = pattern.sub(replacer, content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        run_cmd(f"git add '{filepath}'")
        return True
    except Exception as e:
        log_error(f"Không thể tự sửa file {filepath}: {e}")
        return False

def smart_sync(commit_msg=None, default_strategy="ours"):
    print(f"\n{BOLD}{CYAN}===================================================={RESET}")
    print(f"{BOLD}{CYAN}   🚀 TOOL TỰ ĐỘNG SYNC GIT (PULL & PUSH AN TOÀN)   {RESET}")
    print(f"{BOLD}{CYAN}===================================================={RESET}\n")

    branch = get_current_branch()
    log_info(f"Đang làm việc trên branch: {BOLD}{branch}{RESET}")

    # BƯỚC 1: Tự động commit code hiện tại nếu có thay đổi
    if has_local_changes():
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        if not commit_msg:
            commit_msg = f"Update TV2 - {now_str}"

        log_info(f"Đang lưu (commit) code cục bộ: \"{commit_msg}\"...")
        run_cmd("git add .")
        code, out, err = run_cmd(f'git commit -m "{commit_msg}"')
        if code == 0:
            log_success("Đã commit code cục bộ thành công.")
        else:
            log_warn(f"Thông báo commit: {out or err}")
    else:
        log_info("Không có thay đổi mới ở máy bạn cần commit.")

    # BƯỚC 2: Kéo code mới nhất từ GitHub về (Pull)
    log_info("Đang kiểm tra và tải code mới từ GitHub (git pull)...")
    
    # Dùng git pull với cờ merge thông thường
    code, out, err = run_cmd(f"git pull origin {branch} --no-rebase")

    if code == 0:
        log_success("Tải và gộp code thành công! Không có xung đột nào.")
    else:
        log_warn("Phát hiện xung đột (conflict) giữa code của bạn và đồng đội!")
        log_info("Đang tự động phân tích và khắc phục...")

        # Xử lý trường hợp Modify/Delete
        resolve_modify_delete_conflicts()

        # Tìm các file đang bị conflict
        conflicts = get_conflicted_files()
        
        if conflicts:
            log_warn(f"Các file bị xung đột: {', '.join(conflicts)}")
            for f in conflicts:
                log_info(f"Đang tự động xử lý file: {f} (Ưu tiên giữ code: {default_strategy})...")
                auto_fix_conflict_in_file(f, strategy=default_strategy)

            # Hoàn tất merge commit
            log_info("Đang hoàn thành gộp code...")
            run_cmd("git add .")
            run_cmd('git commit -m "chore: auto resolve merge conflicts"')
            log_success("Đã tự động xử lý toàn bộ xung đột!")
        else:
            # Nếu không có conflict file nào hoặc chỉ là delete
            run_cmd("git add .")
            run_cmd('git commit -m "chore: sync with remote"')

    # BƯỚC 3: Đẩy code lên GitHub (Push)
    log_info("Đang đẩy code đã gộp lên GitHub (git push)...")
    code, out, err = run_cmd(f"git push origin {branch}")

    if code == 0:
        print(f"\n{BOLD}{GREEN}🎉 TẤT CẢ ĐÃ XONG! Code của bạn và đồng đội đã được đồng bộ an toàn lên GitHub.{RESET}\n")
    else:
        log_warn(f"Push lần 1 chưa thành công: {err}")
        log_info("Đang thử lại pull lần cuối trước khi push...")
        run_cmd(f"git pull origin {branch}")
        code2, out2, err2 = run_cmd(f"git push origin {branch}")
        if code2 == 0:
            print(f"\n{BOLD}{GREEN}🎉 TẤT CẢ ĐÃ XONG! Đã push thành công lên GitHub.{RESET}\n")
        else:
            log_error(f"Không thể push: {err2}")
            log_info("Gợi ý: Kiểm tra lại quyền hạn hoặc đăng nhập Git.")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else None
    strat = sys.argv[2] if len(sys.argv) > 2 else "ours"
    smart_sync(commit_msg=msg, default_strategy=strat)
