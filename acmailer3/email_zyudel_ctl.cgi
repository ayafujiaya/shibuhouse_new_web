#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# セッションデータ取得とログインチェック
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my ($data_ref, $regdata);

#ファイルオープン
my @MAIL = $objAcData->GetData('mail', 'MAIL');
my %ZYU;
my $col = $objAcData->{MAIL_COL};
my @col = @$col;
foreach my $row (@MAIL){
	#重複カウント
	if($ZYU{$row->{email}}){
		#削除処理
	}else{
		foreach my $n (@col) {
			$regdata .= $row->{$n}."\t";
		}
		$regdata .= "\n";
	}
	$ZYU{$row->{email}}++;
}

# データ更新
my $file = $objAcData->{DATA_DIR}."mail.cgi";

# データ上書き
$objAcData->UpdateFile($file, $regdata);

# ページジャンプ
print "Location: $SYS->{homeurl_ssl}email_list.cgi?okzyudel=1\n\n";
exit;
