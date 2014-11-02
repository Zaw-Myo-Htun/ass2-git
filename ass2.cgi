#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Date::Calc qw(Delta_Days Decode_Date_US Today); 
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

$students_dir = "./students2";
my @students = glob("$students_dir/*");


if(defined param('Log In')) {
	$username = param('username');
	$password = param('password');
	param('username',$username);
	if($username eq "" || $password eq ""){
		 print "<script>alert('Please enter Username and Password')</script>";
		 print login();
	}else{
		$copyNextLine = "";
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
					$usernames{$user}=$line;    # $line = password
					$copyNextLine = "";
				}
				if($line =~ /^password:$/){
					$copyNextLine = "found";
				}
			}
		close $p;
		}
		if($usernames{$username} eq $password){
			browse_screen($username);
		}else{
			print "<script>alert('Incorrect Username and Password!')</script>";
			print login();
		}
	}
}elsif(defined param('Next Set')){
	$username = param('username');
	param('username',$username);
	$n = param('n') || 0;
	if($n < $#students+1-10){ 
		param('n',$n+10);	
	}
	browse_screen($username);
}elsif(defined param('Previous Set')) {
	$username = param('username');
	param('username',$username);
	my $n = param('n') || 0;
	$n = $n-10;
	$n = min(max($n, 0), $#students);
	param('n',$n);
	browse_screen($username);
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
	$username = param('username');
	param('username',$username);
	my $n = param('n') || 0;
	param('n',$n-($n%10));
	browse_screen($username);
}elsif(defined param('Next')) {
	my $n = param('n') || 0;
	param('n',$n+1);
	print profile_page();
}elsif(defined param('Previous')) {
	my $n = param('n') || 0;
	param('n',$n-1);
	print profile_page();
}elsif(defined param('search')) {
	$searchString = param('search');
	search_page($searchString);
}else{
	#browse_screen(); 
	print login();
}
print page_trailer();
exit 0;	

sub browse_screen {
	$copyNextLine = "";
	my @sortedStudents = ();
	my @indexs = match_gender(@_);
	foreach $index(@indexs){
		push @sortedStudents, $students[$index]; 
	}
	my $n = param('n') || 0;
	$n = min(max($n, 0), $#sortedStudents);
	$maxNumbertoShow = 10;
	if($n > $#sortedStudents+1-10){
		$maxNumbertoShow = ($#sortedStudents+1)-$n;	# make sure the following method won't have out of bound
	}
	for(my $i=0; $i<$maxNumbertoShow; $i++){
		$briefProfile = "";
		%briefDescription = ();
		my $student_to_show  = $sortedStudents[$n+$i];
		my $profile_filename = "$student_to_show/profile.txt";
		open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
		while ( $line = <$p>){
			if($copyNextLine ne ""){
				$briefDescription{$copyNextLine}=$line;
				$copyNextLine = "";
			}
			if($line =~ /^(gender|height|hair_colour|weight|birthdate|username):$/){
				$copyNextLine = $1;
				$briefDescription{$1}="";
			}
		}
		foreach $l (sort keys %briefDescription){
			if($l eq "birthdate"){
				my @yearMD = split('\/',$briefDescription{$l});
				if($yearMD[0] =~ /\d{4}/){
					my $birthdate = $yearMD[1] . "/" . $yearMD[2] . "/" . $yearMD[0];
					$briefProfile .= "age - " . get_age($birthdate) . "\n";
				}else{
					my $birthdate = $yearMD[1] . "/" . $yearMD[0] . "/" . $yearMD[2];
					$briefProfile .= "age - " . get_age($birthdate) . "\n";
				}
			}else{
				$briefDescription{$l} =~ s/\s*//;
				$briefProfile .= "$l - $briefDescription{$l}";
			}
		}
		push @descriptions,$briefProfile; 
		push @images,"$student_to_show/profile.jpg";
		close $p;
	}
	print start_form;
	
	print 'Search:  ', textfield('search');
	
	print submit('Search');
	print div({-class=>'clear'});
	for(my $i=0; $i <$maxNumbertoShow; $i++) {
		$buttonName = $i+1;
		print div({-class=>'div'},
		 img({ 
			src => "$images[$i]",
			style => "width:150px;height:200px"
			}), 
		 	pre($descriptions[$i]),
		 submit("$buttonName","More Detail"),
		 );
	} 
	print hidden('n'),"\n";
	print hidden('username'),"\n";
	print div({-class=>'clear'},
	 submit('Previous Set'),
	 submit('Next Set'),
	 submit('Log Out'),
	 );
	print end_form,"\n";
}

sub search_page{

	foreach $s (@students){
		$briefProfile = "";
		%briefDescription = ();
			if($s =~ /$students_dir\/(.*)/){
				if($1 =~ /@_/i){
					my $profile_filename = "$s/profile.txt";
					open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
					while ( $line = <$p>){
						if($copyNextLine ne ""){
							$briefDescription{$copyNextLine}=$line;
							$copyNextLine = "";
						}
						if($line =~ /^(gender|height|hair_colour|weight|birthdate|username):$/){
							$copyNextLine = $1;
							$briefDescription{$1}="";
						}
					}
					foreach $l (sort keys %briefDescription){
						if($l eq "birthdate"){
							my @yearMD = split('\/',$briefDescription{$l});
							if($yearMD[0] =~ /\d{4}/){
								my $birthdate = $yearMD[1] . "/" . $yearMD[2] . "/" . $yearMD[0];
								$briefProfile .= "age - " . get_age($birthdate) . "\n";
							}else{
								my $birthdate = $yearMD[1] . "/" . $yearMD[0] . "/" . $yearMD[2];
								$briefProfile .= "age - " . get_age($birthdate) . "\n";
							}
						}else{
							$briefDescription{$l} =~ s/\s*//;
							$briefProfile .= "$l - $briefDescription{$l}";
						}
					}
					push @descriptions,$briefProfile; 
					push @images,"$s/profile.jpg";
					close $p;
				}
			}
	}
	$size = $#descriptions+1;
	if($size == 0){
		print start_form;
		print 'Search:  ', textfield('search');
		print submit('Search');
		print h3('Sorry, No Record is found!');
	}else{
		print start_form;
		print 'Search:  ', textfield('search');
		print submit('Search');
		for(my $i=0; $i <$size; $i++) {
		$buttonName = $i+1;
		print div({-class=>'div'},
		 	img({ 
			src => "$images[$i]",
			style => "width:150px;height:200px"
			}), 
		 	pre($descriptions[$i]),
		 	submit("$buttonName","More Detail"),
		);
	}
	print hidden('n'),"\n";
	print div({-class=>'clear'},
	 submit('Back'),
	 );
	print end_form,"\n";
	}
}

sub profile_page {
	$username = param('username');
	param('username',$username);

	my @sortedStudents = ();
	my @indexs = match_gender($username);
	foreach $index(@indexs){
		push @sortedStudents, $students[$index]; 
	}
	my $n = param('n') || 0;
	$n = min(max($n, 0), $#sortedStudents);
	param('n',$n);
	my $student_to_show  = $sortedStudents[$n];
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
		img({ 
			src => "$student_to_show/profile.jpg"
			}), "\n\n",
		pre($profile),"\n",
		hidden('n'),"\n",
		hidden('username'),"\n",
		submit('Back'),"\n",
		submit('Previous'),"\n",
		submit('Next'),"\n",
		end_form, "\n";
}

sub login{
	return p,
		start_form,"\n",
 		'Username: ', textfield('username'),
		p,
		'Password:  ', password_field('password'),
		p,
 		submit('Log In'),
		h1({"-font-size"=>"2em"},'Welcome to Love2041!'),
		end_form;
}


sub get_age { 
    my $bday = shift; 
    my $age_in_days = Delta_Days( 
        Decode_Date_US($bday), 
        Today() 
    ); 
    return int $age_in_days/365.4 
}



sub match_gender {
	my $user = "@_";
	my @indexs = match_age($user);
	my @sortedIndex = ();
	my @prefIndex = ();
	my @notPrefIndex = ();
	my $prefGender = "";
	
	my $preferences_filename = "$students_dir/$user/preferences.txt";
	open my $p, "$preferences_filename" or die "can not open $preferences_filename: $!";			
	while($line = <$p>){
		if($copyNextLine ne ""){
			if($line =~ /:$/){
				$copyNextLine = "";
			}else{
				$prefGender = $line;
			}
		}
		if($line =~ /^gender:$/){
			$copyNextLine = "ok";
		}
	}
	if($prefGender eq ""){
		my $profile_filename = "$students_dir/$user/profile.txt";
		open $p, "$profile_filename" or die "can not open $profile_filename: $!";
		while($line = <$p>){
			if($copyNextLine ne ""){
				$userGender = $line;
				$copyNextLine = "";
			}
			if($line =~ /^(gender):$/){
				$copyNextLine = $1;
			}
		}
		if($userGender == "male"){
			 $prefGender = "female";
		}else{
			 $prefGender = "male";
		}
	}
	for($i = 0 ;$i < $#indexs+1;$i++){
		my $gender = "";
		my $student_to_show  = $students[$indexs[$i]];
		my $profile_filename = "$student_to_show/profile.txt";
		open $p, "$profile_filename" or die "can not open $profile_filename: $!";
		while($line = <$p>){
			if($copyNextLine ne ""){
				$gender = $line;
				$copyNextLine = "";
			}
			if($line =~ /^(gender):$/){
				$copyNextLine = $1;
			}
		}
		if($gender eq $prefGender){
			push @prefIndex, $indexs[$i];
		}else{
			push @notPrefIndex, $indexs[$i];
		}
	}
	push @sortedIndex,@prefIndex;
	push @sortedIndex,@notPrefIndex;
	
	return @sortedIndex;
}


sub match_age{
	my $user = "@_";
	my @indexs = match_height($user);
	my $copyMinMax = "";
	my @sortedIndex = ();
	my @prefIndex = ();
	my @minMaxAge = ();
	my @notPrefIndex = ();
	my $copyMinMax = "";
	my $preferences_filename = "$students_dir/$user/preferences.txt";
	open my $p, "$preferences_filename" or die "can not open $preferences_filename: $!";
	while ($line = <$p>){
		if($copyNextLine ne ""){
			if($copyMinMax ne ""){
				if($line =~ /:$/){
					$copyMinMax = "";
				}else{
					push @minMaxAge, $line;
				}
			}
			if($line =~ /(min|max):$/){
				$copyMinMax = "ok";
			}
			if($line =~ /^\w+:$/){
				$copyNextLine = "";
			}
		}
		if($line =~ /^age:$/){
			$copyNextLine = "ok";
		}
	}
	
	@sortedMinMaxAge = sort { $a <=> $b } @minMaxAge;
	if(not @sortedMinMaxAge){
		my $profile_filename = "$students_dir/$user/profile.txt";
		open $p, "$profile_filename" or die "can not open $profile_filename: $!";
		while($line = <$p>){
			if($copyNextLine ne ""){
				$birthdate = $line;
				my @yearMD = split('\/',$birthdate);
				if($yearMD[0] =~ /\d{4}/){
					my $birthdate = $yearMD[1] . "/" . $yearMD[2] . "/" . $yearMD[0];
					$userAge = get_age($birthdate);
				}else{
					my $birthdate = $yearMD[1] . "/" . $yearMD[0] . "/" . $yearMD[2];
					$userAge = get_age($birthdate);
				}
				$copyNextLine = "";
			}
			if($line =~ /^(birthdate):$/){
				$copyNextLine = $1;
			}
		}
		push @sortedMinMaxAge, ($userAge-4);
		push @sortedMinMaxAge, ($userAge+4);
	}
		for($i = 0 ;$i < $#indexs+1;$i++){
			my $isMatch = 0;
			my $age = 0;
			my $student_to_show  = $students[$indexs[$i]];
			my $profile_filename = "$student_to_show/profile.txt";
			open $p, "$profile_filename" or die "can not open $profile_filename: $!";
			while($line = <$p>){
				if($copyNextLine ne ""){
					$birthdate = $line;
					my @yearMD = split('\/',$birthdate);
					if($yearMD[0] =~ /\d{4}/){
						my $birthdate = $yearMD[1] . "/" . $yearMD[2] . "/" . $yearMD[0];
						$age = get_age($birthdate);
					}else{
						my $birthdate = $yearMD[1] . "/" . $yearMD[0] . "/" . $yearMD[2];
						$age = get_age($birthdate);
					}
					$copyNextLine = "";
				}
				if($line =~ /^(birthdate):$/){
					$copyNextLine = $1;
				}
			}
			if($age>=$sortedMinMaxAge[0] && $age<=$sortedMinMaxAge[1]){
				
				push @prefIndex, $indexs[$i];
			}else{
				push @notPrefIndex, $indexs[$i];
			}
		}
	push @sortedIndex,@prefIndex;
	push @sortedIndex,@notPrefIndex;
	return @sortedIndex;
}


sub match_height{
	my $user = "@_";
	my @indexs = match_weight($user);
	my $copyMinMax = "";
	my @sortedIndex = ();
	my @prefIndex = ();
	my @minMaxHeight = ();
	my @notPrefIndex = ();
	my $copyMinMax = "";
	my $preferences_filename = "$students_dir/$user/preferences.txt";
	open my $p, "$preferences_filename" or die "can not open $preferences_filename: $!";
	while ($line = <$p>){
		if($copyNextLine ne ""){
			if($copyMinMax ne ""){
				if($line =~ /:$/){
					$copyMinMax = "";
				}else{
					$line =~ s/m$//;
					push @minMaxHeight, $line;
				}
			}
			if($line =~ /(min|max):$/){
				$copyMinMax = "ok";
			}
			if($line =~ /^\w+:$/){
				$copyNextLine = "";
			}
		}
		if($line =~ /^height:$/){
			$copyNextLine = "ok";
		}
	}
	
	@sortedMinMaxHeight = sort { $a <=> $b } @minMaxHeight;
	if(not @sortedMinMaxHeight){
		my $profile_filename = "$students_dir/$user/profile.txt";
		open $p, "$profile_filename" or die "can not open $profile_filename: $!";
		while($line = <$p>){
			if($copyNextLine ne ""){
				$line =~ s/m$//;
				$height = $line;
				$copyNextLine = "";
			}
			if($line =~ /^(height):$/){
				$copyNextLine = $1;
			}
		}
		push @sortedMinMaxHeight, ($height-0.1);
		push @sortedMinMaxHeight, ($height+0.1);
	}
		for($i = 0 ;$i < $#indexs+1;$i++){
			my $isMatch = 0;
			my $height = 0;
			my $student_to_show  = $students[$indexs[$i]];
			my $profile_filename = "$student_to_show/profile.txt";
			open $p, "$profile_filename" or die "can not open $profile_filename: $!";
			while($line = <$p>){
				if($copyNextLine ne ""){
					$line =~ s/m$//;
					$height = $line;
					$copyNextLine = "";
				}
				if($line =~ /^(height):$/){
					$copyNextLine = $1;
				}
			}
			if($height>=$sortedMinMaxHeight[0] && $height<=$sortedMinMaxHeight[1]){
				push @prefIndex, $indexs[$i];
			}else{
				push @notPrefIndex, $indexs[$i];
			}
		}
	push @sortedIndex,@prefIndex;
	push @sortedIndex,@notPrefIndex;
	return @sortedIndex;
}


sub match_weight{
	my $user = "@_";
	my @indexs = match_hair_colour($user);
	my $copyMinMax = "";
	my @sortedIndex = ();
	my @prefIndex = ();
	my @minMaxWeight = ();
	my @notPrefIndex = ();
	my $copyMinMax = "";
	my $preferences_filename = "$students_dir/$user/preferences.txt";
	open my $p, "$preferences_filename" or die "can not open $preferences_filename: $!";
	while ($line = <$p>){
		if($copyNextLine ne ""){
			#if($line =~ /^[^(min|max)]:$/){
			#	$copyNextLine = "";
			#}else{
			#	if($line =~ /[^(min|max)]:$/){
			#		$line =~ s/kg$//;
			#		push @minMaxWeight, $line;
			#	}
			#}
			
			if($copyMinMax ne ""){
				if($line =~ /:$/){
					$copyMinMax = "";
				}else{
					$line =~ s/kg$//;
					push @minMaxWeight, $line;
				}
			}
			if($line =~ /(min|max):$/){
				$copyMinMax = "ok";
			}
			if($line =~ /^\w+:$/){
				$copyNextLine = "";
			}
		}
		if($line =~ /^weight:$/){
			$copyNextLine = "ok";
		}
	}
	
	@sortedMinMaxWeight = sort { $a <=> $b } @minMaxWeight;
	if(@sortedMinMaxWeight){
		for($i = 0 ;$i < $#indexs+1;$i++){
			my $isMatch = 0;
			my $weight = 0;
			my $student_to_show  = $students[$indexs[$i]];
			my $profile_filename = "$student_to_show/profile.txt";
			open $p, "$profile_filename" or die "can not open $profile_filename: $!";
			while($line = <$p>){
				if($copyNextLine ne ""){
					$line =~ s/kg$//;
					$weight = $line;
					$copyNextLine = "";
				
				}
				if($line =~ /^(weight):$/){
					$copyNextLine = $1;
				}
			}
			if($weight>=$sortedMinMaxWeight[0] && $weight<=$sortedMinMaxWeight[1]){
				push @prefIndex, $indexs[$i];
			}else{
				push @notPrefIndex, $indexs[$i];
			}
		}
		push @sortedIndex,@prefIndex;
		push @sortedIndex,@notPrefIndex;
	}else{
		push @sortedIndex,@indexs;
	}
	return @sortedIndex;
}

sub match_hair_colour {
	my @sortedIndex = ();
	my @prefIndex = ();
	my @notPrefIndex = ();
	my @hairColours = ();
	my $user = "@_";
	my $preferences_filename = "$students_dir/$user/preferences.txt";
	open my $p, "$preferences_filename" or die "can not open $preferences_filename: $!";			
	while($line = <$p>){
		if($copyNextLine ne ""){
			if($line =~ /:$/){
				$copyNextLine = "";
			}else{
				push @hairColours, $line;
			}
		}
		if($line =~ /^hair_colours:$/){
			$copyNextLine = "ok";
		}
	}
	
	for($i = 0 ;$i < $#students+1;$i++){
		my $isMatch = 0;
		my $hair_colour = "";
		my $student_to_show  = $students[$i];
		my $profile_filename = "$student_to_show/profile.txt";
		open $p, "$profile_filename" or die "can not open $profile_filename: $!";
		while($line = <$p>){
			if($copyNextLine ne ""){
				$hair_colour = $line;
				$copyNextLine = "";
			}
			if($line =~ /^(hair_colour):$/){
				$copyNextLine = $1;
			}
		}
		foreach $colour(@hairColours){
			if($colour eq $hair_colour){
				$isMatch = 1;
				push @prefIndex, $i;
			}
		}
		if($isMatch == 0){
			push @notPrefIndex, $i;
		}
	}
	push @sortedIndex,@prefIndex;
	push @sortedIndex,@notPrefIndex;
	return @sortedIndex;
}

sub page_header {
	return header,
   		start_html("-title"=>"LOVE2041",-style=>{-src=>['homepage.css']}),
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
