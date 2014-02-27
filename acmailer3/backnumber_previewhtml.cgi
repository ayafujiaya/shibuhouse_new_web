#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;
my %FORM = &form("noexchange");

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# 共通変数読み込み
my $li;
&set_common_value(\$li, $admindata);

&writing_check(\$SYS);

# アクセス制限なし
#&limit_access('backnumber.cgi,m_backnumber.cgi');

if (!$admindata->{backnumber_disp}) {
	&error("表示できません。");
}

if (!$FORM{id}) {
	&error("パラメータエラーです。");
}

print "Content-type: text/html; charset=EUC-JP\n\n";
print '<html><head><title>プレビュー</title></head><body>';


# 履歴データ取得
my $row = $objAcData->GetData('hist', 'HIST', $FORM{id});
my $max = $admindata->{backnumber_num};

my $data_ref;


if ($row->{mail_type} eq "plain") {
	print "テキストメールです。";
	exit;
} else {
	$row->{mail_body} =~ s/__<<equal>>__/\=/gi;
	$row->{mail_body} =~ s/__<<semicolon>>__/;/gi;
	$row->{mail_body} =~ s/__<<BR>>__/<BR>/gi;

	# 絵文字
	$row->{mail_body} = &ReplaceEmojiDisp($row->{mail_body});
	$row->{mail_title} = &ReplaceEmojiDisp($row->{mail_title});

	# 画像埋め込み
	$row->{mail_body} = &ReplaceImageDisp($row->{mail_body});
	
	print $row->{mail_body};
}


if (!$li->{writing}) {
	print '
<div align="center"></div>
<div align="center">
<!-- ■■■■■■著作権について（重要！）■■■■■■ -->
<!-- 本システムは、AHREF(エーエイチレフ)に無断で下記著作権表示を削除・改変・非表示にすることは禁止しております -->
<!-- 著作権非表示に関しては、こちらをご確認下さい。 -->
<!-- http://www.ahref.org/cgityosaku.html -->
<!-- ■■■■■■■■■■■■■■■■■■■■■■■■ -->
<font size="-2" color=#999999>メルマガ配信CGI <a href="http://www.ahref.org/" title="メルマガ配信CGI ACMAILER" target="_blank">ACMAILER</a> Copyright (C) 2008 <a href="http://www.ahref.org/" target="_blank" title="エーエイチレフ">ahref.org</a> All Rights Reserved.
</font>
</div>
</div>';
}

print '</body></html>';
exit;
