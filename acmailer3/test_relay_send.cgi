#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use clsMail;
use strict;

our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å�����ꥻ�å����ǡ�������
my %COOKIE = &getcookie;
my %S = getsession($COOKIE{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my %FORM = &form("noexchange");

if (!$FORM{'to'} || !$FORM{'from'} || !$FORM{'relay_host'}) {
	&error("�����ԡ������衢���������Ф����ꤷ�Ƥ�������");
}

my $return_path;
if ($admindata->{errmail} && $admindata->{errmail_email}) {
    $return_path = $admindata->{errmail_email};
}


my $senddata = "";
my $subject = 'ACMAILER���ƥ�������';
my $body = "ACMAILER��곰�������Ф����Ѥ��Ƥ������ƥ��ȤǤ���";

#��̾����ʸ��JIS���Ѵ�
&jcode::convert(\$subject, "jis");
&jcode::convert(\$body, "jis");

my $objMail = new clsMail(1, $FORM{relay_host}, $FORM{port}, $FORM{relay_user}, $FORM{relay_pass}, $FORM{relay_send_mode});

#�᡼��HEADER���
$senddata .= "Return-Path: $FORM{from} \n" if $FORM{from};
$senddata .= "X-Mailer: acmailer3.0 http://www.ahref.org/\n";
$senddata .= "X-SENDTO: $FORM{to}\n";
$senddata .= &mimeencode("To: $FORM{to}\n");
$senddata .= &mimeencode("From: $FORM{from}\n");
$senddata .= "Subject: ".$objMail->sencode($subject)."\n";
$senddata .= "MIME-Version: 1.0\n";
$senddata .= "Content-Transfer-Encoding: 7bit\n\n";
#�᡼����ʸ���
$senddata .= $body;


print "Content-type: text/html; charset=EUC-JP\n\n";
print '<div align="center">';
print "�¹Է��<br>";
print '<textarea style="width:400px;height:200px;">';
# ���������Фˤ������
my $rs = $objMail->relay_sendmail($FORM{to}, $FORM{from}, $return_path, $senddata, 1);
print '</textarea>';
print "<CENTER>";
if ($rs) {
	print "�ƥ��ȥ᡼����������������ޤ�������������Ϥ��Ƥ��뤫����ǧ����������";
} else {
	print "<font color=\"red\">�����˼��Ԥ��ޤ������������٤���ǧ����������</font>";
}
print '<center><br><br><br><input type="button" value="�Ĥ���" onclick="javascript:window.close();">';
print '</div>';
exit;
