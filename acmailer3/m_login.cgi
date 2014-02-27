#!/usr/bin/perl

our $SYS;
use lib "./lib/";
require "./lib/setup.cgi";
use strict;

# 管理情報取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();
my $data_ref = $admindata;



if ($data_ref->{login_id} && $data_ref->{login_pass}) {
	# HTMLテンプレートオープン


} else {
	print "Content-type: text/html; charset=EUC-JP\n\n";
	print "パソコン用ログイン画面より初期設定を行ってください。";
	exit;
}

my %FORM = &form();

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref, "", 1);
exit;
