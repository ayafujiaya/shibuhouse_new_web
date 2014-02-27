#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å����ǡ�������
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

if ($FORM{id} =~ /[^0-9]/ || !$FORM{id}) { &error("�ѥ�᡼�����顼�Ǥ���"); }

# �о�����ǡ�������
my $hist = $objAcData->GetData('hist', 'HIST', $FORM{id});
$data_ref = $hist;


print "Content-type: text/html; charset=EUC-JP\n\n";
print '
<span style="font-size:small">
<font size="1">
�ʲ�������������Ƥ������Ǥ�����
<br>
��̾��'.$data_ref->{mail_title}.'
<br>
<a href="hist_detail.cgi?back=1&id='.$FORM{id}.'&sid='.$FORM{sid}.'">������</a>
&nbsp;&nbsp;
<a href="hist_list.cgi?hist_del=1&id='.$FORM{id}.'&sid='.$FORM{sid}.'">�Ϥ�</a>
</font>
</span>
';
exit;
