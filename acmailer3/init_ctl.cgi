#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
use MailSession;
our $SYS;

my $objAcData = new clsAcData($SYS->{data_dir});

my %COOKIE = &getcookie;
my $sid = decrypt_id($COOKIE{sid});
my $session_fn = $SYS->{dir_session}.".".$sid.".cgi";
my %FORM = &form;

my $data_ref;

# エラーチェック
if (&error_check(\%FORM, \$data_ref->{error_message})) {
	# 初期値設定
	# タイトル
	$FORM{title} = 'ACMAILER3.8';
	# カウンター表示
	$FORM{counter_disp} = 1;
	# バックナンバー表示
	$FORM{backnumber_disp} = 1;
	# バックナンバー表示件数
	$FORM{backnumber_num} = 10;
	# 登録ユーザに自動返信メールを送る
	$FORM{merumaga_usermail} = 1;
	# 管理者にメールを送る
	$FORM{merumaga_adminmail} = 1;
	# ダブルオプトイン
	$FORM{double_opt} = "";
	# 削除時の動作
	$FORM{delmode} = "del";
	# 重複データの登録
	$FORM{double_reg} = "";
	# 機種依存文字チェック
	$FORM{str_check} = 1;
	# 送信モード(ノーマル)
	$FORM{send_type} = "0";
	# ローカルサーバー
	$FORM{relay_use} = "";
	# 不着ログ保存件数
	$FORM{errmail_log_num} = 10;
	# 削除確認はデフォルトON
	$FORM{delconfirm} = 1;
        # sendmailのiオプション
        $FORM{sendmail_i_option} = 1;
	# トップページメモ
	$FORM{free_memo} = '<img src="img/acgirl_top.jpg" />

※こちらはメモ代わりにも使えるように「各種設定」→「トップページメモ」にて編集ができます。



ver.3.8.15 バージョンアップ内容 2014/02/12
■修正
メール配信設定時のページ遷移の不具合を修正



ver.3.8.14 バージョンアップ内容 2013/03/21
■修正
Return-Path設定処理の不具合を修正



ver.3.8.13 バージョンアップ内容 2012/08/02
■改修
CSV登録にオプションを追加



ver.3.8.12 バージョンアップ内容 2011/11/15
■修正
メールアドレスに改行が入っている場合、登録処理時に起こる不具合を修正



ver.3.8.11 バージョンアップ内容 2011/10/20
■修正
メニュー表示の不具合を修正



ver.3.8.10 バージョンアップ内容 2011/10/18
■修正
メール登録時の文字コード変換処理の不具合を修正



ver.3.8.9 バージョンアップ内容 2011/09/21
■修正
携帯からのメール配信処理の不具合を修正
HTML/デコメールプレビュー機能の不具合を修正
特定の条件でメール本文が途切れてしまう不具合を修正

■追加機能
メールコマンドオプション設定追加


ver.3.8.8 バージョンアップ内容 2011/07/08
■修正
予約配信時日付チェックの不具合修正
メールアドレス管理ページのページング処理の不具合修正
Softbankのかに座の絵文字コードを修正
メール配信セッションの不具合修正

ver.3.8.7 バージョンアップ内容 2011/03/10
■修正
長文を送信した場合に機種依存文字がなくてもチェックに引っかかる不具合修正

ver.3.8.6 バージョンアップ内容 2011/01/25
■追加機能
予約編集機能を追加

ver.3.8.5 バージョンアップ内容 2010/12/27
■修正
再登録防止機能を搭載。

ver.3.8.4 バージョンアップ内容 2010/12/17
■修正
携帯版管理画面よりDOCOMO端末で送信を行うと失敗する不具合修正

ver.3.8.3 バージョンアップ内容 2010/12/01
■修正
テストメール送信で数万件のデータが保存されている場合にタイムアウトになる不具合修正
メールアドレス一括登録の際に大文字を小文字に変換されない不具合修正

ver.3.8.2 バージョンアップ内容 2010/10/18
■修正
PC版の予約配信完了画面が表示されない不具合修正

ver.3.8.1 バージョンアップ内容 2010/10/14
■修正
携帯管理画面の予約配信完了画面がPCのモードで表示される不具合修正


';
	# 携帯ドメイン
	$FORM{mobiledomain} = 'docomo.ne.jp
ezweb.ne.jp
softbank.ne.jp
vodafone.ne.jp
disney.ne.jp';
	
	# sendmailpathの中にqmailが含まれている場合はqmailにチェック
	my $qmailpath = `ls -l $FORM{sendmail_path}`;
	if ($qmailpath =~ /qmail/) {
		$FORM{qmail} = 1;
	}
	
	# 管理者データ更新
	$objAcData->UpdAdminData(\%FORM);
	# 自由項目更新
	$objAcData->UpdFreeColData(\%FORM);
	
	# 初期は管理者のメールアドレス
	$FORM{email} = $FORM{admin_email};
	# 新規登録時の日付セット
	my %TIME = &getdatetime();
	$FORM{'add_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	$FORM{'edit_date'} = $FORM{'add_date'};
	
	$objAcData->RegEmail(\%FORM);

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
            if((time - 86400) > ((stat("$SYS->{dir_session}$_"))[9])){
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
	
	my ($secg, $ming, $hourg, $mdayg, $mong, $yearg, $wdayg) = gmtime(time + (86400*3));
	my @mons = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
	my @week = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
	my $cookieexpires = sprintf("%s\, %02d-%s-%04d %02d:%02d:%02d GMT", $week[$wdayg], $mdayg, $mons[$mong], $yearg+1900, $hourg, $ming, $secg);
	print "Set-Cookie: sid=$sid_ec; path=/; \n";

	print "Location: $SYS->{homeurl_ssl}index.cgi\n\n";
	exit;


} else {
	foreach my $n (keys %FORM) {
		$data_ref->{$n} = $FORM{$n};
	}
	
	# フォームの値
	$data_ref->{form} = \%FORM;

	# HTML表示
	&printhtml_tk($data_ref, "tmpl/init.tmpl");
	exit;

}

# エラーチェック
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my %FORM = %$p_FORM;
	my @error;
	
	#エラーチェック
	if (!$FORM{admin_name}) {
		push(@error, "・差出人名を入力してください。");
	#} elsif ($FORM{admin_name} =~ /[\"\'\@\;\:\,\.\<\>\\\[\]]/) {
	} elsif ($FORM{admin_name} =~ /[\"\'\<\>]/) {
		# 使用できない文字は "'<>に変更
		push(@error, "差出人名の中に「'」「\"」「<」「>」は使用できません。");
	}
	push(@error, "・メール差出人メールアドレスを入力してください。") if !$FORM{admin_email};
	if (!CheckMailAddress($FORM{admin_email})) {
		push(@error, "・メール差出人メールアドレスを正しく入力してください。");
	}
	push(@error, "・ログインIDを入力してください。") if !$FORM{login_id};
	push(@error, "・パスワードを入力してください。") if !$FORM{login_pass};
	if($FORM{login_id} && ($FORM{login_id} !~ /^[0-9a-zA-Z_\-]+$/ || length($FORM{login_id}) > 12)){
		push(@error, "・IDは半角英数字で12桁以内でご指定下さい。");
	}
	if($FORM{login_pass} && ($FORM{login_pass} !~ /^[0-9a-zA-Z_\-]+$/ || length($FORM{login_pass}) > 12)){
		push(@error, "・パスワードは半角英数字で12桁以内でご指定下さい。");
	}

	if ($FORM{homeurl} && $FORM{homeurl} !~ /^http\:\/\/.*/) {
		push(@error, "・CGI設置URLはhttps://www.acmailer.jp/acmailer/のような形式で入力してください。");
	} elsif ($FORM{homeurl} !~ /^.*\/$/) {
		$$p_FORM{homeurl} .= "/";
	}

	if ($FORM{mypath} && $FORM{mypath} !~ /\/$/) {
		$$p_FORM{mypath} .= "/";
	}
	
	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;
	
}
