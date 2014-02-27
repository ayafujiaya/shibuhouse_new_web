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
my $data_ref;

# 配信停止
if ($FORM{mode} eq "send_stop" && $FORM{over_count}) {
	
	my %STOP;
	# データ取得
	my @DATA = $objAcData->GetErrorMailLoopData();
	foreach my $row (@DATA){
		# 削除回数制限
		if ($FORM{over_count} && $FORM{over_count} > $row->{count}) { next; }
		$STOP{"send_flg".$row->{email}} = 0;
		$STOP{"hid_email".$row->{email}} = 1;
	}
	# 配信停止
	$objAcData->UpdMailStatus(\%FORM);
	
} elsif ($FORM{mode} eq "alldel") {
	# 不着処理
	$objAcData->error_mail_hist_alldel($admindata);
} elsif ($FORM{mode} eq "scan") {
	# 不着処理
	$objAcData->error_mail_work($admindata);
} elsif ($FORM{mode} eq "csv") {
	# CSVダウンロード
	
	my $mail = "E-MAIL,不着回数\n";

	#フォーム送信先一覧
	my @DATA = $objAcData->GetErrorMailLoopData();

	foreach my $row (@DATA){
		
		# 削除回数制限
		if ($FORM{over_count} && $FORM{over_count} > $row->{count}) { next; }
		
		$mail .= "$row->{email},$row->{count}\n";
	}
	
	&jcode::convert(\$mail, "sjis", "euc");
	my %DATE = &getdatetime;

	my $size = length $mail;
	print "Content-Type: application/octet-stream\n"; 
	print "Content-Disposition: attachment; filename=errmaildata$DATE{year}$DATE{mon}$DATE{mday}.csv\n"; 
	print "Content-Length: $size\n\n"; 
	print $mail;
	exit;
	
}


# エラーメールデータ取得
my @DATA = $objAcData->GetErrorMailLoopData();

my @data;
foreach my $row (@DATA){
	# 削除回数制限
	if ($FORM{over_count} && $FORM{over_count} > $row->{count}) { next; }
	push (@data,$row);
}
# ページング処理
my $objPaging = new clsPaging($FORM{dispnum}, $FORM{page}, '&search=1&over_count='.$FORM{'over_count'});
@data = $objPaging->MakePaging(\@data, \$data_ref);
$data_ref->{loop} = \@data;

$data_ref->{search_url} = '&over_count='.$FORM{over_count};

$data_ref->{oktext} = "$FORM{delnum}件削除されました。" if $FORM{okdel};

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
