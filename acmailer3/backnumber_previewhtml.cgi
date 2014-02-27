#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;
my %FORM = &form("noexchange");

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# �����ѿ��ɤ߹���
my $li;
&set_common_value(\$li, $admindata);

&writing_check(\$SYS);

# �����������¤ʤ�
#&limit_access('backnumber.cgi,m_backnumber.cgi');

if (!$admindata->{backnumber_disp}) {
	&error("ɽ���Ǥ��ޤ���");
}

if (!$FORM{id}) {
	&error("�ѥ�᡼�����顼�Ǥ���");
}

print "Content-type: text/html; charset=EUC-JP\n\n";
print '<html><head><title>�ץ�ӥ塼</title></head><body>';


# ����ǡ�������
my $row = $objAcData->GetData('hist', 'HIST', $FORM{id});
my $max = $admindata->{backnumber_num};

my $data_ref;


if ($row->{mail_type} eq "plain") {
	print "�ƥ����ȥ᡼��Ǥ���";
	exit;
} else {
	$row->{mail_body} =~ s/__<<equal>>__/\=/gi;
	$row->{mail_body} =~ s/__<<semicolon>>__/;/gi;
	$row->{mail_body} =~ s/__<<BR>>__/<BR>/gi;

	# ��ʸ��
	$row->{mail_body} = &ReplaceEmojiDisp($row->{mail_body});
	$row->{mail_title} = &ReplaceEmojiDisp($row->{mail_title});

	# ����������
	$row->{mail_body} = &ReplaceImageDisp($row->{mail_body});
	
	print $row->{mail_body};
}


if (!$li->{writing}) {
	print '
<div align="center"></div>
<div align="center">
<!-- ����������������ˤĤ��ơʽ��ס��ˢ����������� -->
<!-- �ܥ����ƥ�ϡ�AHREF(�������������)��̵�Ǥǲ������ɽ�����������ѡ���ɽ���ˤ��뤳�Ȥ϶ػߤ��Ƥ���ޤ� -->
<!-- �����ɽ���˴ؤ��Ƥϡ�������򤴳�ǧ�������� -->
<!-- http://www.ahref.org/cgityosaku.html -->
<!-- ������������������������������������������������ -->
<font size="-2" color=#999999>���ޥ��ۿ�CGI <a href="http://www.ahref.org/" title="���ޥ��ۿ�CGI ACMAILER" target="_blank">ACMAILER</a> Copyright (C) 2008 <a href="http://www.ahref.org/" target="_blank" title="�������������">ahref.org</a> All Rights Reserved.
</font>
</div>
</div>';
}

print '</body></html>';
exit;
