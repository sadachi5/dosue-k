# dosue-k
Scripts wrote by Shumpei Kotaka for dosue-K experiment

* Google doc for description: https://docs.google.com/document/d/1Cn2uayZuAdGIWZWUjYdDzjyH37X2TOtuRtCVlLCXcbk/edit?usp=sharing


Aeff\_analysis.ipynb
----------------
自分でアンテナを動かしていた時のデータからA\_effを推定する
HFSSシミュレーション結果の図示

diffraction.ipynb
----------------
回折効果の解析

fit\_script.py
----------------
inputデータをフィットする時の関数

function.py
----------------
各スクリプトでよく使う関数がまとまっている
datファイルの読み込み
csvファイルの読み込み
解析に使う2 MHz幅だけ取り出す

get\_N\_eff.ipynb
----------------
Neffの推定
ヌルサンプルのP/ΔPのヒストグラをプロット
ヌルサンプルのp\_localヒストグラムをプロット
実データのp\_local
p\_local<10^-5 の領域のフィット結果の図示
p\_local\_minの追加測定前後の比較（paperのFIG.3）

get\_NEP.ipynb
----------------
yfactorデータからNEPを求めた

get\_original\_signal.ipynb
----------------
スペアナ出力(output)から元信号(input)を再構成する

get\_p\_local\_hide.py
----------------
p\_localの計算を裏で走らせていたスクリプト

limit\_plot.ipynb
----------------
結合定数のプロット（paperのFIG.4）

montecarlo\_signal.ipynb
----------------
モンテカルロノイズと信号のプロット

NEP\_plot.ipynb
----------------
NEPをプロットしようとしたが、諦めた

null\_fit\_cycle.py
----------------
pythonスクリプトを裏で走らせるスクリプト
時間がかかる

null\_fit.py
----------------
ヌルサンプルの作成
それのフィット

peak\_serch.ipynb
----------------
inputデータのフィッティング

plot\_temperature.ipynb
----------------
冷却開始からの温度変化のプロット

quick\_plot.ipynb
----------------
図を見てみたくなった時に適当にここで書いていた
結合定数の95%上限値
追加測定後のp\_local
追加測定前後のp\_localの比較（paperのFIG.2）
inputデータとoutputデータの比較
本研究におけるp\_localとp\_globalの関係

rebin\_analysis.ipynb
----------------
リビン幅の違いによる解析結果(P/ΔP)の違い
P/ΔPヒストグラムの中心値と幅

rewrite\_csv.ipynb
----------------
csvファイルの中身を変える時に使った
修論には使っていない

show\_fit\_result\_all.ipynb
----------------
全フィット結果のP/ΔPヒストグラムのプロット

show\_fit\_result.ipynb
----------------
各領域におけるフィット結果のプロット
修論には使っていない

untitled.ipynb
----------------
各領域でのゲイン、ノイズの確認
修論には使っていない

untitled1.ipynb
----------------
各領域でのフィット結果、p\_localなどまとめたもの
修論には使っていない

xy\_scan.ipynb
----------------
アクチュエータを使ったAeff推定
x方向、y方向の信号強度のカラーマップ
x、yそれぞれの中心でスライスした図

yfactor\_analysis.ipynb
----------------
yfactorの解析結果の保存
TsysとTloadの推定

yfactor\_plot\_all.ipynb
----------------
全領域でのゲインとノイズのプロット
前後のyfactorのゲインの比

yfactor\_plot.ipynb
----------------
各領域でのyfactorの結果
修論では使っていない



# 解析の手順

 1. yfactor\_analysis.ipynb
	ゲイン、ノイズの推定
 2. get\_original\_signal.ipynb
	- input信号強度の推定
	- P\_in を求める (Trx を引いて、G で割る)
 4. peak\_serch.ipynb
	- input信号(追加測定を含む)をフィッティング
 5. quick\_plot.ipynb 
	- [6行目] fit result から upper limit on P\_DP と upper limit on χ (syst. uncertainties含む) を計算
 6. limit\_plot.ipynb
	- quick\_plot の output data からリミットの図をプロット

null sample の表示は get\_Neff.py に書いてあるので、 null sample を使いたいときはそれを参照する良い

