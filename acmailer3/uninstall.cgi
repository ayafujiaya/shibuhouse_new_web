#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
$|=1;

select(STDOUT);
$|=1;
select(STDOUT);

our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# クッキーよりセッションデータ取得
my %COOKIE = &getcookie;
my %S = getsession($COOKIE{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

$SYS->{mypath} = $admindata->{mypath};

my %FORM = &form();

if ($FORM{uninstall}) {
	# アンインストール作業
	&uninstall($admindata);
	
}


# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;



# アンインストール作業
sub uninstall {
	my $admindata = shift;
	
	# 削除するパスがあっているか検証
	if (!$admindata->{mypath} || !-e $admindata->{mypath}."lib/setup.cgi") {
		&error("CGI設置パスが不正です。各種設定の「システム設定」→「CGI設置パス」を確認して更新ボタンを押してください。");
	}
	
	print "Content-type: text/html; charset=EUC-JP\n\n";
	
	# ファイル数取得
	&file_delete($admindata->{mypath}, "");
	
	# 自分自身のディレクトリすべて削除
	&file_delete($admindata->{mypath}, "1");
	
	print "<center><b>ACMAILERのご使用ありがとうございました。</b><br><br>dataディレクリとsessionディレクトリを削除しました。<br>";
	print "インストール先のディレクトリを削除してアンインストール完了となります。</center>";
	
	# 最後に自分自身を削除
	unlink('./uninstall.cgi');
	
	exit;
}

# ファイルを削除
sub file_delete() {
	my $dir = shift;
	my $mode = shift;
	
	opendir DATA, $dir;
	my @files = readdir DATA;
	closedir DATA;
	
	foreach my $fn(@files) {
		if ($fn eq "." || $fn eq "..") { next; }
		if (-d $dir.$fn) {
			# ACMAILERのdataディレクトリとsessionディレクトリの場合だけ
			if ($fn eq "data" || $fn eq "session") {
				# ディレクトリの場合
				#&file_delete($dir.$fn."/", $mode);
				`rm -r $dir$fn`;
			}
		} else {
			## ファイルの場合
			#if ($fn eq "uninstall.cgi") { next; }
			#if ($dir =~ /$SYS->{mypath}/ && $mode) {
			#	unlink($dir.$fn);
			#	$SYS->{delnowcount}++;
			#	my $per = ($SYS->{delnowcount} / $SYS->{delcount}) * 100;
			#	
			#} elsif (!$mode) {
			#	$SYS->{delcount}++;
			#}
		}
	}
	if ($dir =~ /$SYS->{mypath}/ && $mode) {
		
		rmdir($dir);
		$SYS->{delnowcount}++;
		my $per = ($SYS->{delnowcount} / $SYS->{delcount}) * 100;
		
	} elsif (!$mode) {
		$SYS->{delcount}++;
	}
	return 1;
}
