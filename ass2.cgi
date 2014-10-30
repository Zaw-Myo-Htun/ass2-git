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
$skipLines = 0;				#skip private lines
$copyNextLine = "";			#for skipping if gender birthday etc is found and copy next line
%briefDescription = ();
$briefProfile = "";
@descriptions = ();
@images = ();
%usernames = ();
$user = "";
@st = ();

$students_dir = "./students2";
my @students = glob("$students_dir/*");


if(defined param('Log In')) {
	$username = param('username');
	$password = param('password');
	print start_form,"\n";		# delete later ?
	print h3("$username - $password"),"\n";	# delete later ?
	if($username eq "" || $password eq ""){
		 print "<script>alert('Please enter Username and Password')</script>";
		 print login();
	}else{
		$copyNextLine = "";
		
		#$password_file = "users/$username.password";
		#if (!open F, "<$password_file") {
		#	print "Unknown username!\n";
		#} else {
		foreach $s (@students){
			if($s =~ /$students_dir\/(.*)/){
				$user = $1;
			}
			my $profile_filename = "$s/profile.txt";
			open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
			while ( $line = <$p>){
				if($copyNextLine ne ""){
					$line =~ s/^\s+//;
					$line =~ s/\s+$//;
					$usernames{$user}=$line;
					$copyNextLine = "";
				}
				if($line =~ /^password:$/){
					$copyNextLine = "found";
				}
			}
			
		close $p;
		}
		
		if($usernames{$username} eq $password){
			browse_screen();
		}else{
			print "<script>alert('Incorrect Username and Password!')</script>";
			print login();
		}
	
			#$correct_password = <F>;	
			#chomp $correct_password;
			#if ($password eq $correct_password) {
			#	print "You are authenticated.\n";
			#} else {
			#	print "Incorrect password!\n";
			#}
		#}
		#browse_screen();
	}
		print end_form,"\n";	# delete later ?
}elsif(defined param('Next Set')) {
	$n = param('n') || 0;
	if($n < $#students+1-10){ 
		param('n',$n+10);	
	}
	browse_screen();
}elsif(defined param('Previous Set')) {
	my $n = param('n') || 0;
	$n = $n-10;
	$n = min(max($n, 0), $#students);
	param('n',$n);
	browse_screen();
}elsif(defined param('Log Out')) {
	print login();
}elsif(defined param('1')) {
	my $n = param('n') || 0;
	param('n',$n+0);
	print profile_page();
}elsif(defined param('2')) {
	my $n = param('n') || 0;
	param('n',$n+1);
	print profile_page();
}elsif(defined param('3')) {
	my $n = param('n') || 0;
	param('n',$n+2);
	print profile_page();
}elsif(defined param('4')) {
	my $n = param('n') || 0;
	param('n',$n+3);
	print profile_page();
}elsif(defined param('5')) {
	my $n = param('n') || 0;
	param('n',$n+4);
	print profile_page();
}elsif(defined param('6')) {
	my $n = param('n') || 0;
	param('n',$n+5);
	print profile_page();
}elsif(defined param('7')) {
	my $n = param('n') || 0;
	param('n',$n+6);
	print profile_page();
}elsif(defined param('8')) {
	my $n = param('n') || 0;
	param('n',$n+7);
	print profile_page();
}elsif(defined param('9')) {
	my $n = param('n') || 0;
	param('n',$n+8);
	print profile_page();
}elsif(defined param('10')) {
	my $n = param('n') || 0;
	param('n',$n+9);
	print profile_page();
}elsif(defined param('Back')) {
	#my $n = param('n') || 0;
	print browse_screen();
}elsif(defined param('Next')) {
	my $n = param('n') || 0;
	param('n',$n+1);
	print profile_page();
}elsif(defined param('Previous')) {
	my $n = param('n') || 0;
	param('n',$n-1);
	print profile_page();
}else{
	print login();
}
print page_trailer();
exit 0;	

sub browse_screen {
	$copyNextLine = "";
	my $n = param('n') || 0;
	print h1($n),"\n";
	$n = min(max($n, 0), $#students);
	$maxNumbertoShow = 10;
	if($n > $#students+1-10){
		#$maxNumbertoShow = ($#students+1)%10;
		$maxNumbertoShow = ($#students+1)-$n;	# make sure the following method won't have out of bound
	}
	for(my $i=0; $i<$maxNumbertoShow; $i++){
		$briefProfile = "";
		%briefDescription = ();
		#$n = min(max($n, 0), $#students);
		my $student_to_show  = $students[$n+$i];
		my $profile_filename = "$student_to_show/profile.txt";
		open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
		while ( $line = <$p>){
			if($copyNextLine ne ""){
				$briefDescription{$copyNextLine}=$line;
				$copyNextLine = "";
			}
			if($line =~ /^(gender|height|hair_colour|weight|birthdate):$/){
				$copyNextLine = $1;
				$briefDescription{$1}="";
			}
		}
		foreach $l (sort keys %briefDescription){
			$briefDescription{$l} =~ s/\s*//;
			$briefProfile .= "$l - $briefDescription{$l}";
		}
		push @descriptions,$briefProfile; 
		push @images,"$student_to_show/profile.jpg";
		close $p;
	}
	print p;
	print start_form, "\n";
	for(my $i=0; $i <$maxNumbertoShow; $i++) {
	print img({ 
		src => "$images[$i]",
		style => "width:250px;height:240px"
		}), "\n";
		print	pre(""),"\n";
		print pre($descriptions[$i]),"\n";
		#print a({href="$SCRIPT_NAME"},"More Detail.."),"/n";
		$buttonName = $i+1;
		print submit("$buttonName","$buttonName"),"\n";
	}
	print hidden('n'),"\n";
	print submit('Previous Set'),"\n";
	print submit('Next Set'),"\n";
	print submit('Log Out'),"\n";
	print end_form, "\n";
}

sub profile_page {
	my $n = param('n') || 0;
	#my @students = glob("$students_dir/*");
	$n = min(max($n, 0), $#students);
	param('n',$n);
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
		hidden('n'),"\n",
		submit('Back'),"\n",
		submit('Previous'),"\n",
		submit('Next'),"\n",
		img({ 
			src => "$student_to_show/profile.jpg"
			}), "\n\n",
		end_form, "\n",
		p, "\n";
}
sub login{
	return p,
	start_form,"\n",
 	'Username: ', textfield('username'),
	p,
	'Password: ', password_field('password'),
	p,
 	submit('Log In'),
	end_form;
}

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