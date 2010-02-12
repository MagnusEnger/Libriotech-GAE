#!/usr/bin/perl -w

use File::Slurp;
use strict;

my %public;
my @public = read_file('public.txt');
for my $line (@public) {
	next if substr($line, 0, 1) eq '#';
	my ($no, $dummy) = split(/\|/, $line);
	$public{$no} = 1;
}

my %bokhylla;
my @bokhylla = read_file('bokhylla_02.txt');
for my $line (@bokhylla) {
	next if substr($line, 0, 1) eq '#';
	my ($no, $dummy) = split(/\|/, $line);
	$bokhylla{$no} = 1;
}

my @total_file = read_file('totalt.txt');
for my $line (@total_file) {
	
	next if substr($line, 0, 1) eq '#';
	
	my ($no, $urn, $oaiids, $sesamids, $isbn, $pages, $title, $creator) = split(/\|/, $line);
	
	$urn      =~ s/; /,/g;
	$oaiids   =~ s/; /,/g;
	$sesamids =~ s/; /,/g;
	$isbn     =~ s/-//g;
	$title    =~ s/\"/\"\"/g;
	$title    = substr($title, 0, 499);
	if ($creator) {
		$creator  = substr($creator, 0, 499);
		$creator  =~ s/\"/\"\"/g;
	} else {
		$creator = "";
	}
	my $ticr  = "$creator $title";
	$ticr     = substr($ticr, 0, 499);
	my $public_bool = "false";
	if ($public{$no}) { 
		$public_bool = "true";
	}
	my $bokhylla_bool = "false";
	if ($bokhylla{$no}) { 
		$bokhylla_bool = "true";
	}

	my $new_line = "\"$no\",\"$urn\",\"$oaiids\",\"$sesamids\",\"$isbn\",\"$pages\",\"$title\",\"$creator\",\"$ticr\",\"$public_bool\",\"$bokhylla_bool\"";
	$new_line =~ s/\n//g;
	
	print $new_line, "\n";
	
}