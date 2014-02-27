#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
use MailSession;

our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# セッションデータ取得とログインチェック
my %COOKIE = &getcookie;
my %FORM = &form("noexchange", "noencode");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
if ($FORM{sid}) { $COOKIE{sid} = $FORM{sid}; }


# メールセッション
my $mail_session = MailSession->new(
    mail_id     => $FORM{mail_session_id},
    session_dir => $SYS->{dir_session_mail},
);


my $data_ref;

# 検索条件取得
for (1..5) {
    # 絞込みカラム
    $FORM{"search".$_} .= $mail_session->get("search".$_);

    # 絞込みテキスト
    $FORM{"search_text".$_} .= $mail_session->get("search_text".$_);
    $FORM{"searchlike".$_} = $mail_session->get("searchlike".$_);
}
$FORM{'search_domain'} = $mail_session->get('search_domain');
$FORM{'andor'} = $mail_session->get('andor');


$FORM{mail_title} =~ s/__<<equal>>__/\=/gi;
$FORM{mail_body} =~ s/__<<equal>>__/\=/gi;
$FORM{mail_title} =~ s/__<<semicolon>>__/;/gi;
$FORM{mail_body} =~ s/__<<semicolon>>__/;/gi;

$data_ref = $admindata;

# 管理画面の設定が行われているかどうか
&CheckAdminData_MailSend($admindata);

# 検索項目作成
my @search = $objAcData->MakeSearchCol(\%FORM, $SYS->{max_colnum});
$data_ref->{search} = \@search;

# メールデータ取得
my @DATA = $objAcData->GetData('mail', 'MAIL');

# 重複チェック
&CheckDoubleData(\@DATA, $admindata);

$data_ref->{totalnum} = $#DATA+1;

# 背景色
if ($FORM{bgcolor}) {
	# BODYタグがあれば置換
	if ($FORM{mail_body} =~ s/\<BODY(.*)?\>/\<BODY$1 bgcolor\=\"$FORM{bgcolor}\"\>/i) {
		
	} else {
		$FORM{mail_body} = '<body bgcolor="'.$FORM{bgcolor}.'">'.$FORM{mail_body}.'</body>';
	}
}

#件名
$data_ref->{mail_title} = $FORM{mail_title};
my $session_mail_title = $FORM{mail_title};

#本文
$data_ref->{mail_body} = $FORM{mail_body};
my $session_mail_body = $FORM{mail_body};

# セッションに格納
$mail_session->set('mail_title', $session_mail_title);
$mail_session->set('mail_body', $session_mail_body);

# 表示用
$data_ref->{'mail_title'} = &plantext2html($data_ref->{'mail_title'});
$data_ref->{'mail_body'} = &plantext2html($data_ref->{'mail_body'});

foreach my $n (qw(EMAIL REGURL DELURL YEAR MONTH DAY HOUR MINUTE SECOND WEEK WEEK-JP MONTH-00 DAY-00 HOUR-00 MINUTE-00 SECOND-00)) {
	$data_ref->{mail_title} =~ s/\{$n\}/<font color=\"blue\"><b>\{$n\}<\/b><\/font>/g;
	$data_ref->{mail_body} =~ s/\{$n\}/<font color=\"blue\"><b>\{$n\}<\/b><\/font>/g;
}

# 絵文字と画像の埋め込みをやめる
$data_ref->{mail_body} =~ s/(\{e_.*?\})/<font color=\"blue\"><b>$1<\/b><\/font>/g;
$data_ref->{mail_title} =~ s/(\{e_.*?\})/<font color=\"blue\"><b>$1<\/b><\/font>/g;
$data_ref->{mail_body} =~ s/(\{img_.*?\})/<font color=\"blue\"><b>$1<\/b><\/font>/g;

for(1..$SYS->{max_colnum}) {
	my $n = "COL$_";
	$data_ref->{mail_title} =~ s/\{$n\}/<font color=\"blue\"><b>\{$n\}<\/b><\/font>/g;
	$data_ref->{mail_body} =~ s/\{$n\}/<font color=\"blue\"><b>\{$n\}<\/b><\/font>/g;
}
$data_ref->{mail_title} =~ s/\t/ /gi;
$data_ref->{mail_body} =~ s/\t/ /gi;

# 送信先一覧
my @DATA = $objAcData->GetData('mail', 'MAIL');
# 検索絞り込み
my @DATA = $objAcData->SearchEmail(\@DATA, \%FORM, $SYS->{max_colnum});
my @predata;
my (%ZYU, $zyunum, $errornum, $i);
$S{sender_data} = "";
my $sendertotal = 0;
foreach my $row (@DATA){
	
	# 配信停止の場合はNEXT
	if (!$row->{status}) { next; }
	
	$row->{i} = $i+1;
	
	my %TIME = &getdatetime();
	
	# 送信先一覧用
	$row->{subject} = $objAcData->ReplaceMailBody($FORM{mail_title}, $admindata, $row, $SYS->{max_colnum});
	$row->{body} = $objAcData->ReplaceMailBody($FORM{mail_body}, $admindata, $row, $SYS->{max_colnum});
	
	$row->{subject} =~ s/\t/ /gi;
	$row->{body} =~ s/\t/ /gi;
	$row->{body} =~ s/'/’/gi;
	$row->{num} = ($i + 1);
	
	# プレビュー用本文は1000文字以内
	$row->{body} = z_substr($row->{body}, 0, 1000);
	
	# 絵文字
	$row->{body} = &ReplaceEmojiDisp($row->{body});
	$row->{subject} = &ReplaceEmojiDisp($row->{subject});
	
	# 画像埋め込み
	$row->{body} = &ReplaceImageDisp($row->{body});
	push(@predata, $row);
	
	$ZYU{$row->{email}}++;
	$i++;
	$sendertotal++;
	
}
$data_ref->{pre_list} = \@predata;

# CSV出力
if ($FORM{'down_mode'} eq "csv") {
	my @CSV;
	push(@CSV, @predata);
	
	my $mail = "E-MAIL\n";
	my @col = ('email');
	&DownloadCSV(\@CSV, \@col, 'email_data', ',');
	exit;
}

if ($sendertotal == 0) { &error("送り先がありません。"); }
$data_ref->{sender_total} = $sendertotal;

# 自由項目取得
my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
