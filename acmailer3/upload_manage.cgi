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

#my %FORM = &form_multi();

my %FORM;
my $query = new CGI;
my @names = $query->param;
foreach(@names){
	$FORM{$_} =  $query->param($_);
}

my $row = $admindata;
my $data_ref;

if ($FORM{imagefile}) {
	UploadFile(\$FORM{imagefile});
	$data_ref->{uploadok} = 1;
}

if ($FORM{mode} eq "delete" && $FORM{file_name}) {
	if (-e './upload/'.$FORM{file_name}) {
		unlink('./upload/'.$FORM{file_name});
	}
	$data_ref->{delok} = 1;
}

# アップロードされているファイル一覧取得
my @f = &get_uploadimage();
foreach my $ref (@f) {
	$ref->{file_name_urlenco} = &urlencode($ref->{file_name});
}
$data_ref->{file_list} = \@f;


# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
