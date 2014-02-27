#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

my %FORM = &form("noexchange");
my $data_ref;

if ($FORM{id}) {
	# �оݥǡ�������
	my $doptdata = $objAcData->GetData('mailbuf', 'TEMPMAIL', $FORM{id});
	
	if (!$doptdata->{id} || !$doptdata->{email}) { &error("�оݤΥǡ��������˼��Ԥ��ޤ�����<br>������Ͽ����Ƥ��뤫������Ͽ����Ƥ��ޤ���"); }
	$data_ref->{doptdata} = $doptdata;
	

} elsif ($FORM{mode} ne "preview") {
	# �̾�Υե�����Ȥ��ƻ��Ѥ���褦��
	#&error("�����ʥ��������Ǥ�");
}

# ���Ѷػߤ��ɤ���
if (!$FORM{'preview'} && !$admindata->{'autoform_use'}) {
	&error("���߻��Ѥ��뤳�Ȥ��Ǥ��ޤ���");
}

# ��ͳ����
my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
$data_ref->{freecol_list} = \@freecol;

# �����å��ܥå����Τ�ΤϤ��餫����ʸ��������
my $i = 1;

foreach my $n (@freecol) {
	if ($FORM{'preview'}) {
		foreach my $n2 (qw(type name disp text)) {
			$n->{"col".$n2} = $FORM{"col".$i.$n2};
			if ($n2 eq "text") {
				# ���Ԥ��ޤޤ�Ƥ�����
				my @autodata = split(/\r\n|\r|\n/, $n->{"col".$n2});
				my @v2;
				foreach my $n2 (@autodata) {
					if ($n2 eq "") { next; }
					my $row2;
					$row2->{"coltext"} = $n2;
					push(@v2, $row2);
				}
				$n->{"autodatalist"} = \@v2;
			}
		}
	}
	if ($n->{coltype} eq "checkbox") {
		$data_ref->{checkbox_list} .= ",col".$n->{num};
	}
	$i++;
}

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# �ե��������
$data_ref->{form} = \%FORM;

# HTMLɽ��
if (&isMobile()) {
	# ����ü���ξ��
	&printhtml_tk($data_ref, "tmpl/m_form.tmpl", "", "Shift_JIS");
} else {
	# PC��
	&printhtml_tk($data_ref, "tmpl/form.tmpl");
}
exit;
