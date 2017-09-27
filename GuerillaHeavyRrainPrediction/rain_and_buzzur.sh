# 第一引数でsshのパスワードを入力してください

#予測降雨量算出 -> txtファイルで書き出し
python 1hLaterRain.py

#1hLaterRain.pyで書き出されたtxtファイルから予測降雨量取得
result=`cat ./result/result.txt`

#予測降雨量が10mm以上であればRaspbarryPiのi2c1602.py実行 ->　ブザーがなる
#第一引数で渡されたパスワードを使ってssh

if [ $result -gt 10 ] ; then
    sshpass -p $1 ssh -o StrictHostKeyChecking=no pi@[RaspberryPiのIPアドレス] python /home/pi/test/i2c1602_lcd.py $result
    #sleep 5
    #process_no=`sshpass -p ssh  -o StrictHostKeyChecking=no pi@[RaspberryPiのIPアドレス] ps auxww | grep i2c`
    #echo $process_no
    #process_no=${process_no#* }
    #process_no="$(echo $process_no | head -c 1)"
    #sshpass -p $1 ssh -o StrictHostKeyChecking=no pi@[RaspberryPiのIPアドレス] kill $process_no

fi
