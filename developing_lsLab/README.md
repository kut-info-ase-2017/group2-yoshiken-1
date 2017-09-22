#lsLab

## Humandetection
HumanDetection -> HOG特徴で人物検出

## HumanIdentification
create_model -> Bag of Featureモデルを作成
create_bof -> 各画像のVisual Wordを作成
create_humanmodel -> 未知の画像を用いて，人物検出

##raspberryPi
twosensor -> 2つのセンサーで入退出を判定し，カメラで画像を取得

##client
write -> 特定した人物の情報を更新する
show -> 現在の研究室の状況を表示する
member.json -> ユーザの情報を格納