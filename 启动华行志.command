#!/bin/zsh

setopt NO_BG_NICE

PROJECT_DIR="${0:A:h}"
PORT="8766"
URL="http://127.0.0.1:${PORT}/"

cd "$PROJECT_DIR" || exit 1

if /usr/bin/curl -fsS "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
  /usr/bin/open "$URL"
  exit 0
fi

echo "正在启动华行志，请稍候……"
LOG_FILE="$PROJECT_DIR/.china-travel-kit.log"
nohup python3 -m china_travel_kit serve --host 127.0.0.1 --port "$PORT" >"$LOG_FILE" 2>&1 < /dev/null &
SERVER_PID=$!

for attempt in {1..30}; do
  if /usr/bin/curl -fsS "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
    /usr/bin/open "$URL"
    echo "查询版已打开。现在可以关闭这个窗口，查询服务会继续运行。"
    sleep 1
    exit 0
  fi
  sleep 0.1
done

echo "启动失败，请确认电脑已安装 Python 3，且 8766 端口没有被其他程序占用。"
echo "详细记录：$LOG_FILE"
exit 1
