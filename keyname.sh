#!/bin/bash

# スクリプトの絶対パスを取得
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/$(basename "${BASH_SOURCE[0]}")"

# スクリプトが存在するディレクトリの絶対パスを取得
HOMEDIR="$(cd "$(dirname "${SCRIPT_PATH}")" && pwd -P)"

# IFSを変更
IFS_BK=$IFS
IFS=$'\n'

# $HOMEDIR配下のディレクトリを取得
TARGETS=($(find "$HOMEDIR/keynametmp" -type d))

# IFSを元に戻す
IFS=$IFS_BK

# カレントディレクトリを変更
cd "$HOMEDIR"

# リストに対してスクリプトを実行
for TARGET in "${TARGETS[@]}"
do
  #echo "$TARGET"
  python3 keyname.py "$TARGET"
done

exit 0