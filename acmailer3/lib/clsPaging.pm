#!/usr/bin/perl
# 
# 

package clsPaging;

use File::Basename;
use POSIX;

use strict;

# ���󥹥ȥ饯��
# ���������ǡ����ǥ��쥯�ȥ�
sub new {
	my $pkg = shift;
	my $dispnum = shift;
	my $page = shift;
	my $para = shift;
	my $thispage = shift;
	
	if (!$thispage) {
 		my ($base,$path,$suffix) = fileparse($0);
		$base =~ s/\.cgi$//;
		$thispage = $base;
	}
	bless {
		dispnum	=> $dispnum,
		page		=> $page,
		para		=> $para,
		thispage	=> $thispage,
		
	} ,$pkg;
}

# �ڡ����󥰽���
# ���������ǡ�������
sub MakePaging() {
	my $this = shift;
	my $p_data = shift;
	my $pagedata = shift;
	
	my @data = @$p_data;
	
	# *** �ڡ������� *** #
	my $page = $this->{page};
	my $dispnum = $this->{dispnum};
	my ($offset, $dispnum_d);
	if($page and ( $page < 1 or $page >= 2000000000)){
		main::error("PAGE�λ��꤬����������ޤ���");
	}
	if($dispnum and $dispnum != "all" and ( $dispnum < 1 or $dispnum >= 2000000000)){
		main::error("ɽ������λ��꤬����������ޤ���");
	}

	if(!$page){ $page = 1; }
	if(!$dispnum){ $dispnum = "50";$dispnum_d = 1; }
	if($dispnum != "all"){
		$offset = ($page-1)*$dispnum;
	}
	# ****************** #
	my @return;
	my $i = 0;
	foreach my $row (@data) {
		if(($dispnum eq "all") ||
		   ($offset <= $i && ($offset+$dispnum) > $i)){
			push (@return, $row);
		}
		$i++;
	}
	
	# *** �ڡ������� *** #
	if($page > 1 ){
		$$pagedata->{backlink} = 1;
	}

	if($dispnum ne "all" && ($offset+$dispnum) < ($#data+1) ){
		$$pagedata->{nextlink} = 1;
	}

	$$pagedata->{page} = $page;
	$$pagedata->{page_m1} = $page-1;
	$$pagedata->{page_p1} = $page+1;
	$$pagedata->{dispnum} = $dispnum;
	$$pagedata->{thispage} = $this->{thispage};
	$$pagedata->{totalnum} = $#data+1;
	
	$$pagedata->{para} = $this->{para};
	my $pagenumall = 1;
	if($dispnum >= 1 && $dispnum ne "all"){
		$pagenumall = ceil(($#data+1) / $dispnum);
	}

	if (!$$pagedata->{'dispspan'}) { $$pagedata->{'dispspan'} = 3; }
	for(my $i = ($page - $$pagedata->{'dispspan'}); $i <= ($page + $$pagedata->{'dispspan'}); $i++){
		if($i < 1){ next; }
		if($i > $pagenumall){ last; }

	#for(1..$pagenumall){
		if($i == $page){
			$$pagedata->{pagelink} .= "��$i";
		}else{
			$$pagedata->{pagelink} .= "��<A href=\"$this->{thispage}.cgi?page=$i&dispnum=$dispnum$this->{para}\">$i</A>";
		}
	}
	return @return;
}

1;
