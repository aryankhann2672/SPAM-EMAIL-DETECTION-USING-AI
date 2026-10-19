"""Single-command runner to launch both Backend (FastAPI) and Frontend (Vite) concurrently."""

from pathlib import Path
import subprocess
import sys
import threading
import time
import webbrowser

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / 'frontend'


def open_browser_after_delay() -> None:
    """Wait 2.5 seconds for servers to initialize, then launch the browser."""
    time.sleep(2.5)
    print('\n[RUNNER] 🌐 Opening browser at http://localhost:5173 ...\n')
    try:
        webbrowser.open('http://localhost:5173')
    except Exception:
        pass


def main() -> None:
    print('=' * 65)
    print('  🛡️  SpamShield AI - Unified Development Runner')
    print('=' * 65)
    print('[RUNNER] Starting FastAPI backend and React frontend concurrently...\n')

    # 1. Command for Backend
    backend_cmd = [
        sys.executable,
        '-m',
        'uvicorn',
        'app.main:app',
        '--app-dir',
        'backend',
        '--reload',
        '--port',
        '8000',
    ]

    # 2. Command for Frontend (on Windows use npm.cmd)
    npm_executable = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    frontend_cmd = [npm_executable, 'run', 'dev']

    backend_proc = None
    frontend_proc = None

    try:
        # Launch Backend Process
        print('[RUNNER] ⚡ Starting FastAPI on http://localhost:8000')
        backend_proc = subprocess.Popen(
            backend_cmd,
            cwd=str(ROOT_DIR),
        )

        # Launch Frontend Process
        print('[RUNNER] ⚡ Starting Vite frontend on http://localhost:5173')
        frontend_proc = subprocess.Popen(
            frontend_cmd,
            cwd=str(FRONTEND_DIR),
        )

        # Schedule automatic browser launch in background thread
        threading.Thread(target=open_browser_after_delay, daemon=True).start()

        print('\n' + '-' * 65)
        print('  Press Ctrl + C anytime in this terminal to STOP BOTH services.')
        print('-' * 65 + '\n')

        # Monitor both processes
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print('\n[RUNNER] ⚠️ Backend process exited.')
                break
            if frontend_proc.poll() is not None:
                print('\n[RUNNER] ⚠️ Frontend process exited.')
                break

    except KeyboardInterrupt:
        print('\n[RUNNER] 🛑 Received Ctrl+C. Shutting down all services...')

    finally:
        # Gracefully kill child process trees
        for name, proc in [('Backend', backend_proc), ('Frontend', frontend_proc)]:
            if proc and proc.poll() is None:
                try:
                    if sys.platform == 'win32':
                        subprocess.run(
                            ['taskkill', '/F', '/T', '/PID', str(proc.pid)],
                            capture_output=True,
                            check=False,
                        )
                    else:
                        proc.terminate()
                except Exception:
                    pass
        print('[RUNNER] ✅ Both services stopped cleanly.')


if __name__ == '__main__':
    main()
