# 内部処理
**※こちらはまだ記述中です。**
内部処理を記述します。
```
・名称
msg: リンク先のメッセージ
message: リンクが含まれているメッセージ
m: Botが展開し、送信したメッセージ
```
# 展開処理を開始するかの確認処理
## mute確認
messageの[mute](https://github.com/Huyu2239/ExpandBot/blob/main/docs/flow.md#mute)設定を確認し、`有効`の場合は展開せずに処理を終了します。
## msgのサーバーがmessageのサーバーと同じとき
`設定にかかわらず`[展開処理](https://github.com/Huyu2239/ExpandBot/blob/main/docs/flow.md#展開処理)を開始します。
## msgのサーバーがmessageのサーバーと違うとき
設定を参照します。
### allow確認
msgの[allow](https://github.com/Huyu2239/ExpandBot/blob/main/docs/flow.md#allow)設定を確認し、`無効`と判断した場合は展開を行わず終了します。
### hidden確認
msgの[hidden](https://github.com/Huyu2239/ExpandBot/blob/main/docs/flow.md#hidden)設定を確認し、`有効`と判断した場合は展開を行わず終了します。
### 展開
上記の二つの確認をパスしたmsgのみ[展開処理](https://github.com/Huyu2239/ExpandBot/blob/main/docs/flow.md#展開処理)を開始します。
# 展開処理
# mute
# allow
# hidden