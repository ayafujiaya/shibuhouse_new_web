#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use clsMail;
use strict;
use MailSession;

our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

&writing_check(\$SYS);

# セッションデータ取得とログインチェック
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

# 管理画面の設定が行われているかどうか
&CheckAdminData_MailSend($admindata);


# メールセッション
my $mail_session = MailSession->new(
    mail_id     => $FORM{mail_session_id},
    session_dir => $SYS->{dir_session_mail}
);
$FORM{mail_title} = $mail_session->get('mail_title');
$FORM{mail_body} = $mail_session->get('mail_body');
$FORM{mail_title} =~ s/__<<equal>>__/\=/gi;
$FORM{mail_body} =~ s/__<<equal>>__/\=/gi;
$FORM{mail_title} =~ s/__<<semicolon>>__/;/gi;
$FORM{mail_body} =~ s/__<<semicolon>>__/;/gi;

# 送信用データ取得
if ($FORM{sid}) { $COOKIE{sid} = $FORM{sid}; }
my $objAcDataSender = new clsAcData($SYS->{dir_session});
my $sender_data = $objAcDataSender->getSenderData($mail_session->mail_id());


if ($sender_data eq "") {
	&error("送り先がありません。");
}

if (!$FORM{mail_title}) { &error("件名を入力してください。"); }
if (!$FORM{mail_body}) { &error("本文を入力してください。"); }
$data_ref = $admindata;

# 予約配信の場合
if ($FORM{reserve_mode}) {
	# 予約時間チェック
	my %TIME = &getdatetime();
	if (!$FORM{send_year} || !$FORM{send_mon} || !$FORM{send_day} || $FORM{send_hour} eq "" || $FORM{send_min} eq "") { &error("予約配信の設定の場合は配信日時を選択してください。"); }
	# 現在より時間が後の場合
	if ("$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}" > sprintf("%04d%02d%02d%02d%02d", $FORM{send_year}, $FORM{send_mon}, $FORM{send_day}, $FORM{send_hour}, $FORM{send_min})) {
	#	&error("配信日時の設定が現在より過去になっています。");
	}
}

#件名
$data_ref->{mail_title} = &plantext2html($FORM{mail_title},"nobr");
$data_ref->{mail_title_html} = &plantext2html($FORM{mail_title});

#本文
$data_ref->{mail_body} = &plantext2html($FORM{mail_body},"nobr");
$data_ref->{mail_body_html} = &plantext2html($FORM{mail_body});

# 送信先一覧
my @DATA = split(/\n/, $sender_data);
my @data;
my $i;

foreach(@DATA){
	if (!$_) { next; }
	$_ =~ s/__<<equal>>__/\=/gi;
	$_ =~ s/__<<semicolon>>__/;/gi;
	my $row;
	
	my @d = split(/\t/,$_);
	my $col = $objAcData->{MAIL_COL};
	my @col = @$col;
	my $j = 0;
	foreach my $n (@col) {
		$row->{$n} = $d[$j];
		$j++;
	}
	
	# 配信停止は無視
	if (!$row->{status}) { next; }
	
	$row->{subject} = $FORM{mail_title};
	$row->{body} = $FORM{mail_body};
	
	# 改行コード制御
	if ($FORM{mail_type} eq "plain") {
		$row->{subject} =~ s/__<<BR>>__/\n/gi;
		$row->{body} =~ s/__<<BR>>__/\n/gi;
	} else {
		$row->{subject} =~ s/__<<BR>>__/<BR>/gi;
		$row->{body} =~ s/__<<BR>>__/<BR>/gi;
	}
	
	# 置換
	$row->{subject} = $objAcData->ReplaceMailBody($row->{subject}, $admindata, $row, $SYS->{max_colnum});
	$row->{body} = $objAcData->ReplaceMailBody($row->{body}, $admindata, $row, $SYS->{max_colnum});
	
	
	
	$row->{num} = ($i + 1);
	push (@data,$row);
	$i++;
}

#配信テスト
if($FORM{send_test}){
	&sendmail_admin(@data);
	exit;
}

# 携帯の場合は予約以外はバックグランド強制
if (!$FORM{reserve_mode} && $FORM{sid}) {
	$admindata->{send_type} = 2;
}

# デコメールで送ったかどうかを記憶する
$FORM{'deco_mode'} = $mail_session->get('email_send_mode');

# メール送信
if ($FORM{reserve_mode}) {
	# 予約配信
	&reserve(@data);
} elsif ($admindata->{send_type} == 1 && $admindata->{divnum} =~ /^[0-9]+$/ && $admindata->{divnum} > 0){
	&sendmail_div(@data);
}elsif($admindata->{send_type} == 0){
	&sendmail(@data);
}elsif($admindata->{send_type} == 2){

	# バックグランド処理
	my @NEWDATA_ORG = @data;
	
	if (!$FORM{starttime}) {
		my %STIME = &getdatetime();
		$FORM{starttime} = "$STIME{year}$STIME{mon}$STIME{mday}$STIME{hour}$STIME{min}$STIME{sec}";
	}
	

	# 履歴データに書き込み------------------------------------------
	my $id = time.$$;
	$FORM{id} = $id;
	$FORM{start_send_date} = $FORM{starttime};
	$FORM{status} = 1;
	$FORM{send_type} = $admindata->{send_type};
	for(1..5) {
		$FORM{"search".$_}      .= $mail_session->get("search".$_);	# 絞込みカラム
		$FORM{"search_text".$_} .= $mail_session->get("search_text".$_);		# 絞込みテキスト
		$FORM{"searchlike".$_}   = $mail_session->get("searchlike".$_);
	}
	$FORM{'search_domain'} = $mail_session->get('search_domain');
	$FORM{'andor'} = $mail_session->get('andor');
	$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
	# 書き込み
	$objAcData->InsData('hist', 'HIST', \%FORM);
	#------------------------------------------------------------------
	

	my $pid;
	# 処理をバックグラウンドでする
	FORK: {
		if ($pid = fork) {
			my $sid = "";
			if ($FORM{sid}) { $sid = "sid=".$FORM{sid}; }
			print "Location:email_send_finish.cgi?$sid \n\n";
			
			# STDOUTを閉じないと、apacheが終了statusを返さないらしい。よって、ブラウザが開放されない。
			close(STDOUT);
			close(STDERR);
			close(STDIN);
			# 子プロセスの終了を待っていないと、子がZombieになってまうらしい
			wait;
		} elsif (defined $pid) {
			# バックグラウンド処理
		
			close(STDOUT);
			close(STDERR);
			close(STDIN);
			my $c = 1;
			
			my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));

			my $return_path = $admindata->{admin_email};
			if ($admindata->{errmail} && $admindata->{errmail_email}) {
				$return_path = $admindata->{errmail_email};
			}
			my @hist;
			my $objMail = create_clsMail($admindata);
			foreach my $row (@NEWDATA_ORG){
				my $return = 1;
				$return = $objMail->send($admindata->{sendmail_path},$row->{email},$row->{subject},$row->{body},$sendername,$admindata->{admin_email},"",$return_path, $FORM{mail_type}, $id);
				
				# 一定間隔待つ
				if ($admindata->{'send_span'}) { select(undef, undef, undef, $admindata->{'send_span'}); }
				
				if ($return){
					my $hist;
					$hist->{email} = $row->{email};
					push(@hist, $hist);
				}else{
					
				}
				$c++;
			}
			
			# 履歴データに最終書き込み
			my %TIME = &getdatetime();
			
			# 対象データ取得
			my $target = $objAcData->GetData('hist', 'HIST', $id);
			my %UPDATE;
			foreach my $n (keys %$target) {
				$UPDATE{$n} = $target->{$n};
			}
			$UPDATE{end_send_date} = "$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}$TIME{sec}";	# 送信終了時間
			$UPDATE{backnumber} = 1;
			$UPDATE{status} = 2;
			$UPDATE{total_count} = ($c - 1);
			# 更新
			$objAcData->UpdData('hist', 'HIST', $id, \%UPDATE);
			
			# セッションクリア
			&clear_mailsession();
			exit;
		} elsif ($! =~ /No more process/) {
			# プロセスが多すぎる場合、時間を置いて再チャレンジ
			sleep 5;
			redo FORK;
		} else {
			# ここにくることはない
			die "Can't fork: $\n";
		}
	}
}
&error("システムエラーです。送信タイプを各種設定で設定してください。");
exit;


sub sendmail{
	my @NEWDATA_ORG = @_;
	
	# 何件送れば一時休憩に入るか
	my $waitspan = 30;
	# 休憩時間
	my $waittime = 3;
	
	if (!$FORM{starttime}) {
		my %STIME = &getdatetime();
		$FORM{starttime} = "$STIME{year}$STIME{mon}$STIME{mday}$STIME{hour}$STIME{min}$STIME{sec}";
	}
	
	
	# 履歴データに書き込み------------------------------------------
	my $id = time.$$;
	$FORM{id} = $id;
	$FORM{start_send_date} = $FORM{starttime};
	$FORM{status} = 1;
	$FORM{send_type} = $admindata->{send_type};
	for(1..5) {
		$FORM{"search".$_}      .= $mail_session->get("search".$_);	# 絞込みカラム
		$FORM{"search_text".$_} .= $mail_session->get("search_text".$_);		# 絞込みテキスト
		$FORM{"searchlike".$_}   = $mail_session->get("searchlike".$_);
	}
	$FORM{'search_domain'} = $mail_session->get('search_domain');
	$FORM{'andor'} = $mail_session->get('andor');
	$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
	# 書き込み
	$objAcData->InsData('hist', 'HIST', \%FORM);
	#------------------------------------------------------------------
	
	$|=1;

	&htmlheader;
	
	# 閉じれないようにする
	print '<body onBeforeUnload="return UnloadMessage();">
<script language="JavaScript" type="text/javascript">

var noLocation = 1;
<!--
function UnloadMessage(){
	if (noLocation) {
		return "画面から移動すると処理が中断されてしまいます。";
	} else {
		
	}
}
// -->
</script>
';
	
	print '</div><br><div align="center"><div style="width:600;padding:4px 5px;border:1px solid #666;background:#FFFFFF;">'."\r\n\r\n";
	
	
	# グラフ生成
	print &make_graph_html()."<br>";
	
	print "<div id=\"init_title\"><font color=\"#ff0000\"><b>送信中です・・・</b></font></div><br>";
	my $c = 1;
	
	my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));

	my $return_path = $admindata->{admin_email};
	if ($admindata->{errmail} && $admindata->{errmail_email}) {
		$return_path = $admindata->{errmail_email};
	}
	my @hist;
	my $objMail = create_clsMail($admindata);
	foreach my $row (@NEWDATA_ORG){
		my $return = 1;
		$return = $objMail->send($admindata->{sendmail_path},$row->{email},$row->{subject},$row->{body},$sendername,$admindata->{admin_email},"",$return_path, $FORM{mail_type}, $id);
		
		# 一定間隔待つ
		if ($admindata->{'send_span'}) { select(undef, undef, undef, $admindata->{'send_span'}); }
		
		if ($return){
			print '<font size="-1">'."$c:"."$row->{email}</font><br>\n";
			my $hist;
			$hist->{email} = $row->{email};
			push(@hist, $hist);
		}else{
			print '<font size="-1">'."$c:"."<font color=\"#ff0000\">送信エラー($row->{email})</font></font><br>\n";
		}
		# 休憩なし
		#if(defined $waitspan && ($c % $waitspan) == 0){ sleep($waittime);}
		
		my $bar = int(($c / ($#NEWDATA_ORG + 1)) * 50);
		my $per = int(($c / ($#NEWDATA_ORG + 1)) * 100);
		if ($bar > 50) { $bar = 50; }
		if ($per > 100) { $per = 100; }
		print '<script type="text/javascript">parent.setProgress('.$per.','.$bar.');</script>';
		$c++;
	}
	print "<br><font color=\"#ff0000\"><b>送信完了しました。</b></font><br>";
	print "<div align=\"center\">";
	print "<br><a href=\"email_send.cgi\">戻る</a></div></div></div>";

	print '<script type="text/javascript"><!--
document.getElementById(\'init_title\').innerHTML = "<b>送信完了しました</b>";
// --></script>';
	&htmlfooter;
	
	# 履歴データに最終書き込み
	my %TIME = &getdatetime();
	
	# 対象データ取得
	my $target = $objAcData->GetData('hist', 'HIST', $id);
	my %UPDATE;
	foreach my $n (keys %$target) {
		$UPDATE{$n} = $target->{$n};
	}
	$UPDATE{end_send_date} = "$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}$TIME{sec}";	# 送信終了時間
	$UPDATE{backnumber} = 1;
	$UPDATE{status} = 2;
	$UPDATE{total_count} = ($c - 1);
	# 更新
	$objAcData->UpdData('hist', 'HIST', $id, \%UPDATE);
	
	# セッションクリア
	&clear_mailsession();
	print '<script language="JavaScript" type="text/javascript">noLocation = 0;</script>';
	print "<meta http-equiv=\"REFRESH\" content=\"0;URL=email_send_finish.cgi\">\n";
	exit;
}

sub sendmail_div{
	my @NEWDATA_ORG = @_;
	
	my $waittime = $admindata->{divwait};
	my $start = $FORM{"start"};
	my $end = $start + $admindata->{divnum};

	my $c = 0;
	
	my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));

	my $return_path = $admindata->{admin_email};
	if ($admindata->{errmail} && $admindata->{errmail_email}) {
		$return_path = $admindata->{errmail_email};
	}
	
	if (!$FORM{starttime}) {
		my %STIME = &getdatetime();
		$FORM{starttime} = "$STIME{year}$STIME{mon}$STIME{mday}$STIME{hour}$STIME{min}$STIME{sec}";
		
		$FORM{id} = time.$$;
		# 履歴データに書き込み
		$FORM{start_send_date} = $FORM{starttime};
		$FORM{status} = 1;
		$FORM{send_type} = $admindata->{send_type};
		for(1..5) {
			$FORM{"search".$_}      .= $mail_session->get("search".$_);	# 絞込みカラム
			$FORM{"search_text".$_} .= $mail_session->get("search_text".$_);		# 絞込みテキスト
			$FORM{"searchlike".$_}   = $mail_session->get("searchlike".$_);
		}
		$FORM{'search_domain'} = $mail_session->get('search_domain');
		$FORM{'andor'} = $mail_session->get('andor');
		$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
		# 書き込み
		$objAcData->InsData('hist', 'HIST', \%FORM);
	}
	
	my $data_num = ($#NEWDATA_ORG + 1);
	$| = 1;
	my $wr;
	foreach my $n (keys %$admindata) {
		$wr->{admindata}{$n} = $admindata->{$n};
	}
	&writing_check(\$wr);
	my $write = '<a href="http://www.ahref.org"><img src="img/ahref_2.jpg" alt="メルマガ配信CGI acmailer" /></a>';
	if ($wr->{writing}) { $write = ""; }

	print "Content-Type: text/html; charset=EUC-JP\n\n";
	print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP" />
<title>分割送信中</title>
<link rel="stylesheet" href="./css/common.css" type="text/css">
<link rel="stylesheet" href="./css/default.css" type="text/css">
<link rel="stylesheet" href="./css/login_etc.css" type="text/css">
<SCRIPT language="JavaScript">
<!--
var set=0;
function nidoosi() {
	if(set==0){
		set=1;
	}else{
		alert("二度押しはいけません。\\nしばらくそのままお待ちください。");
		return false
	}
}
function delcheck() {
	f = confirm("削除してよろしいですか？");
	return f
}
var noLocation = 1;
function UnloadMessage(){
	if (noLocation) {
		return "画面から移動すると処理が中断されてしまいます。";
	} else {
		
	}
}

//-->
</SCRIPT>
</head>
<body onBeforeUnload="return UnloadMessage();">
<div id="containt_panel_wrapper">
	<div id="containt_panel">
    	<div id="panel_head" class="clearfix">
        	<div id="panel_head_left"><a href="http://www.acmailer.jp"><img src="img/logo.jpg" alt="メルマガ配信CGI acmailer" /></a></div>
            <div id="panel_head_right">'.$write.'</div>
        </div>';	
	
	

	print "<br><div align=\"center\" id=\"message\"><b>ただいま送信中・・・</b><br><br>しばらくそのままでおまちください！";
	print "<br><br></div><div align=\"center\" id=\"now\">$end / $data_num</div>";
	print '<div align="center"><div style="width:600;padding:4px 5px;border:1px solid #666;background:#FFFFFF;">';
	
	# グラフ生成
	print &make_graph_html()."<br>";
	my $bar = int((($start + 1) / ($#NEWDATA_ORG + 1)) * 50);
	my $per = int((($start + 1) / ($#NEWDATA_ORG + 1)) * 100);
	if ($bar > 50) { $bar = 50; }
	if ($per > 100) { $per = 100; }
	print '<script type="text/javascript">parent.setProgress('.$per.','.$bar.');</script><br>';
	
	my $objMail = create_clsMail($admindata);
	foreach my $row (@NEWDATA_ORG){
		if($c >= $start && $c < $end){
			my $return = 1;
			$return = $objMail->send($admindata->{sendmail_path},$row->{email},$row->{subject},$row->{body},$sendername,$admindata->{admin_email},"",$return_path, $FORM{mail_type}, $FORM{id});
			
			if ($return){
				print ('<font size="-1">'.($c + 1).":"."$row->{email}</font><br>\n");
			}else{
				print (($c + 1).":"."<font color=\"#ff0000\">送信エラー($row->{email})</font><br>\n");
			}
			my $bar = int((($c + 1) / ($#NEWDATA_ORG + 1)) * 50);
			my $per = int((($c + 1) / ($#NEWDATA_ORG + 1)) * 100);
			if ($bar > 50) { $bar = 50; }
			if ($per > 100) { $per = 100; }
			print '<script type="text/javascript">parent.setProgress('.$per.','.$bar.');</script>';
			print '<script type="text/javascript"><!--
	document.getElementById(\'now\').innerHTML = "'.($c + 1)." / ".$data_num.'";
	// --></script>';
			
			# 一定間隔待つ
			if ($admindata->{'send_span'}) { select(undef, undef, undef, $admindata->{'send_span'}); }
			
		}
		$c++;

	}

	if($data_num > $end){
	    my $mail_id = $mail_session->mail_id();
	    print '<script language="JavaScript" type="text/javascript">noLocation = 0;</script>';
	    print "<meta http-equiv=\"REFRESH\" content=\"$waittime;URL=email_send_ctl.cgi?start=$end&starttime=$FORM{starttime}&mail_type=$FORM{mail_type}&id=$FORM{id}&mail_session_id=$mail_id\">\n";
	}
	print "</head>\n";
	#print "<body bgcolor=\"#FFFFFF\">\n";

	if($data_num > $end){
		
	}else{
		print '<script type="text/javascript"><!--
document.getElementById(\'message\').innerHTML = "<b>送信完了！</b><br><br>'.$data_num.'件の送信が完了しました。";
// --></script>';
		print "<br><a href=\"email_send.cgi\">戻る</a>";
		print '<script language="JavaScript" type="text/javascript">noLocation = 0;</script>';
		
		# 履歴データに書き込み
		my %TIME = &getdatetime();
		
		# 対象データ取得
		my $target = $objAcData->GetData('hist', 'HIST', $FORM{id});
		my %UPDATE;
		foreach my $n (keys %$target) {
			$UPDATE{$n} = $target->{$n};
		}
		$UPDATE{end_send_date} = "$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}$TIME{sec}";	# 送信終了時間
		$UPDATE{backnumber} = 1;
		$UPDATE{status} = 2;
		$UPDATE{total_count} = ($#NEWDATA_ORG + 1);
		# 更新
		$objAcData->UpdData('hist', 'HIST', $FORM{id}, \%UPDATE);
		
		# セッションクリア
		&clear_mailsession();
		
		print "<meta http-equiv=\"REFRESH\" content=\"0;URL=email_send_finish.cgi\">\n";
	}

	&htmlfooter();

	exit;
}

# 管理者テスト送信
sub sendmail_admin{
	my @NEWDATA_ORG = @_;
	
	$|=1;
	if (&isMobile()) {
		print "Content-Type: text/html; charset=EUC-JP\n\n";
		print '<?xml version="1.0" encoding="EUC-JP"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">
<head>
<meta http-equiv="Content-Type" content="application/xhtml+xml; charset=EUC-JP" />
<title>テスト送信</title>
</head>
<body>
<br><br>';
	} else {
		&htmlheader;
		print "</div>";
		print '<div align="center">';
	}
	my $c = 1;
	
	my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));

	my $objMail = create_clsMail($admindata);
	foreach my $row (@NEWDATA_ORG){
		my $return = 1;
		#$return = $objMail->send($admindata->{sendmail_path},$admindata->{admin_email},$row->{subject},$row->{body},$sendername,$sendername,"",$sendername, $FORM{mail_type});
		$return = $objMail->send($admindata->{sendmail_path},$FORM{test_email},$row->{subject},$row->{body},$sendername,$admindata->{admin_email},"",$admindata->{admin_email}, $FORM{mail_type});
		if ($return){
			print "$FORM{test_email}<br>\n";
		}else{
			print "<font color=\"#ff0000\">送信エラー($admindata->{admin_email})</font><br>\n";
		}
		last;
	}
	print "<br><font color=\"#ff0000\"><b>送信完了しました。</b></font><br>";
	print "<div align=\"center\">";
	if (!&isMobile()) {
		print "<br><input type=\"button\" value=\"閉じる\" onclick=\"javascript:window.close();\"></div>";
		print '<script type="text/javascript"><!--
document.getElementById(\'title\').innerHTML = "<b>送信完了！</b>";
// --></script>';
	} else {
		
	}
	
	&htmlfooter;
	exit;
}

# 予約配信
sub reserve{
	my @NEWDATA_ORG = @_;
	# 履歴データに書き込み------------------------------------------
	$FORM{id} = time.$$;
	$FORM{start_send_date} = sprintf("%04d%02d%02d%02d%02d%02d", $FORM{send_year}, $FORM{send_mon}, $FORM{send_day}, $FORM{send_hour}, $FORM{send_min}, 0);
	$FORM{status} = 3;
	$FORM{send_type} = $admindata->{send_type};
	$FORM{total_count} = ($#NEWDATA_ORG + 1);
	for(1..5) {
		$FORM{"search".$_}      .= $mail_session->get("search".$_);	# 絞込みカラム
		$FORM{"search_text".$_} .= $mail_session->get("search_text".$_);		# 絞込みテキスト
		$FORM{"searchlike".$_}   = $mail_session->get("searchlike".$_);
	}
	$FORM{'search_domain'} = $mail_session->get('search_domain');
	$FORM{'andor'} = $mail_session->get('andor');
	$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
	# 書き込み
	$objAcData->InsData('hist', 'HIST', \%FORM);
	#------------------------------------------------------------------
	
	my $sid = "";
	if ($FORM{'sid'}) { $sid = "&sid=".$FORM{'sid'}; }
	
	# セッションクリア
	&clear_mailsession();
	print "Location: email_send_finish.cgi?mode=reserve".$sid."\n\n";
	exit;
	
}


sub make_graph_html() {
	my $tag = '
    <table summary="プログレスバー" border="0"
     cellpadding="0" cellspacing="1" height="2" bgcolor="black"><tr><td bgcolor="#FFFFFF">
	 <table class="frame" border="0" width="100%" height="100%">
      <tr>';
	for(1..50) {
		$tag .= '
        <td width="2" height="2" id="bar'.$_.'"
         style="background-color:#CCCCCC;">
            &nbsp;
        </td>';
	}
	$tag .= '</tr>
    </table></td></tr></table><table width="100%"><tr>
        <td bgcolor="white" height="5" width="100%" id="percent"
         style="font-size:1.4em"></td></tr></table>
		 <SCRIPT language="JavaScript">
<!--

function setProgress(percent,barno)
{
var node = document.getElementById(\'percent\');
node.innerHTML = percent + \'パーセント\';
if(barno > 0) {
	for(i = 1; i <= barno; i++) {
	    node = document.getElementById(\'bar\'+ i);
	    node.style.backgroundColor = "#FFCC00";
	}
}
}

//-->
</SCRIPT>';
	return $tag;
}

sub clear_mailsession {
    $mail_session->clear();
    return 1;
}
