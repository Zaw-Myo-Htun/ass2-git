#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
warningsToBrowser(1);

# print start of HTML ASAP to assist debugging if there is an error in the script
print page_header();

# some globals used through the script
$debug = 1;
$skipLines = 0;
$students_dir = "./students";

print browse_screen();
print page_trailer();
exit 0;	

sub browse_screen {
	my $n = param('n') || 0;
	my @students = glob("$students_dir/*");
	$n = min(max($n, 0), $#students);
	param('n', $n + 1);
	my $student_to_show  = $students[$n];
	my $profile_filename = "$student_to_show/profile.txt";
	open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
	while ( $line = <$p>){
		if($skipLines == 0){
			if($line =~ /^(name:|password:|email:|courses:)$/){
				$skipLines = 1;
			}else{
				$profile .= $line;
			}
		}else{
			if(not($line =~ /^(name:|password:|email:|courses:)$/)){
				if($line =~ /:$/){
				$profile .= $line;
				$skipLines = 0;
				}
			}
		}
	}
	
	close $p;
	
	
	return p,
		start_form, "\n",
		pre($profile),"\n",
		hidden('n', $n + 1),"\n",
		submit('Next student'),"\n",
		img({ 
			src => "$student_to_show/profile.jpg"
			}), "\n\n",
		end_form, "\n",
		p, "\n";
}

#
# HTML placed at bottom of every screen
#
sub page_header {
	return header,
   		start_html("-title"=>"LOVE2041", -bgcolor=>"#FEDCBA"),
 		center(h2(i("LOVE2041")));
}

#
# HTML placed at bottom of every screen
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
	my $html = "";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
	$html .= end_html;
	return $html;
}