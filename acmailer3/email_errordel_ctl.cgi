#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# クッキーよりセッションデータ取得
my %COOKIE = &getcookie;
my %S = getsession($COOKIE{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my %FORM = &form("noexchange");
my $regdata;

# データ取得
my @MAIL = $objAcData->GetData('mail', 'MAIL');
my $col = $objAcData->{MAIL_COL};
my @col = @$col;
foreach my $row (@MAIL){
	#エラーカウント
	if(!CheckMailAddress($row->{email})){
		#削除処理
	}else{
		foreach my $n (@col) {
			$regdata .= $row->{$n}."\t";
		}
		$regdata .= "\n";
	}
}

# データ更新
my $file = $objAcData->{DATA_DIR}."mail.cgi";

# データ上書き
$objAcData->UpdateFile($file, $regdata);

# ページジャンプ
print "Location: $SYS->{homeurl_ssl}email_list.cgi?okerrordel=1\n\n";
exit;
