#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å����ǡ��������ȥ���������å�
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my @DATA = &openfile2array("$SYS->{data_dir}hist.cgi");

if ($FORM{id} =~ /[^0-9]/ || !$FORM{id}) { &error("�ѥ�᡼�����顼�Ǥ���"); }

# �оݥǡ�������
my $email = $objAcData->GetMailData($FORM{id});

print "Content-type: text/html; charset=EUC-JP\n\n";
print '

<span style="font-size:small">
<font size="1">
�ʲ��Υ᡼��������Ƥ������Ǥ�����
<br>
'.$email->{email}.'
<br>
<a href="email_list.cgi?back=1&sid='.$FORM{sid}.'">������</a>
&nbsp;&nbsp;
<a href="email_edit.cgi?del=1&id='.$FORM{id}.'&sid='.$FORM{sid}.'">�Ϥ�</a>
</font></span>
';
exit;
