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
実データのp\_localをプロット
p\_local<10^-5 の領域のフィット結果の図示
p\_local\_minの追加測定前後の比較（paperのFIG.3）

get\_NEP.ipynb
----------------
yfactorデータからNEPを求めた

get\_original\_signal.ipynb
----------------
スペアナ出力(output)から元信号(input)を再構成する
--> 時間がかかるので get\_original\_signal.py を作成して、
    get\_original\_signal.sh で 2GHz ずつ job を作って
    並列で計算することにした

get\_p\_local\_hide.py
----------------
p\_localの計算を裏で走らせていたスクリプト
実データのフィット結果から p\_local を計算する

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
--> 時間がかかるので peak\_search.py を作成して、 
    peak\_search.sh で 1GHz ずつ job を作って
    並列で計算することにした。
 - result\_data\_newrebin1/fit\_result4 では
   2.5483924e+10 Hz の fit で P\_err が Nan になって 
   (fit がうまくいかない) 問題であった
 - peak\_search\_one.py は確認用に指定した周波数が含まれる
   2MHz のスパンだけ fit するスクリプト 

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
Paper に載せる beam width の図

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
 2. get\_original\_signal.ipynb or (get\_original\_signal.py & get\_original\_signal.sh)
	(今は追加測定のみになっている)
	- input信号強度の推定
	- P\_in を求める (Trx を引いて、G で割る)
 4. peak\_search.ipynb or (peak\_search.py & peak\_search.sh)
	(今は追加測定のみになっている)
	- input信号(追加測定を含む)をフィッティング
 5. beam width 関係の見積もり
 	1. Aeff\_analysis.ipynb
		- Aeff, eta_win の simulation からの見積もり
 	2. xy\_scan.ipynb
		- xy scan による beam width の measurement と simulation の比較
          	と beam width の誤差の見積もり
 5. quick\_plot.ipynb 
	- [10行目] fit result をプロット (P\_DP と p\_local)
	- [6行目] fit result から upper limit on P\_DP と upper limit on χ (syst. uncertainties含む) を計算
	- 全周波数領域の P\_DP, P\_out などのプロット
 6. limit\_plot.ipynb
	- quick\_plot の output data からリミットの図をプロット

null sample の表示は get\_Neff.py に書いてあるので、 null sample を使いたいときはそれを参照する良い


# Versions

result\_data
--------------
rebin to 2kHz を peak\_search.py の中で fit の前におこなった
- rebinfunc = 0: function.rebin_func(): Kotaka's wrong benning

result\_data\_newrebin
------------------------
rebin to 2kHz を peak\_search.py の中で fit の前におこなった
- rebinfunc = 1: function.rebin_func_consider_rbw()
- rebinmethod = 0 in function.rebin_func_consider_rbw(): consider bin edges of the original benning

result\_data\_newrebin1
------------------------
rebin to 2kHz を y-factor, get\_original\_signal.py でおこなった
(y-factor での 300K の温度は一定で、厳密には正しくない)
- rebinfunc = 1: function.rebin_func_consider_rbw()
- rebinmethod = 1 in function.rebin_func_consider_rbw(): cosider only bin center of the original benning

- fit\_result4
    - rebinfunc=2 (No rebin), init\_value\_set=3 (3回 fit をしてうまく fit を収束させる)
    - 25.483924 GHz のみ fit が失敗して nan 値が P\_err に入った
    - fit\_script.py で nan が出たら、 init value を P=1 にして再 fit するようにしたら、nan がなくなった
    - その結果を fit\_result4/start\_25.481750GHz.csv に反映
        - 修正前) 25483924000.0,-1.1709555794540472e-25,1.899894487002748e-18,9.084085768799774e-27,,,,1.1095077700758385,True
        - 修正後) 25483924000.0,-1.17095762e-25,1.8998945e-18,-5.31907781e-25,4.34419251e-26,4.78037268e-21,1.46775e-19,1.10950777,True
    - Bug: peak\_search.py で rebin をしないのだが、additional data があるときに、W1+W2 = W\_add ではなく、W1 に置き換えてしまっていた

result\_data\_newrebin2
------------------------
rebin to 2kHz を peak\_search.py の中で fit の前におこなった
- rebinfunc = 1: function.rebin_func_consider_rbw()
- rebinmethod = 1 in function.rebin_func_consider_rbw(): cosider only bin center of the original benning
** これが paper で最終的に掲載した方法 **