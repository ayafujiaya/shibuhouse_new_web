# /////////////////////// #
#    各種設定ここから
# /////////////////////// #

package main;


sub mobilemailimg(){
=pod
#############################################################################

$imgtag = mobileimg(c);
sjis絵文字バイナリコードを返す。

EUCのCGIファイル内で、printhtml（sjis出力）しているときに、
sjisバイナリコードを読み込むため、正常に表示できる

c=キャリア（ドコモ、au、ソフトバンク  99=画像）

例

#############################################################################
=cut

# コメントアウトしてるものは、使わないやつ（ドコモとAUで互換性の無い絵文字）
# ドコモとAUは同じ絵文字を使用していますが、今後のことを考えて一応分けてあります
	
	my $paturn = shift;
	
	if($paturn eq "docomo"){
		$paturn = 1;
	}elsif($paturn eq "ezweb"){
		$paturn = 2;
	}elsif($paturn eq "jphone"){
		$paturn = 3;
	}
	
	my @PAT;
	# 太陽
	$PAT[1]->{e_taiyou} = "\xF8\x9F";
	$PAT[2]->{e_taiyou} = "\xF6\x60";
	$PAT[3]->{e_taiyou} = "\xEE\x81\x8A";
	$PAT[99]->{e_taiyou} = '63647.gif';
	
	# 曇り
	$PAT[1]->{e_kumo} = "\xF8\xA0";
	$PAT[2]->{e_kumo} = "\xF6\x65";
	$PAT[3]->{e_kumo} = "\xEE\x81\x89";
	$PAT[99]->{e_kumo} = '63648.gif';
	
	# 雨
	$PAT[1]->{e_ame} = "\xF8\xA1";
	$PAT[2]->{e_ame} = "\xF6\x64";
	$PAT[3]->{e_ame} = "\xEE\x81\x8B";
	$PAT[99]->{e_ame} = '63649.gif';
	
	# 雪
	$PAT[1]->{e_yuki} = "\xF8\xA2";
	$PAT[2]->{e_yuki} = "\xF6\x5D";
	$PAT[3]->{e_yuki} = "\xEE\x81\x88";
	$PAT[99]->{e_yuki} = '63650.gif';
	
	# 雷
	$PAT[1]->{e_kaminari} = "\xF8\xA3";
	$PAT[2]->{e_kaminari} = "\xF6\x5F";
	$PAT[3]->{e_kaminari} = "\xEE\x84\xBD";
	$PAT[99]->{e_kaminari} = '63651.gif';
	
	# 台風
	$PAT[1]->{e_taihu} = "\xF8\xA4";
	$PAT[2]->{e_taihu} = "\xF6\x41";
	$PAT[3]->{e_taihu} = "\xEE\x91\x83";
	$PAT[99]->{e_taihu} = '63652.gif';
	
	# 霧
#	$PAT[1]->{e_kiri} = "\xF8\xA5";
#	$PAT[2]->{e_kiri} = "\xF7\xB5";
#	$PAT[3]->{e_kiri} = "\xEE\x84\x8B";
#	$PAT[99]->{e_kiri} = '63653.gif';
	
	# 傘
	$PAT[1]->{e_kasa} = "\xF8\xA6";
	$PAT[2]->{e_kasa} = "\xF3\xBC";
	$PAT[3]->{e_kasa} = "\xEE\x90\xBC";
	$PAT[99]->{e_kasa} = '63654.gif';

	# 牡羊座
	$PAT[1]->{e_ohitujiza} = "\xF8\xA7";
	$PAT[2]->{e_ohitujiza} = "\xF6\x67";
	$PAT[3]->{e_ohitujiza} = "\xEE\x88\xBF";
	$PAT[99]->{e_ohitujiza} = '63655.gif';
	
	# 牡牛座
	$PAT[1]->{e_ousiza} = "\xF8\xA8";
	$PAT[2]->{e_ousiza} = "\xF6\x68";
	$PAT[3]->{e_ousiza} = "\xEE\x89\x80";
	$PAT[99]->{e_ousiza} = '63656.gif';
	
	# 双子座
	$PAT[1]->{e_hutagoza} = "\xF8\xA9";
	$PAT[2]->{e_hutagoza} = "\xF6\x69";
	$PAT[3]->{e_hutagoza} = "\xEE\x89\x81";
	$PAT[99]->{e_hutagoza} = '63657.gif';
	
	# 蟹座
	$PAT[1]->{e_kaniza} = "\xF8\xAA";
	$PAT[2]->{e_kaniza} = "\xF6\x6A";
	$PAT[3]->{e_kaniza} = "\xEE\x89\x82";
	$PAT[99]->{e_kaniza} = '63658.gif';
	
	# 獅子座
	$PAT[1]->{e_sisiza} = "\xF8\xAB";
	$PAT[2]->{e_sisiza} = "\xF6\x6B";
	$PAT[3]->{e_sisiza} = "\xEE\x89\x83";
	$PAT[99]->{e_sisiza} = '63659.gif';
	
	# 乙女座
	$PAT[1]->{e_otomeza} = "\xF8\xAC";
	$PAT[2]->{e_otomeza} = "\xF6\x6C";
	$PAT[3]->{e_otomeza} = "\xEE\x89\x84";
	$PAT[99]->{e_otomeza} = '63660.gif';
	
	# 天秤座
	$PAT[1]->{e_tenbinza} = "\xF8\xAD";
	$PAT[2]->{e_tenbinza} = "\xF6\x6D";
	$PAT[3]->{e_tenbinza} = "\xEE\x89\x85";
	$PAT[99]->{e_tenbinza} = '63661.gif';
	
	# 蠍座
	$PAT[1]->{e_sasoriza} = "\xF8\xAE";
	$PAT[2]->{e_sasoriza} = "\xF6\x6E";
	$PAT[3]->{e_sasoriza} = "\xEE\x89\x86";
	$PAT[99]->{e_sasoriza} = '63662.gif';
	
	# 射手座
	$PAT[1]->{e_iteza} = "\xF8\xAF";
	$PAT[2]->{e_iteza} = "\xF6\x6F";
	$PAT[3]->{e_iteza} = "\xEE\x89\x87";
	$PAT[99]->{e_iteza} = '63663.gif';
	
	# 山羊座
	$PAT[1]->{e_yagiza} = "\xF8\xB0";
	$PAT[2]->{e_yagiza} = "\xF6\x70";
	$PAT[3]->{e_yagiza} = "\xEE\x89\x88";
	$PAT[99]->{e_yagiza} = '63664.gif';
	
	# 水瓶座
	$PAT[1]->{e_mizugameza} = "\xF8\xB1";
	$PAT[2]->{e_mizugameza} = "\xF6\x71";
	$PAT[3]->{e_mizugameza} = "\xEE\x89\x89";
	$PAT[99]->{e_mizugameza} = '63665.gif';
	
	# 魚座
	$PAT[1]->{e_uoza} = "\xF8\xB2";
	$PAT[2]->{e_uoza} = "\xF6\x72";
	$PAT[3]->{e_uoza} = "\xEE\x89\x8A";
	$PAT[99]->{e_uoza} = '63666.gif';
	
	# 野球
	$PAT[1]->{e_uoza} = "\xF8\xB4";
	$PAT[2]->{e_uoza} = "\xF6\x93";
	$PAT[3]->{e_uoza} = "\xEE\x80\x96";
	$PAT[99]->{e_uoza} = '63668.gif';
	
	# ゴルフ
	$PAT[1]->{e_golf} = "\xF8\xB5";
	$PAT[2]->{e_golf} = "\xF7\xB6";
	$PAT[3]->{e_golf} = "\xEE\x80\x94";
	$PAT[99]->{e_golf} = '63669.gif';
	
	# テニス
	$PAT[1]->{e_tennis} = "\xF8\xB6";
	$PAT[2]->{e_tennis} = "\xF6\x90";
	$PAT[3]->{e_tennis} = "\xEE\x80\x85";
	$PAT[99]->{e_tennis} = '63670.gif';
	
	# サッカー
	$PAT[1]->{e_soccer} = "\xF8\xB7";
	$PAT[2]->{e_soccer} = "\xF6\x8F";
	$PAT[3]->{e_soccer} = "\xEE\x80\x98";
	$PAT[99]->{e_soccer} = '63671.gif';
	
	# スキー
	$PAT[1]->{e_ski} = "\xF8\xB8";
	$PAT[2]->{e_ski} = "\xF3\x80";
	$PAT[3]->{e_ski} = "\xEE\x80\x93";
	$PAT[99]->{e_ski} = '63672.gif';
	
	# バスケットボール
	$PAT[1]->{e_baske} = "\xF8\xB9";
	$PAT[2]->{e_baske} = "\xF7\xB7";
	$PAT[3]->{e_baske} = "\xEE\x90\xAA";
	$PAT[99]->{e_baske} = '63673.gif';
	
	# モータースポーツ
	$PAT[1]->{e_motor} = "\xF8\xBA";
	$PAT[2]->{e_motor} = "\xF6\x92";
	$PAT[3]->{e_motor} = "\xEE\x84\xB2";
	$PAT[99]->{e_motor} = '63674.gif';
	
	# 電車
	$PAT[1]->{e_train} = "\xF8\xBC";
	$PAT[2]->{e_train} = "\xF6\x8E";
	$PAT[3]->{e_train} = "\xEE\x80\x9E";
	$PAT[99]->{e_train} = '63676.gif';
	
	# 地下鉄
	$PAT[1]->{e_subway} = "\xF8\xBD";
	$PAT[2]->{e_subway} = "\xF7\xEC";
	$PAT[3]->{e_subway} = "\xEE\x90\xB4";
	$PAT[99]->{e_subway} = '63677.gif';
	
	# 車
	$PAT[1]->{e_car} = "\xF8\xBF";
	$PAT[2]->{e_car} = "\xF6\x8A";
	$PAT[3]->{e_car} = "\xEE\x80\x9B";
	$PAT[99]->{e_car} = '63679.gif';
	
	# バス
	$PAT[1]->{e_bus} = "\xF8\xC1";
	$PAT[2]->{e_bus} = "\xF6\x88";
	$PAT[3]->{e_bus} = "\xEE\x85\x99";
	$PAT[99]->{e_bus} = '63681.gif';
	
	# 船
	$PAT[1]->{e_ship} = "\xF8\xC2";
	$PAT[2]->{e_ship} = "\xF3\x55";
	$PAT[3]->{e_ship} = "\xEE\x88\x82";
	$PAT[99]->{e_ship} = '63682.gif';
	
	# 飛行機
	$PAT[1]->{e_hikouki} = "\xF8\xC3";
	$PAT[2]->{e_hikouki} = "\xF6\x8C";
	$PAT[3]->{e_hikouki} = "\xEE\x80\x9D";
	$PAT[99]->{e_hikouki} = '63683.gif';
	
	# 家
	$PAT[1]->{e_house} = "\xF8\xC4";
	$PAT[2]->{e_house} = "\xF6\x84";
	$PAT[3]->{e_house} = "\xEE\x80\xB6";
	$PAT[99]->{e_house} = '63684.gif';
	
	# ビル
	$PAT[1]->{e_biru} = "\xF8\xC5";
	$PAT[2]->{e_biru} = "\xF6\x86";
	$PAT[3]->{e_biru} = "\xEE\x80\xB8";
	$PAT[99]->{e_biru} = '63685.gif';
	
	# 郵便局
	$PAT[1]->{e_yuubin} = "\xF8\xC6";
	$PAT[2]->{e_yuubin} = "\xF3\x51";
	$PAT[3]->{e_yuubin} = "\xEE\x85\x93";
	$PAT[99]->{e_yuubin} = '63686.gif';
	
	# 病院
	$PAT[1]->{e_hospital} = "\xF8\xC7";
	$PAT[2]->{e_hospital} = "\xF3\x52";
	$PAT[3]->{e_hospital} = "\xEE\x85\x95";
	$PAT[99]->{e_hospital} = '63687.gif';
	
	# 銀行
	$PAT[1]->{e_bank} = "\xF8\xC8";
	$PAT[2]->{e_bank} = "\xF6\x83";
	$PAT[3]->{e_bank} = "\xEE\x85\x8D";
	$PAT[99]->{e_bank} = '63688.gif';
	
	# ATM
	$PAT[1]->{e_atm} = "\xF8\xC9";
	$PAT[2]->{e_atm} = "\xF6\x7B";
	$PAT[3]->{e_atm} = "\xEE\x85\x94";
	$PAT[99]->{e_atm} = '63689.gif';
	
	# ホテル
	$PAT[1]->{e_hotel} = "\xF8\xCA";
	$PAT[2]->{e_hotel} = "\xF3\x54";
	$PAT[3]->{e_hotel} = "\xEE\x85\x98";
	$PAT[99]->{e_hotel} = '63690.gif';
	
	# コンビニ
	$PAT[1]->{e_konbini} = "\xF8\xCB";
	$PAT[2]->{e_konbini} = "\xF6\x7C";
	$PAT[3]->{e_konbini} = "\xEE\x85\x96";
	$PAT[99]->{e_konbini} = '63691.gif';
	
	# ガソリンスタンド
	$PAT[1]->{e_gs} = "\xF8\xCC";
	$PAT[2]->{e_gs} = "\xF7\x8E";
	$PAT[3]->{e_gs} = "\xEE\x80\xBA";
	$PAT[99]->{e_gs} = '63692.gif';
	
	# 駐車場
	$PAT[1]->{e_parking} = "\xF8\xCD";
	$PAT[2]->{e_parking} = "\xF6\x7E";
	$PAT[3]->{e_parking} = "\xEE\x85\x8F";
	$PAT[99]->{e_parking} = '63693.gif';
	
	# 信号
	$PAT[1]->{e_singou} = "\xF8\xCE";
	$PAT[2]->{e_singou} = "\xF6\x42";
	$PAT[3]->{e_singou} = "\xEE\x85\x8E";
	$PAT[99]->{e_singou} = '63694.gif';
	
	# トイレ
	$PAT[1]->{e_toilet} = "\xF8\xCF";
	$PAT[2]->{e_toilet} = "\xF6\x7D";
	$PAT[3]->{e_toilet} = "\xEE\x85\x80";
	$PAT[99]->{e_toilet} = '63695.gif';
	
	# レストラン
	$PAT[1]->{e_resutoran} = "\xF8\xD0";
	$PAT[2]->{e_resutoran} = "\xF6\x85";
	$PAT[3]->{e_resutoran} = "\xEE\x81\x83";
	$PAT[99]->{e_resutoran} = '63696.gif';
	
	# 喫茶店
	$PAT[1]->{e_cafe} = "\xF8\xD1";
	$PAT[2]->{e_cafe} = "\xF7\xB4";
	$PAT[3]->{e_cafe} = "\xEE\x81\x85";
	$PAT[99]->{e_cafe} = '63697.gif';
	
	# バー
	$PAT[1]->{e_bar} = "\xF8\xD2";
	$PAT[2]->{e_bar} = "\xF6\x9B";
	$PAT[3]->{e_bar} = "\xEE\x81\x84";
	$PAT[99]->{e_bar} = '63698.gif';
	
	# ビール
	$PAT[1]->{e_beer} = "\xF8\xD3";
	$PAT[2]->{e_beer} = "\xF6\x9C";
	$PAT[3]->{e_beer} = "\xEE\x81\x87";
	$PAT[99]->{e_beer} = '63699.gif';
	
	# ハンバーガー
	$PAT[1]->{e_humburger} = "\xF8\xD4";
	$PAT[2]->{e_humburger} = "\xF6\xAF";
	$PAT[3]->{e_humburger} = "\xEE\x84\xA0";
	$PAT[99]->{e_humburger} = '63700.gif';
	
	# 靴
	$PAT[1]->{e_shoes} = "\xF8\xD5";
	$PAT[2]->{e_shoes} = "\xF6\xF3";
	$PAT[3]->{e_shoes} = "\xEE\x80\x87";
	$PAT[99]->{e_shoes} = '63701.gif';
	
	# ハサミ
	$PAT[1]->{e_hasami} = "\xF8\xD6";
	$PAT[2]->{e_hasami} = "\xF6\xEF";
	$PAT[3]->{e_hasami} = "\xEE\x8C\x93";
	$PAT[99]->{e_hasami} = '63702.gif';
	
	# カラオケ
	$PAT[1]->{e_karaoke} = "\xF8\xD7";
	$PAT[2]->{e_karaoke} = "\xF6\xDC";
	$PAT[3]->{e_karaoke} = "\xEE\x80\xBC";
	$PAT[99]->{e_karaoke} = '63703.gif';
	
	# 映画
	$PAT[1]->{e_movie} = "\xF8\xD8";
	$PAT[2]->{e_movie} = "\xF6\xF0";
	$PAT[3]->{e_movie} = "\xEE\x80\xBD";
	$PAT[99]->{e_movie} = '63704.gif';
	
	# 右斜め上
	$PAT[1]->{e_migiue} = "\xF8\xD9";
	$PAT[2]->{e_migiue} = "\xF7\x71";
	$PAT[3]->{e_migiue} = "\xEE\x88\xB6";
	$PAT[99]->{e_migiue} = '63705.gif';
	
	# 音楽
	$PAT[1]->{e_music} = "\xF8\xDB";
	$PAT[2]->{e_music} = "\xF6\xE1";
	$PAT[3]->{e_music} = "\xEE\x80\xBE";
	$PAT[99]->{e_music} = '63707.gif';
	
	# アート
	$PAT[1]->{e_art} = "\xF8\xDC";
	$PAT[2]->{e_art} = "\xF7\xB9";
	$PAT[3]->{e_art} = "\xEE\x94\x82";
	$PAT[99]->{e_art} = '63708.gif';
	
	# 演劇
	$PAT[1]->{e_engeki} = "\xF8\xDD";
	$PAT[2]->{e_engeki} = "\xF3\xC9";
	$PAT[3]->{e_engeki} = "\xEE\x94\x83";
	$PAT[99]->{e_engeki} = '63709.gif';
	
	# チケット
	$PAT[1]->{e_ticket} = "\xF8\xDF";
	$PAT[2]->{e_ticket} = "\xF6\x76";
	$PAT[3]->{e_ticket} = "\xEE\x84\xA5";
	$PAT[99]->{e_ticket} = '63711.gif';
	
	# 喫煙
	$PAT[1]->{e_smoking} = "\xF8\xE0";
	$PAT[2]->{e_smoking} = "\xF6\x55";
	$PAT[3]->{e_smoking} = "\xEE\x8C\x8E";
	$PAT[99]->{e_smoking} = '63712.gif';
	
	# 禁煙
	$PAT[1]->{e_nosmoking} = "\xF8\xE1";
	$PAT[2]->{e_nosmoking} = "\xF6\x56";
	$PAT[3]->{e_nosmoking} = "\xEE\x88\x88";
	$PAT[99]->{e_nosmoking} = '63713.gif';
	
	# カメラ
	$PAT[1]->{'e_camera'} = "\xF8\xE2";
	$PAT[2]->{'e_camera'} = "\xF6\xEE";
	$PAT[3]->{'e_camera'} = "\xEE\x80\x88";
	$PAT[99]->{'e_camera'} = '63714.gif';
	
	# カバン
	$PAT[1]->{e_kaban} = "\xF8\xE3";
	$PAT[2]->{e_kaban} = "\xF6\x74";
	$PAT[3]->{e_kaban} = "\xEE\x84\x9E";
	$PAT[99]->{e_kaban} = '63715.gif';
	
	# 本
	$PAT[1]->{e_book} = "\xF8\xE4";
	$PAT[2]->{e_book} = "\xF6\x77";
	$PAT[3]->{e_book} = "\xEE\x85\x88";
	$PAT[99]->{e_book} = '63716.gif';
	
	# リボン
	$PAT[1]->{e_ribon} = "\xF8\xE5";
	$PAT[2]->{e_ribon} = "\xF7\xBC";
	$PAT[3]->{e_ribon} = "\xEE\x8C\x94";
	$PAT[99]->{e_ribon} = '63717.gif';
	
	# プレゼント
	$PAT[1]->{e_prezent} = "\xF8\xE6";
	$PAT[2]->{e_prezent} = "\xF6\xA8";
	$PAT[3]->{e_prezent} = "\xEE\x84\x92";
	$PAT[99]->{e_prezent} = '63718.gif';
	
	# バースデー
	$PAT[1]->{e_birthday} = "\xF8\xE7";
	$PAT[2]->{e_birthday} = "\xF7\xBD";
	$PAT[3]->{e_birthday} = "\xEE\x8D\x8B";
	$PAT[99]->{e_birthday} = '63719.gif';
	
	# 電話
	$PAT[1]->{e_tel} = "\xF8\xE8";
	$PAT[2]->{e_tel} = "\xF7\xB3";
	$PAT[3]->{e_tel} = "\xEE\x80\x89";
	$PAT[99]->{e_tel} = '63720.gif';
	
	# 携帯
	$PAT[1]->{e_mobile} = "\xF8\xE9";
	$PAT[2]->{e_mobile} = "\xF7\xA5";
	$PAT[3]->{e_mobile} = "\xEE\x80\x8A";
	$PAT[99]->{e_mobile} = '63721.gif';
	
	# メモ
	$PAT[1]->{e_memo} = "\xF8\xEA";
	$PAT[2]->{e_memo} = "\xF3\x65";
	$PAT[3]->{e_memo} = "\xEE\x8C\x81";
	$PAT[99]->{e_memo} = '63722.gif';
	
	# テレビ
	$PAT[1]->{e_tv} = "\xF8\xEB";
	$PAT[2]->{e_tv} = "\xF6\xDB";
	$PAT[3]->{e_tv} = "\xEE\x84\xAA";
	$PAT[99]->{e_tv} = '63723.gif';
	
	# CD
	$PAT[1]->{e_cd} = "\xF8\xED";
	$PAT[2]->{e_cd} = "\xF6\xE5";
	$PAT[3]->{e_cd} = "\xEE\x84\xA6";
	$PAT[99]->{e_cd} = '63725.gif';
	
	# ハート
	$PAT[1]->{e_heart} = "\xF8\xEE";
	$PAT[2]->{e_heart} = "\xF3\x78";
	$PAT[3]->{e_heart} = "\xEE\x88\x8C";
	$PAT[99]->{e_heart} = '63726.gif';
	
	# スペード
	$PAT[1]->{e_spead} = "\xF8\xEF";
	$PAT[2]->{e_spead} = "\xF7\xBE";
	$PAT[3]->{e_spead} = "\xEE\x88\x8E";
	$PAT[99]->{e_spead} = '63727.gif';
	
	# ダイヤ
	$PAT[1]->{e_daiya} = "\xF8\xF0";
	$PAT[2]->{e_daiya} = "\xF7\xBF";
	$PAT[3]->{e_daiya} = "\xEE\x88\x8D";
	$PAT[99]->{e_daiya} = '63728.gif';
	
	# クラブ
	$PAT[1]->{e_kurabu} = "\xF8\xF1";
	$PAT[2]->{e_kurabu} = "\xF7\xC0";
	$PAT[3]->{e_kurabu} = "\xEE\x88\x8F";
	$PAT[99]->{e_kurabu} = '63729.gif';
	
	# 目
	$PAT[1]->{e_eye} = "\xF8\xF2";
	$PAT[2]->{e_eye} = "\xF7\xC1";
	$PAT[3]->{e_eye} = "\xEE\x90\x99";
	$PAT[99]->{e_eye} = '63730.gif';
	
	# 耳
	$PAT[1]->{e_ear} = "\xF8\xF3";
	$PAT[2]->{e_ear} = "\xF7\xC2";
	$PAT[3]->{e_ear} = "\xEE\x90\x9B";
	$PAT[99]->{e_ear} = '63731.gif';
	
	# グー
	$PAT[1]->{e_guu} = "\xF8\xF4";
	$PAT[2]->{e_guu} = "\xF4\x88";
	$PAT[3]->{e_guu} = "\xEE\x80\x90";
	$PAT[99]->{e_guu} = '63732.gif';
	
	# ちょき
	$PAT[1]->{e_tyoki} = "\xF8\xF5";
	$PAT[2]->{e_tyoki} = "\xF7\xC3";
	$PAT[3]->{e_tyoki} = "\xEE\x80\x91";
	$PAT[99]->{e_tyoki} = '63733.gif';
	
	# パー
	$PAT[1]->{e_paa} = "\xF8\xF6";
	$PAT[2]->{e_paa} = "\xF7\xC4";
	$PAT[3]->{e_paa} = "\xEE\x80\x92";
	$PAT[99]->{e_paa} = '63734.gif';
	
	# 右下
	$PAT[1]->{e_migishita} = "\xF8\xF7";
	$PAT[2]->{e_migishita} = "\xF7\x69";
	$PAT[3]->{e_migishita} = "\xEE\x88\xB8";
	$PAT[99]->{e_migishita} = '63735.gif';
	
	# 左上
	$PAT[1]->{e_hidariue} = "\xF8\xF8";
	$PAT[2]->{e_hidariue} = "\xF7\x68";
	$PAT[3]->{e_hidariue} = "\xEE\x88\xB7";
	$PAT[99]->{e_hidariue} = '63736.gif';
	
	# 足
	$PAT[1]->{e_foot} = "\xF8\xF9";
	$PAT[2]->{e_foot} = "\xF3\xEB";
	$PAT[3]->{e_foot} = "\xEE\x94\xB6";
	$PAT[99]->{e_foot} = '63737.gif';
	
	# 車いす
	$PAT[1]->{e_kurumaisu} = "\xF8\xFC";
	$PAT[2]->{e_kurumaisu} = "\xF6\x57";
	$PAT[3]->{e_kurumaisu} = "\xEE\x88\x8A";
	$PAT[99]->{e_kurumaisu} = '63740.gif';
	
	# 三日月
	$PAT[1]->{e_mikazuki} = "\xF9\x43";
	$PAT[2]->{e_mikazuki} = "\xF6\x5E";
	$PAT[3]->{e_mikazuki} = "\xEE\x81\x8C";
	$PAT[99]->{e_mikazuki} = '63811.gif';
	
	# 犬
	$PAT[1]->{e_dog} = "\xF9\x45";
	$PAT[2]->{e_dog} = "\xF6\xBA";
	$PAT[3]->{e_dog} = "\xEE\x81\x92";
	$PAT[99]->{e_dog} = '63813.gif';
	
	# 猫
	$PAT[1]->{e_neko} = "\xF9\x46";
	$PAT[2]->{e_neko} = "\xF6\xB4";
	$PAT[3]->{e_neko} = "\xEE\x81\x8F";
	$PAT[99]->{e_neko} = '63814.gif';
	
	# ヨット
	$PAT[1]->{e_yotto} = "\xF9\x47";
	$PAT[2]->{e_yotto} = "\xF6\x8D";
	$PAT[3]->{e_yotto} = "\xEE\x80\x9C";
	$PAT[99]->{e_yotto} = '63815.gif';
	
	# クリスマス
	$PAT[1]->{e_xmas} = "\xF9\x48";
	$PAT[2]->{e_xmas} = "\xF6\xA2";
	$PAT[3]->{e_xmas} = "\xEE\x80\xB3";
	$PAT[99]->{e_xmas} = '63816.gif';
	
	# 左下
	$PAT[1]->{e_hidarishita} = "\xF9\x49";
	$PAT[2]->{e_hidarishita} = "\xF7\x72";
	$PAT[3]->{e_hidarishita} = "\xEE\x88\xB9";
	$PAT[99]->{e_hidarishita} = '63817.gif';
	
	# 電話する
	$PAT[1]->{e_phoneto} = "\xF9\x72";
	$PAT[2]->{e_phoneto} = "\xF7\xDF";
	$PAT[3]->{e_phoneto} = "\xEE\x80\x89";
	$PAT[99]->{e_phoneto} = '63858.gif';
	
	# メールする
	$PAT[1]->{e_mailto} = "\xF9\x73";
	$PAT[2]->{e_mailto} = "\xF4\x66";
	$PAT[3]->{e_mailto} = "\xEE\x84\x83";
	$PAT[99]->{e_mailto} = '63859.gif';
	
	# ファックス
	$PAT[1]->{e_faxto} = "\xF9\x74";
	$PAT[2]->{e_faxto} = "\xF6\xF9";
	$PAT[3]->{e_faxto} = "\xEE\x80\x8B";
	$PAT[99]->{e_faxto} = '63860.gif';
	
	# ID
	$PAT[1]->{e_id} = "\xF9\x7C";
	$PAT[2]->{e_id} = "\xF3\x5B";
	$PAT[3]->{e_id} = "\xEE\x88\xA9";
	$PAT[99]->{e_id} = '63868.gif';
	
	# サーチ
	$PAT[1]->{e_search} = "\xF9\x81";
	$PAT[2]->{e_search} = "\xF6\xF1";
	$PAT[3]->{e_search} = "\xEE\x84\x94";
	$PAT[99]->{e_search} = '63873.gif';
	
	# NEW
	$PAT[1]->{e_new} = "\xF9\x82";
	$PAT[2]->{e_new} = "\xF7\xE5";
	$PAT[3]->{e_new} = "\xEE\x88\x92";
	$PAT[99]->{e_new} = '63874.gif';
	
	# シャープ
	$PAT[1]->{e_sharp} = "\xF9\x85";
	$PAT[2]->{e_sharp} = "\xF4\x89";
	$PAT[3]->{e_sharp} = "\xEE\x88\x90";
	$PAT[99]->{e_sharp} = '63877.gif';
	
	# 1
	$PAT[1]->{e_1} = "\xF9\x87";
	$PAT[2]->{e_1} = "\xF6\xFB";
	$PAT[3]->{e_1} = "\xEE\x88\x9C";
	$PAT[99]->{e_1} = '63879.gif';
	
	# 2
	$PAT[1]->{e_2} = "\xF9\x88";
	$PAT[2]->{e_2} = "\xF6\xFC";
	$PAT[3]->{e_2} = "\xEE\x88\x9D";
	$PAT[99]->{e_2} = '63880.gif';
	
	# 3
	$PAT[1]->{e_3} = "\xF9\x89";
	$PAT[2]->{e_3} = "\xF7\x40";
	$PAT[3]->{e_3} = "\xEE\x88\x9E";
	$PAT[99]->{e_3} = '63881.gif';
	
	# 4
	$PAT[1]->{e_4} = "\xF9\x8A";
	$PAT[2]->{e_4} = "\xF7\x41";
	$PAT[3]->{e_4} = "\xEE\x88\x9F";
	$PAT[99]->{e_4} = '63882.gif';
	
	# 5
	$PAT[1]->{e_5} = "\xF9\x8B";
	$PAT[2]->{e_5} = "\xF7\x42";
	$PAT[3]->{e_5} = "\xEE\x88\xA0";
	$PAT[99]->{e_5} = '63883.gif';
	
	# 6
	$PAT[1]->{e_6} = "\xF9\x8C";
	$PAT[2]->{e_6} = "\xF7\x43";
	$PAT[3]->{e_6} = "\xEE\x88\xA1";
	$PAT[99]->{e_6} = '63884.gif';
	
	# 7
	$PAT[1]->{e_7} = "\xF9\x8D";
	$PAT[2]->{e_7} = "\xF7\x44";
	$PAT[3]->{e_7} = "\xEE\x88\xA2";
	$PAT[99]->{e_7} = '63885.gif';
	
	# 8
	$PAT[1]->{e_8} = "\xF9\x8E";
	$PAT[2]->{e_8} = "\xF7\x45";
	$PAT[3]->{e_8} = "\xEE\x88\xA3";
	$PAT[99]->{e_8} = '63886.gif';
	
	# 9
	$PAT[1]->{e_9} = "\xF9\x8F";
	$PAT[2]->{e_9} = "\xF7\x46";
	$PAT[3]->{e_9} = "\xEE\x88\xA4";
	$PAT[99]->{e_9} = '63887.gif';
	
	# 0
	$PAT[1]->{e_0} = "\xF9\x90";
	$PAT[2]->{e_0} = "\xF7\xC9";
	$PAT[3]->{e_0} = "\xEE\x88\xA5";
	$PAT[99]->{e_0} = '63888.gif';
	
	# OK
	$PAT[1]->{e_ok} = "\xF9\xB0";
	$PAT[2]->{e_ok} = "\xF7\xCA";
	$PAT[3]->{e_ok} = "\xEE\x90\xA0";
	$PAT[99]->{e_ok} = '63920.gif';
	
	# ハートマーク
	$PAT[1]->{e_heartmark} = "\xF9\x91";
	$PAT[2]->{e_heartmark} = "\xF7\xB2";
	$PAT[3]->{e_heartmark} = "\xEE\x80\xA2";
	$PAT[99]->{e_heartmark} = '63889.gif';
	
	# 失恋
	$PAT[1]->{e_heartbreak} = "\xF9\x93";
	$PAT[2]->{e_heartbreak} = "\xF6\x4F";
	$PAT[3]->{e_heartbreak} = "\xEE\x80\xA3";
	$PAT[99]->{e_heartbreak} = '63891.gif';
	
	# うれしい顔
	$PAT[1]->{e_smile} = "\xF9\x95";
	$PAT[2]->{e_smile} = "\xF6\x49";
	$PAT[3]->{e_smile} = "\xEE\x81\x96";
	$PAT[99]->{e_smile} = '63893.gif';
	
	# 怒った顔
	$PAT[1]->{e_angry} = "\xF9\x96";
	$PAT[2]->{e_angry} = "\xF6\x4A";
	$PAT[3]->{e_angry} = "\xEE\x81\x99";
	$PAT[99]->{e_angry} = '63894.gif';
	
	# 悲しい顔
	$PAT[1]->{e_syobon} = "\xF9\x98";
	$PAT[2]->{e_syobon} = "\xF3\x97";
	$PAT[3]->{e_syobon} = "\xEE\x81\x98";
	$PAT[99]->{e_syobon} = '63895.gif';
	
	# ♪
	$PAT[1]->{e_onpu} = "\xF9\x9B";
	$PAT[2]->{e_onpu} = "\xF7\xEE";
	$PAT[3]->{e_onpu} = "\xEE\x8C\xA6";
	$PAT[99]->{e_onpu} = '63899.gif';
	
	# 温泉
	$PAT[1]->{e_onsen} = "\xF9\x9C";
	$PAT[2]->{e_onsen} = "\xF6\x95";
	$PAT[3]->{e_onsen} = "\xEE\x84\xA3";
	$PAT[99]->{e_onsen} = '63900.gif';
	
	# キスマーク
	$PAT[1]->{e_kiss} = "\xF9\x9E";
	$PAT[2]->{e_kiss} = "\xF6\xC4";
	$PAT[3]->{e_kiss} = "\xEE\x80\x83";
	$PAT[99]->{e_kiss} = '63902.gif';
	
	# キラキラ
	$PAT[1]->{e_kirakira} = "\xF9\x9F";
	$PAT[2]->{e_kirakira} = "\xF3\x7E";
	$PAT[3]->{e_kirakira} = "\xEE\x8C\xAE";
	$PAT[99]->{e_kirakira} = '63903.gif';
	
	# ひらめき
	$PAT[1]->{e_idea} = "\xF9\xA0";
	$PAT[2]->{e_idea} = "\xF6\x4E";
	$PAT[3]->{e_idea} = "\xEE\x84\x8F";
	$PAT[99]->{e_idea} = '63904.gif';
	
	# 怒り（ぶちっ）
	$PAT[1]->{e_buti} = "\xF9\xA1";
	$PAT[2]->{e_buti} = "\xF6\xBE";
	$PAT[3]->{e_buti} = "\xEE\x8C\xB4";
	$PAT[99]->{e_buti} = '63905.gif';
	
	# パンチ
	$PAT[1]->{e_panti} = "\xF9\xA2";
	$PAT[2]->{e_panti} = "\xF6\xCC";
	$PAT[3]->{e_panti} = "\xEE\x80\x8D";
	$PAT[99]->{e_panti} = '63906.gif';
	
	# 爆弾
	$PAT[1]->{e_bomb} = "\xF9\xA3";
	$PAT[2]->{e_bomb} = "\xF6\x52";
	$PAT[3]->{e_bomb} = "\xEE\x8C\x91";
	$PAT[99]->{e_bomb} = '63907.gif';
	
	# メロディ
	$PAT[1]->{e_melody} = "\xF9\xA4";
	$PAT[2]->{e_melody} = "\xF6\xDE";
	$PAT[3]->{e_melody} = "\xEE\x8C\xA6";
	$PAT[99]->{e_melody} = '63908.gif';
	
	# 眠い
	$PAT[1]->{e_zzz} = "\xF9\xA6";
	$PAT[2]->{e_zzz} = "\xF6\x4D";
	$PAT[3]->{e_zzz} = "\xEE\x84\xBC";
	$PAT[99]->{e_zzz} = '63910.gif';
	
	# びっくりマーク
	$PAT[1]->{e_bikkuri} = "\xF9\xA7";
	$PAT[2]->{e_bikkuri} = "\xF6\x5A";
	$PAT[3]->{e_bikkuri} = "\xEE\x80\xA1";
	$PAT[99]->{e_bikkuri} = '63911.gif';
	
	# 汗汗
	$PAT[1]->{e_asease} = "\xF9\xAB";
	$PAT[2]->{e_asease} = "\xF7\xCE";
	$PAT[3]->{e_asease} = "\xEE\x8C\xB1";
	$PAT[99]->{e_asease} = '63915.gif';
	
	# ダッシュ
	$PAT[1]->{e_dush} = "\xF9\xAD";
	$PAT[2]->{e_dush} = "\xF6\xCD";
	$PAT[3]->{e_dush} = "\xEE\x8C\xB0";
	$PAT[99]->{e_dush} = '63917.gif';
	
	# 夜
	$PAT[1]->{e_night} = "\xF9\x57";
	$PAT[2]->{e_night} = "\xF3\xC5";
	$PAT[3]->{e_night} = "\xEE\x91\x8B";
	$PAT[99]->{e_night} = '63831.gif';
	
	# シャツ
	$PAT[1]->{e_huku} = "\xF9\xB3";
	$PAT[2]->{e_huku} = "\xF7\xE6";
	$PAT[3]->{e_huku} = "\xEE\x80\x86";
	$PAT[99]->{e_huku} = '63923.gif';
	
	# 口紅
	$PAT[1]->{e_kutibeni} = "\xF9\xB5";
	$PAT[2]->{e_kutibeni} = "\xF6\xE2";
	$PAT[3]->{e_kutibeni} = "\xEE\x8C\x9C";
	$PAT[99]->{e_kutibeni} = '63925.gif';
	
	# チャペル
	$PAT[1]->{e_tyaperu} = "\xF9\xB8";
	$PAT[2]->{e_tyaperu} = "\xF6\xEB";
	$PAT[3]->{e_tyaperu} = "\xEE\x8C\xA5";
	$PAT[99]->{e_tyaperu} = '63928.gif';
	
	# ドル袋
	$PAT[1]->{e_doru} = "\xF9\xBA";
	$PAT[2]->{e_doru} = "\xF6\xA0";
	$PAT[3]->{e_doru} = "\xEE\x84\xAF";
	$PAT[99]->{e_doru} = '63930.gif';
	
	# パソコン
	$PAT[1]->{e_pc} = "\xF9\xBB";
	$PAT[2]->{e_pc} = "\xF7\xE8";
	$PAT[3]->{e_pc} = "\xEE\x80\x8C";
	$PAT[99]->{e_pc} = '63931.gif';
	
	# 王冠
	$PAT[1]->{e_oukan} = "\xF9\xBF";
	$PAT[2]->{e_oukan} = "\xF7\xF9";
	$PAT[3]->{e_oukan} = "\xEE\x84\x8E";
	$PAT[99]->{e_oukan} = '63935.gif';
	
	# 指輪
	$PAT[1]->{e_ring} = "\xF9\xC0";
	$PAT[2]->{e_ring} = "\xF6\xED";
	$PAT[3]->{e_ring} = "\xEE\x80\xB4";
	$PAT[99]->{e_ring} = '63936.gif';
	
	# 自転車
	$PAT[1]->{e_bycicle} = "\xF9\xC2";
	$PAT[2]->{e_bycicle} = "\xF6\x87";
	$PAT[3]->{e_bycicle} = "\xEE\x84\xB6";
	$PAT[99]->{e_bycicle} = '63938.gif';
	
	# 湯呑
	$PAT[1]->{e_otya} = "\xF9\xC3";
	$PAT[2]->{e_otya} = "\xF3\x82";
	$PAT[3]->{e_otya} = "\xEE\x8C\xB8";
	$PAT[99]->{e_otya} = '63939.gif';
	
	# ほっとした顔
	$PAT[1]->{e_tere} = "\xF9\xC6";
	$PAT[2]->{e_tere} = "\xF3\x99";
	$PAT[3]->{e_tere} = "\xEE\x90\x8A";
	$PAT[99]->{e_tere} = '63942.gif';
	
	# 冷汗
	$PAT[1]->{e_hiyaase} = "\xF9\xC8";
	$PAT[2]->{e_hiyaase} = "\xF7\xF6";
	$PAT[3]->{e_hiyaase} = "\xEE\x90\x8F";
	$PAT[99]->{e_hiyaase} = '63943.gif';
	
	# ぷー
	$PAT[1]->{e_pu} = "\xF9\xC9";
	$PAT[2]->{e_pu} = "\xF4\x61";
	$PAT[3]->{e_pu} = "\xEE\x90\x96";
	$PAT[99]->{e_pu} = '63945.gif';
	
	# ボケー
	$PAT[1]->{e_boke} = "\xF9\xCA";
	$PAT[2]->{e_boke} = "\xF3\x9D";
	$PAT[3]->{e_boke} = "\xEE\x90\x8E";
	$PAT[99]->{e_boke} = '63946.gif';
	
	# 目がハート
	$PAT[1]->{e_lovelove} = "\xF9\xCB";
	$PAT[2]->{e_lovelove} = "\xF7\xF4";
	$PAT[3]->{e_lovelove} = "\xEE\x90\x97";
	$PAT[99]->{e_lovelove} = '63947.gif';
	
	# GOOD
	$PAT[1]->{e_good} = "\xF9\xCC";
	$PAT[2]->{e_good} = "\xF6\xD2";
	$PAT[3]->{e_good} = "\xEE\x80\x8E";
	$PAT[99]->{e_good} = '63948.gif';
	
	# あっかんべー
	$PAT[1]->{e_bee} = "\xF9\xCD";
	$PAT[2]->{e_bee} = "\xF6\xC0";
	$PAT[3]->{e_bee} = "\xEE\x84\x85";
	$PAT[99]->{e_bee} = '63949.gif';
	
	# ウインク
	$PAT[1]->{e_wink} = "\xF9\xCE";
	$PAT[2]->{e_wink} = "\xF7\xF3";
	$PAT[3]->{e_wink} = "\xEE\x90\x85";
	$PAT[99]->{e_wink} = '63950.gif';
	
	# 我慢がお
	$PAT[1]->{e_gaman} = "\xF9\xD0";
	$PAT[2]->{e_gaman} = "\xF3\x96";
	$PAT[3]->{e_gaman} = "\xEE\x90\x86";
	$PAT[99]->{e_gaman} = '63952.gif';
	
	# ふっ
	$PAT[1]->{e_hohoemi} = "\xF9\xD1";
	$PAT[2]->{e_hohoemi} = "\xF3\x93";
	$PAT[3]->{e_hohoemi} = "\xEE\x90\x82";
	$PAT[99]->{e_hohoemi} = '63953.gif';
	
	# 泣き顔
	$PAT[1]->{e_nakigao} = "\xF9\xD2";
	$PAT[2]->{e_nakigao} = "\xF6\x4B";
	$PAT[3]->{e_nakigao} = "\xEE\x90\x91";
	$PAT[99]->{e_nakigao} = '63954.gif';
	
	# コピーライト
	$PAT[1]->{e_copyright} = "\xF9\xD6";
	$PAT[2]->{e_copyright} = "\xF7\x74";
	$PAT[3]->{e_copyright} = "\xEE\x89\x8E";
	$PAT[99]->{e_copyright} = '63958.gif';
	
	# トレードマーク
	$PAT[1]->{e_trademark} = "\xF9\xD7";
	$PAT[2]->{e_trademark} = "\xF7\x6A";
	$PAT[3]->{e_trademark} = "\xEE\x94\xB7";
	$PAT[99]->{e_trademark} = '63959.gif';
	
	# マラソン
	$PAT[1]->{e_marathon} = "\xF9\xD8";
	$PAT[2]->{e_marathon} = "\xF6\x43";
	$PAT[3]->{e_marathon} = "\xEE\x84\x95";
	$PAT[99]->{e_marathon} = '63960.gif';
	
	# マル秘
	$PAT[1]->{e_maruhi} = "\xF9\xD9";
	$PAT[2]->{e_maruhi} = "\xF6\xCA";
	$PAT[3]->{e_maruhi} = "\xEE\x8C\x95";
	$PAT[99]->{e_maruhi} = '63961.gif';
	
	# レジスタードトレードマーク
	$PAT[1]->{e_regmark} = "\xF9\xDB";
	$PAT[2]->{e_regmark} = "\xF7\x75";
	$PAT[3]->{e_regmark} = "\xEE\x89\x8F";
	$PAT[99]->{e_regmark} = '63963.gif';
	
	# 危険
	$PAT[1]->{e_danger} = "\xF9\xDC";
	$PAT[2]->{e_danger} = "\xF6\x59";
	$PAT[3]->{e_danger} = "\xEE\x89\x92";
	$PAT[99]->{e_danger} = '63964.gif';
	
	# 空室
	$PAT[1]->{e_akimark} = "\xF9\xDE";
	$PAT[2]->{e_akimark} = "\xF3\x5D";
	$PAT[3]->{e_akimark} = "\xEE\x88\xAB";
	$PAT[99]->{e_akimark} = '63966.gif';
	
	# 満室マーク
	$PAT[1]->{e_manmark} = "\xF9\xE0";
	$PAT[2]->{e_manmark} = "\xF3\x5C";
	$PAT[3]->{e_manmark} = "\xEE\x88\xAA";
	$PAT[99]->{e_manmark} = '63968.gif';
	
	# 学校
	$PAT[1]->{e_school} = "\xF9\xE3";
	$PAT[2]->{e_school} = "\xF3\x53";
	$PAT[3]->{e_school} = "\xEE\x85\x97";
	$PAT[99]->{e_school} = '63971.gif';
	
	# 波
	$PAT[1]->{e_wave} = "\xF9\xE4";
	$PAT[2]->{e_wave} = "\xF4\x81";
	$PAT[3]->{e_wave} = "\xEE\x90\xBE";
	$PAT[99]->{e_wave} = '63972.gif';
	
	# 富士山
	$PAT[1]->{e_fuji} = "\xF9\xE5";
	$PAT[2]->{e_fuji} = "\xF7\xED";
	$PAT[3]->{e_fuji} = "\xEE\x80\xBB";
	$PAT[99]->{e_fuji} = '63973.gif';
	
	# クローバー
	$PAT[1]->{e_clover} = "\xF9\xE6";
	$PAT[2]->{e_clover} = "\xF6\xEC";
	$PAT[3]->{e_clover} = "\xEE\x84\x90";
	$PAT[99]->{e_clover} = '63974.gif';
	
	# チューリップ
	$PAT[1]->{e_tulip} = "\xF9\xE8";
	$PAT[2]->{e_tulip} = "\xF6\xBD";
	$PAT[3]->{e_tulip} = "\xEE\x8C\x84";
	$PAT[99]->{e_tulip} = '63976.gif';
	
	# リンゴ
	$PAT[1]->{e_apple} = "\xF9\xEA";
	$PAT[2]->{e_apple} = "\xF3\x8D";
	$PAT[3]->{e_apple} = "\xEE\x8D\x85";
	$PAT[99]->{e_apple} = '63978.gif';
	
	# 紅葉
	$PAT[1]->{e_momiji} = "\xF9\xEC";
	$PAT[2]->{e_momiji} = "\xF6\xA7";
	$PAT[3]->{e_momiji} = "\xEE\x84\x98";
	$PAT[99]->{e_momiji} = '63980.gif';
	
	# 桜
	$PAT[1]->{e_sakura} = "\xF9\xED";
	$PAT[2]->{e_sakura} = "\xF6\xA3";
	$PAT[3]->{e_sakura} = "\xEE\x80\xB0";
	$PAT[99]->{e_sakura} = '63981.gif';
	
	# おにぎり
	$PAT[1]->{e_onigiri} = "\xF9\xEE";
	$PAT[2]->{e_onigiri} = "\xF6\xAE";
	$PAT[3]->{e_onigiri} = "\xEE\x8D\x82";
	$PAT[99]->{e_onigiri} = '63982.gif';
	
	# ショートケーキ
	$PAT[1]->{e_shortcake} = "\xF9\xEF";
	$PAT[2]->{e_shortcake} = "\xF6\xA9";
	$PAT[3]->{e_shortcake} = "\xEE\x81\x86";
	$PAT[99]->{e_shortcake} = '63983.gif';
	
	# とっくり
	$PAT[1]->{e_tokkuri} = "\xF9\xF0";
	$PAT[2]->{e_tokkuri} = "\xF3\x6A";
	$PAT[3]->{e_tokkuri} = "\xEE\x8C\x8B";
	$PAT[99]->{e_tokkuri} = '63984.gif';
	
	# ラーメン
	$PAT[1]->{e_raamen} = "\xF9\xF1";
	$PAT[2]->{e_raamen} = "\xF7\xD1";
	$PAT[3]->{e_raamen} = "\xEE\x8D\x80";
	$PAT[99]->{e_raamen} = '63985.gif';
	
	# パン
	$PAT[1]->{e_bread} = "\xF9\xF2";
	$PAT[2]->{e_bread} = "\xF3\x83";
	$PAT[3]->{e_bread} = "\xEE\x8C\xB9";
	$PAT[99]->{e_bread} = '63986.gif';
	
	# ひよこ
	$PAT[1]->{e_hiyoko} = "\xF9\xF4";
	$PAT[2]->{e_hiyoko} = "\xF6\xB9";
	$PAT[3]->{e_hiyoko} = "\xEE\x94\xA3";
	$PAT[99]->{e_hiyoko} = '63988.gif';
	
	# ペンギン
	$PAT[1]->{e_pengin} = "\xF9\xF5";
	$PAT[2]->{e_pengin} = "\xF6\xB5";
	$PAT[3]->{e_pengin} = "\xEE\x81\x95";
	$PAT[99]->{e_pengin} = '63989.gif';
	
	# 馬
	$PAT[1]->{e_uma} = "\xF9\xF9";
	$PAT[2]->{e_uma} = "\xF6\xB1";
	$PAT[3]->{e_uma} = "\xEE\x84\xB4";
	$PAT[99]->{e_uma} = '63993.gif';
	
	# 豚
	$PAT[1]->{e_buta} = "\xF9\xFA";
	$PAT[2]->{e_buta} = "\xF6\xB7";
	$PAT[3]->{e_buta} = "\xEE\x84\x8B";
	$PAT[99]->{e_buta} = '63994.gif';
	
	
	
	
	
	return $PAT[$paturn];
}

1;
