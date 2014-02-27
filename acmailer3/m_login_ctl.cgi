#!/usr/bin/perl

use lib "./lib/";
require './lib/setup.cgi';
use strict;
use MailSession;

our $SYS;

my %COOKIE = &getcookie;
my $sid = decrypt_id($COOKIE{sid});
my $session_fn = $SYS->{dir_session}.".".$sid.".cgi";

my %FORM = &form;

# 入力データチェック
my $errordata;
$errordata .= "・ログインIDを入力してください。<br>" if !$FORM{login_id};
$errordata .= "・パスワードを入力してください。<br>" if !$FORM{login_pass};
&error("$errordata") if $errordata;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();


if($admindata->{login_id} eq $FORM{login_id} && $admindata->{login_pass} eq $FORM{login_pass}){ 
}else{
	&error("ID,PWをご確認下さい。");
}


# メールセッション
my $mail_session = MailSession->new(
    session_dir => $SYS->{dir_session_mail}
);

# 古いメールセッションデータ削除
$mail_session->delete_old_session_file();


# 古いセッションデーター削除
my @temp_files;
opendir(DIR, $SYS->{dir_session});
@temp_files = (grep !/^\.\.?$/,readdir DIR);
closedir(DIR);
foreach(@temp_files){
    next if $_ eq '.htaccess';
    if ((time - 86400) > ((stat("$SYS->{dir_session}$_"))[9])) {
        unlink "$SYS->{dir_session}$_";
    }
}
# フォームデーター整形
my %S;
$S{login_id} = $FORM{login_id};
$S{login_pass} = $FORM{login_pass};

my %TIME = &getdatetime;
# ファイルを使わず、pidでの場合
$sid = "$TIME{sec}".$$;

my $sid_e = encrypt_id($sid);
my $sid_ec = $sid_e;
$sid_ec =~ s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;

# セッション保存
&setsession($sid_e,%S);

$FORM{login_id} =~ s/%([a-f\d]{2})/pack 'H2',$1/egi;

# クッキー書き込み
if($FORM{memory}){
	my ($secg, $ming, $hourg, $mdayg, $mong, $yearg, $wdayg) = gmtime(time + (86400*30));
	my @mons = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
	my @week = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
	my $cookieexpires = sprintf("%s\, %02d-%s-%04d %02d:%02d:%02d GMT", $week[$wdayg], $mdayg, $mons[$mong], $yearg+1900, $hourg, $ming, $secg);
	
	print "Set-Cookie: sid=$sid_ec; path=/; \n";

}else{
	
	my ($secg, $ming, $hourg, $mdayg, $mong, $yearg, $wdayg) = gmtime(time + (86400*3));
	my @mons = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
	my @week = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
	my $cookieexpires = sprintf("%s\, %02d-%s-%04d %02d:%02d:%02d GMT", $week[$wdayg], $mdayg, $mons[$mong], $yearg+1900, $hourg, $ming, $secg);
	print "Set-Cookie: sid=$sid_ec; path=/; \n";
}

print "Location: $SYS->{homeurl_ssl}index.cgi?sid=$sid_ec \n\n";
exit;
