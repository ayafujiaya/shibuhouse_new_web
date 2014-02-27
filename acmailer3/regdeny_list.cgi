#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

if ($FORM{del}) {
    # ���
	if ($FORM{'id'}) {
		$objAcData->DelData("regdeny", "REGDENY", $FORM{'id'});
		$data_ref->{'oktext'} = "����������ޤ�����";
	} else {
	    $objAcData->CleanRegDeny(\%FORM);
	    $data_ref->{oktext} = "$FORM{delnum}��������ޤ�����";
	}
} elsif ($FORM{'alldel'}) {
	# �����
	my %REG;
	$objAcData->ResetData("regdeny", "REGDENY", \%REG);
	$data_ref->{'oktext'} = "����������ޤ�����";
} elsif ($FORM{'mode'} eq "change") {
	# ����Ͽ���������ѹ�
	my $regdata = $admindata;
	$regdata->{'regdeny'} = $FORM{'regdeny'} ? "1" : "";
	
	# �����ԥǡ�������
	$objAcData->UpdAdminData($regdata);
	
	# �����ԥǡ�����Ƽ���
	$admindata = $objAcData->GetAdminData();

}

# ����Ͽ�ǡ�������
my @DATA = $objAcData->GetData('regdeny', 'REGDENY');
foreach my $row (@DATA) {
	# �����
	#$row->{del_date_disp} = substr($row->{del_date}, 0, 4)."/".substr($row->{del_date}, 4, 2)."/".substr($row->{del_date}, 6, 2);
	$row->{del_date_disp} = $row->{del_date};
	$row->{del_date_disp} =~ s/^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})$/$1\/$2\/$3 $4:$5:$6/;
	# ������
	if ($row->{limit_date}) {
		$row->{limit_date_disp} = $row->{limit_date};
		#$row->{limit_date_disp} = substr($row->{limit_date}, 0, 4)."/".substr($row->{limit_date}, 4, 2)."/".substr($row->{limit_date}, 6, 2);
		$row->{limit_date_disp} =~ s/^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})$/$1\/$2\/$3 $4:$5:$6/;
	}
}
my @SEARCH;
if ($FORM{'search'} && $FORM{'search_word'}) {
	# �ʤ����
	foreach my $row (@DATA) {
		if ($row->{'email'} =~ /$FORM{search_word}/) {
			push(@SEARCH, $row);
		}
	}
	@DATA = @SEARCH;
}

# ������
@DATA = sort {$b->{'del_date_disp'} cmp $a->{'del_date_disp'}} @DATA;

# �ѥ�᡼����������
if ($FORM{'search'}) {
	$data_ref->{'para'} = "&search=1&search_word=".&urlencode($FORM{'search_word'});	
}

# �ڡ����󥰽���
my $objPaging = new clsPaging($FORM{dispnum}, $FORM{page}, $data_ref->{'para'});
@DATA = $objPaging->MakePaging(\@DATA, \$data_ref);

$data_ref->{loop} = \@DATA;

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;
