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
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);

# 共通変数読み込み
my $li;
&set_common_value(\$li, $admindata);

if ($FORM{mode} eq "hist") {

	if ($FORM{id} =~ /[^0-9]/ || !$FORM{id}) { &error("パラメータエラーです。"); }

	my $data_ref = $objAcData->GetData('hist', 'HIST', $FORM{id});
	$data_ref->{mail_body} =~ s/__<<BR>>__/\n/gi;
	$data_ref->{mail_body} =~ s/__<<equal>>__/\=/gi;
	$data_ref->{mail_body} =~ s/__<<semicolon>>__/;/gi;
	$data_ref->{mail_body} =~ s/__<<BR>>__/<BR>/gi;

	# 絵文字
	$data_ref->{mail_body} = &ReplaceEmojiDisp($data_ref->{mail_body});
	$data_ref->{mail_title} = &ReplaceEmojiDisp($data_ref->{mail_title});

	# 画像埋め込み
	$data_ref->{mail_body} = &ReplaceImageDisp($data_ref->{mail_body});

	print "Content-type: text/html; charset=EUC-JP\n\n";
	print '<html><head><title>プレビュー</title></head><body>';
	print $data_ref->{mail_body};
} elsif ($FORM{'makepreview'}) {
	# 作成中のプレビュー
	$FORM{mail_body} =~ s/__<<equal>>__/\=/gi;
	$FORM{mail_body} =~ s/__<<semicolon>>__/;/gi;
	$FORM{mail_body} =~ s/__<<BR>>__/<BR>/gi;
	
	# 絵文字
	$FORM{mail_body} = &ReplaceEmojiDisp($FORM{mail_body});
	$FORM{mail_title} = &ReplaceEmojiDisp($FORM{mail_title});

	# 画像埋め込み
	$FORM{mail_body} = &ReplaceImageDisp($FORM{mail_body});
	
	# 背景色
	if ($FORM{bgcolor}) {
		# BODYタグがあれば置換
		if ($FORM{mail_body} =~ s/\<BODY(.*)?\>/\<BODY$1 bgcolor\=\"$FORM{bgcolor}\"\>/i) {
			
		} else {
			$FORM{mail_body} = '<body bgcolor="'.$FORM{bgcolor}.'">'.$FORM{mail_body}.'</body>';
		}
	}
	
	print "Content-type: text/html; charset=EUC-JP\n\n";
	print '<html><head><title>プレビュー</title></head><body>';

	print $FORM{mail_body};
} elsif ($FORM{boutou}) {

    # メールセッション
    my $mail_session_id = $FORM{mail_session_id};
    my $mail_session = MailSession->new(
        mail_id     => $mail_session_id,
        session_dir => $SYS->{dir_session_mail},
    );

    my $mail_body  = $mail_session->get('mail_body');
    my $mail_title = $mail_session->get('mail_title');

    # 冒頭プレビュー
    $mail_body =~ s/__<<equal>>__/\=/gi;
    $mail_body =~ s/__<<semicolon>>__/;/gi;
    $mail_body =~ s/__<<BR>>__/<BR>/gi;

    # 絵文字
    $mail_body  = &ReplaceEmojiDisp($mail_body);
    $mail_title = &ReplaceEmojiDisp($mail_title);

    # 画像埋め込み
    $mail_body = &ReplaceImageDisp($mail_body);

    # 送信用データ取得
    my $objDataSender = clsAcData->new($SYS->{dir_session});

    # 配信データ１件を取得
    my @DATA = split(/\n/, $objDataSender->getSenderData( $mail_session->mail_id() ));
    foreach (@DATA) {
        if (!$_) {
            next;
        }
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
        if (!$row->{status}) {
            next;
        }


        # 改行コード制御
        if ($FORM{mail_type} eq "plain") {
            $mail_title =~ s/__<<BR>>__/\n/gi;
            $mail_body  =~ s/__<<BR>>__/\n/gi;
        } else {
            $mail_title =~ s/__<<BR>>__/<BR>/gi;
            $mail_body  =~ s/__<<BR>>__/<BR>/gi;
        }

        # 置換
        $mail_title = $objAcData->ReplaceMailBody($mail_title, $admindata, $row, $SYS->{max_colnum});
        $mail_body  = $objAcData->ReplaceMailBody($mail_body , $admindata, $row, $SYS->{max_colnum});
        last;
    }

    if ($FORM{mail_type} eq "plain") {
        $mail_body =~ s/\r\n|\r|\n/\<br\>/g;
    }

    print "Content-type: text/html; charset=EUC-JP\n\n";
    print '<html><head><title>プレビュー</title></head><body>';

    print $mail_body;
} else {
	$S{mail_body} =~ s/__<<equal>>__/\=/gi;
	$S{mail_body} =~ s/__<<semicolon>>__/;/gi;
	$S{mail_body} =~ s/__<<BR>>__/<BR>/gi;

	# 絵文字
	$S{mail_body} = &ReplaceEmojiDisp($S{mail_body});
	$S{mail_title} = &ReplaceEmojiDisp($S{mail_title});

	# 画像埋め込み
	$S{mail_body} = &ReplaceImageDisp($S{mail_body});

	print "Content-type: text/html; charset=EUC-JP\n\n";
	print '<html><head><title>プレビュー</title></head><body>';

	print $S{mail_body};
}

if (!$li->{writing}) {
	&htmlfooter();
} else {
	print '</body></html>';
	exit;
}
