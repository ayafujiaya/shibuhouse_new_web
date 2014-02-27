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
my $query = new CGI;
my %FORM = &form_multi($query);
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);

my $data_ref;

my $data;
if ($FORM{data}) {
	# アップロードデータ受取
	my $buffer;
	while(read($FORM{data}, $buffer, 2048)){ 
		$data .= $buffer;
	}
		
	if ($FORM{'mode'} eq "admin") {
		# 管理者データ
		my $file = $SYS->{data_dir}."admin.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "freecol") {
		# 自由項目データ
		my $file = $SYS->{data_dir}."freecol.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "errmail") {
		# エラーメール
		my $file = $SYS->{data_dir}."errmail.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "form") {
		# 自動返信メール
		my $file = $SYS->{data_dir}."form.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "template") {
		# 配信テンプレート
		my $file = $SYS->{data_dir}."template.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "hist") {
		# 履歴データ
		my $file = $SYS->{data_dir}."hist.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "dispcol") {
		# 検索用表示項目
		my $file = $SYS->{data_dir}."dispcol.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "license") {
		# 検索用表示項目
		my $file = $SYS->{data_dir}."enc.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "autoform") {
		# フォーム設定データ
		my $file = $SYS->{data_dir}."autoform.cgi";
		$objAcData->UpdateFile($file, $data);
	}
	# リロード
	print "Location: import.cgi?okedit=1 \n\n";
	exit;

} elsif ($FORM{mode}) {
	$data_ref->{error_message} = "ファイルを選択してください。";
}


# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# フォームの値
$data_ref->{form} = \%FORM;

# HTML表示
&printhtml_tk($data_ref);
exit;
