#!/usr/bin/perl -w

# RRDWeather
# Released under the GNU General Public License
# http://www.wains.be/projects/rrdweather/

use CGI ();
#use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use POSIX qw(strftime);
use RRDs;
use XML::Simple;

my $VERSION = "0.43";

############################################################
############## EDIT THESE VALUES BELOW #####################
############################################################

my $xpoints = 350;			 # Graphs width
my $ypoints = 150;			 # Graphs height
my $db_dir = '/var/lib/rrdweather/db'; 	 # DB files directory
my $tmp_dir = '/var/tmp/rrdweather';	 # Images directory
my $system = 'm';		 # m : metric units / e : english units
my $scriptname = 'weather.cgi'; # if you want to rename the script

############################################################
### YOU SHOULD NOT HAVE TO EDIT ANYTHING BELOW THIS LINE ###
############################################################

# Fetching ZIP code passed as argument
my $cgi = CGI->new();
my $zip = $cgi->param("zip");
my $uri = $ENV{SCRIPT_URI};

if ( ! $zip ) {
	print "Content-Type: text/html\n\n";
	print "<pre>RRDWeather $VERSION\n---------------\n\n";	
	print "Please specify a city to display.\n\n";
	print "Example : $uri?zip=12345";
	exit 1;
}

# Fetching city name from XML file
my $xml = new XML::Simple;
my $xmlfile = "$tmp_dir/$zip.xml";

# If XML is not available, wait 3 seconds and try again
# If still not available, display the error message which will try to reload the page after 5 seconds
if ( ! -r $xmlfile) { 
	sleep 3;
	if ( ! -r $xmlfile) {
		print "Content-Type: text/html\n\n";
		print "<head>";
		print "<meta http-equiv=\"pragma\" content=\"no-cache\"/>";
		print "<meta http-equiv=\"refresh\" content=\"5\"/>";
		print "<meta http-equiv=\"content-type\" content=\"text/html; charset=ISO-8859-1\"/>";
		print "</head>";
		print "<pre>RRDWeather $VERSION\n---------------\n\n";	
		print "XML source cannot be read !\n\n";	
		print "Make sure you are trying to display a city monitored by RRDWeather.\n\n";
		print "The XML source may temporarily be unavailable. The page will reload within 5 seconds.\n\n";
		print "If the problem persists, there's a problem with this configuration.";
		exit 1;
	}
}

my $xmldata = $xml->XMLin("$xmlfile");
my $city = $xmldata->{loc}->{dnam};

# Variables
my $date = strftime "%a %b %e %Y %I.%M%p", localtime;
my $points_per_sample = 3;
my $ypoints_err = 96;
my $db_real = "$db_dir/$zip/real.rrd";
my $db_dew = "$db_dir/$zip/dew.rrd";
my $db_felt = "$db_dir/$zip/felt.rrd";
my $db_humidity = "$db_dir/$zip/humidity.rrd";
my $db_wind = "$db_dir/$zip/wind.rrd";
my $db_pressure = "$db_dir/$zip/pressure.rrd";
my $db_uv = "$db_dir/$zip/uv.rrd";

if($system eq "m") {
	$speed = 'kph';		
	$pressurelowlimit = '980';	
	$pressureuplimit = '1100';
}
elsif($system eq "e") {
	$speed = 'mph';
	$pressurelowlimit = '20';	
	$pressureuplimit = '40';
}

my @graphs = (
	{ title => 'Daily Graphs',   seconds => 3600*24,        },
	{ title => 'Weekly Graphs',  seconds => 3600*24*7,      },
	{ title => 'Monthly Graphs', seconds => 3600*24*31,     },
	{ title => 'Yearly Graphs',  seconds => 3600*24*365, 	},
);

sub graph_temperature($$$)
{
	my $range = shift;
	my $file = shift;
	my $title = shift;
	my $step = $range*$points_per_sample/$xpoints;
	
	my ($graphret,$xs,$ys) = RRDs::graph($file,
		'--imgformat', 'PNG',
		'--width', $xpoints,
		'--height', $ypoints,
		'--start', "-$range",
		"--title= Real & felt temp. in $city",
		'--vertical-label', 'Real & felt temp.',
		'--units-exponent', 0,
		'--lazy',
		'-Y',
		
		"DEF:real_c=$db_real:real:AVERAGE",
		"DEF:felt_c=$db_felt:felt:AVERAGE",
		"DEF:dew_c=$db_dew:dew:AVERAGE",
		"COMMENT:           Min       Max       Ave       Last\\n",
		'LINE2:real_c#DD3F4A:Real', 'GPRINT:real_c:MIN: %5.2lf C',
		'GPRINT:real_c:MAX: %5.2lf C', 'GPRINT:real_c:AVERAGE: %5.2lf C',
		'GPRINT:real_c:LAST: %5.2lf C\\n',
		'LINE1:felt_c#3F4ADD:Felt', , 'GPRINT:felt_c:MIN: %5.2lf C',
		'GPRINT:felt_c:MAX: %5.2lf C', 'GPRINT:felt_c:AVERAGE: %5.2lf C',
		'GPRINT:felt_c:LAST: %5.2lf C\\n',	
		'LINE1:dew_c#4ADD3F:Dew ', , 'GPRINT:dew_c:MIN: %5.2lf C',
		'GPRINT:dew_c:MAX: %5.2lf C', 'GPRINT:dew_c:AVERAGE: %5.2lf C',
		'GPRINT:dew_c:LAST: %5.2lf C\\n',
		"COMMENT: \\n",
		"COMMENT:RRDWeather $VERSION - $date",
	);

	my $ERR=RRDs::error;
	die "ERROR : $ERR\n" if $ERR;
}

sub graph_humidity($$$)
{
        my $range = shift;
        my $file = shift;
        my $title = shift;
        my $step = $range*$points_per_sample/$xpoints;

        my ($graphret,$xs,$ys) = RRDs::graph($file,
                '--imgformat', 'PNG',
                '--width', $xpoints,
                '--height', $ypoints,
                '--start', "-$range",
		"--title= Humidity in $city",
                '--vertical-label', 'Humidity',
                '--lower-limit', 0,
		'--upper-limit', 100,
                '--units-exponent', 0,
		'--lazy',
		'-Y',

                "DEF:humidity_pc=$db_humidity:humidity:AVERAGE",
                'COMMENT:        ', "COMMENT:     Min        Max        Ave        Last\\n",
                'LINE1:humidity_pc#4DD34A:Humidity', 'GPRINT:humidity_pc:MIN: %5.2lf pc',
                'GPRINT:humidity_pc:MAX: %5.2lf pc', 'GPRINT:humidity_pc:AVERAGE: %5.2lf pc',
                'GPRINT:humidity_pc:LAST: %5.2lf pc\\n',
		"COMMENT: \\n",
		"COMMENT: \\n",
		"COMMENT: \\n",
		"COMMENT:RRDWeather $VERSION - $date",
	);

        my $ERR=RRDs::error;
        die "ERROR : $ERR\n" if $ERR;
}

sub graph_wind($$$)
{
        my $range = shift;
        my $file = shift;
        my $title = shift;
        my $step = $range*$points_per_sample/$xpoints;

        my ($graphret,$xs,$ys) = RRDs::graph($file,
                '--imgformat', 'PNG',
                '--width', $xpoints,
                '--height', $ypoints,
                '--start', "-$range",
                "--title= Wind in $city",
                '--vertical-label', 'Wind',
                '--units-exponent', 0,
		'--lazy',
                '-Y',

                "DEF:wind_s=$db_wind:wind:AVERAGE",
                "COMMENT:            Min        Max         Ave         Last\\n",
                'LINE2:wind_s#DD3F4A:Wind', "GPRINT:wind_s:MIN: %5.2lf $speed",
                "GPRINT:wind_s:MAX: %5.2lf $speed", "GPRINT:wind_s:AVERAGE: %5.2lf $speed",
                "GPRINT:wind_s:LAST: %5.2lf $speed\\n",
		"COMMENT: \\n",
		"COMMENT:RRDWeather $VERSION - $date",
        );

        my $ERR=RRDs::error;
        die "ERROR : $ERR\n" if $ERR;
}

sub graph_pressure($$$)
{
        my $range = shift;
        my $file = shift;
        my $title = shift;
        my $step = $range*$points_per_sample/$xpoints;

        my ($graphret,$xs,$ys) = RRDs::graph($file,
                '--imgformat', 'PNG',
                '--width', $xpoints,
                '--height', $ypoints,
                '--start', "-$range",
                "--title= Pressure in $city",
                '--vertical-label', 'Pressure',
                '--lower-limit', $pressurelowlimit,
                '--upper-limit', $pressureuplimit,
		'--units-exponent', 0,
		'--lazy',
		'-Y',

        	"DEF:pressure_hpa=$db_pressure:pressure:AVERAGE",
                'COMMENT:        ', "COMMENT:        Min           Max           Last\\n",
                'LINE1:pressure_hpa#DD3F4A:Pressure', 'GPRINT:pressure_hpa:MIN: %5.2lf hPa',
                'GPRINT:pressure_hpa:MAX: %5.2lf hPa', 
                'GPRINT:pressure_hpa:LAST: %5.2lf hPa\\n',
		"COMMENT: \\n",
		"COMMENT:RRDWeather $VERSION - $date",
	);

        my $ERR=RRDs::error;
        die "ERROR : $ERR\n" if $ERR;
}

sub graph_uv($$$)
{
        my $range = shift;
        my $file = shift;
        my $title = shift;
        my $step = $range*$points_per_sample/$xpoints;

        my ($graphret,$xs,$ys) = RRDs::graph($file,
                '--imgformat', 'PNG',
                '--width', $xpoints,
                '--height', $ypoints,
                '--start', "-$range",
                "--title= UV index in $city",
                '--vertical-label', 'UV index',
                '--lower-limit', 0,
	        '--upper-limit', 10,        
		'--units-exponent', 0,
		'--lazy',
		'-y', '1:5',		

                "DEF:uv_index=$db_uv:uv:AVERAGE",
                'COMMENT:        ', "COMMENT:     Min     Max     Ave    Last\\n",
                'AREA:uv_index#DD3F4A:UV index', 'GPRINT:uv_index:MIN: %5.2lf',
                'GPRINT:uv_index:MAX: %5.2lf', 'GPRINT:uv_index:AVERAGE: %5.2lf',
		'GPRINT:uv_index:LAST: %5.2lf\\n',
		"COMMENT: \\n",
		"COMMENT:RRDWeather $VERSION - $date",
	);

        my $ERR=RRDs::error;
        die "ERROR : $ERR\n" if $ERR;
}

sub print_html()
{
	print "Content-Type: application/xhtml+xml\n\n";

	print <<HEADER;
<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Weather in $city - Generated by RRDWeather</title>
<meta http-equiv="pragma" content="no-cache"/>
<meta http-equiv="refresh" content="600"/>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=ISO-8859-1"/>
<style type="text/css">

body
{
	background-color: #ABABAB; 
	color: #737367;	
	font-size: 11px;
	margin: 0px;
	padding: 0px;
	text-align: center;
	font-family: arial, helvetica, sans-serif;
}

a 
{
	text-decoration: none;
	color: #464646; 
	background-color: transparent; 
}

a:visited 
{ 
	color: #59594F; 
	background-color: transparent; 
}

a:hover 
{ 
	color: #FF6633; 
	background-color: transparent; 
}

a:active 
{ 
	color: #444444; 
}

table 
{ 
	margin-left: auto; 
	margin-right: auto; 
	text-align: center; 
}

img 
{ 
	border: 0; 
}

.graphtitle
{
	background-color: #DDDDDD; 
	color: #444444; 
	width: 900px;
	margin: 0 auto;
}

.page_header 
{
	margin-top: 0px;
	padding-top: 25px;
}

.page_footer 
{
	margin-bottom: 10px;
	padding-top: 0px;
}

</style>
</head>
<body>
HEADER
	print "<h1 class=\"page_header\">Weather in $city</h1>\n";
	print "<h4>According to weather.com</h4>\n";
	for my $n (0..$#graphs) {
		print "<table>\n";
		print "<tr>\n";
		print "<td colspan=\"2\">\n";
		my $h2_id = $graphs[$n]{title};
		my $next_h2_id = $graphs[$n+1]{title};
		$h2_id =~ s/ /_/;
		$next_h2_id =~ s/ /_/;
		print "<div class=\"graphtitle\"><h2 id=\"". $h2_id ."\"><a href=\"#". $h2_id ."\">".$graphs[$n]{title}."</a></h2></div>\n";
		print "</td>\n";
		print "</tr>\n";
		print "<tr>\n";
		print "<td><a href=\"#". $next_h2_id . "\"><img src=\"$scriptname?zip=$zip&amp;file=$n-temperature\" alt=\"Temperature\" /></a></td>\n";
		print "<td><a href=\"#". $next_h2_id . "\"><img src=\"$scriptname?zip=$zip&amp;file=$n-humidity\" alt=\"Humidity\" /></a></td>\n";
		print "</tr>\n";
		print "<tr>\n";
		print "<td><a href=\"#". $next_h2_id . "\"><img src=\"$scriptname?zip=$zip&amp;file=$n-wind\" alt=\"Wind\" /></a></td>\n";
		print "<td><a href=\"#". $next_h2_id . "\"><img src=\"$scriptname?zip=$zip&amp;file=$n-pressure\" alt=\"Pressure\" /></a></td>\n";
		print "</tr>\n";
		print "<tr>\n";
		print "<td colspan=\"2\"><a href=\"#". $next_h2_id . "\"><img src=\"$scriptname?zip=$zip&amp;file=$n-uv\" alt=\"UV index\" /></a></td>\n";
		print "</tr>\n";
		print "</table>\n";
	}

	print <<FOOTER;
<p>
    <a href="http://validator.w3.org/check?uri=referer"><img
        src="http://www.w3.org/Icons/valid-xhtml11"
        alt="Valid XHTML 1.1" height="31" width="88" /></a>
</p>
<table class=\"page_footer\" border="0" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center"><a href="http://www.wains.be/projects/rrdweather/" onclick="window.open(this.href); return false;">RRDWeather</a> $VERSION by <a href="http://www.wains.be/" onclick="window.open(this.href); return false;">Sebastien Wains</a></td></tr></table>\n</body>\n</html>\n
FOOTER
}

sub send_image($)
{
	my $file = shift;
	-r $file or do {
		print "Content-type: text/plain\n\nERROR : can't find $file\n";
		exit 1;
	};

	print "Content-type: image/png\n";
	print "Content-length: ".((stat($file))[7])."\n";
	print "\n";
	open(IMG, $file) or die;
	my $data;
	print $data while read IMG, $data, 1024;
}

sub main()
{
        mkdir $tmp_dir, 0777 unless -d $tmp_dir;
        mkdir "$tmp_dir/$zip", 0777 unless -d "$tmp_dir/$zip";

        my $img = $ENV{QUERY_STRING};
        if(defined $img and $img =~ /\S/) {
                if($img =~ /^zip=([a-zA-Z0-9]{5,8})&file=(\d+)-temperature$/) {
                        my $file = "$tmp_dir/$1/RRDWeather_$2_temperature.png";
                        graph_temperature($graphs[$2]{seconds}, $file, $graphs[$2]{title});
                        send_image($file);
                }
                elsif($img =~ /^zip=([a-zA-Z0-9]{5,8})&file=(\d+)-humidity$/) {
                        my $file = "$tmp_dir/$1/RRDWeather_$2_humidity.png";
                        graph_humidity($graphs[$2]{seconds}, $file, $graphs[$2]{title});
                        send_image($file);
                }
                elsif($img =~ /^zip=([a-zA-Z0-9]{5,8})&file=(\d+)-wind$/) {
                        my $file = "$tmp_dir/$1/RRDWeather_$2_wind.png";
                        graph_wind($graphs[$2]{seconds}, $file, $graphs[$2]{title});
                        send_image($file);
                }
                elsif($img =~ /^zip=([a-zA-Z0-9]{5,8})&file=(\d+)-pressure$/) {
                        my $file = "$tmp_dir/$1/RRDWeather_$2_pressure.png";
                        graph_pressure($graphs[$2]{seconds}, $file, $graphs[$2]{title});
                        send_image($file);
                }
                elsif($img =~ /^zip=([a-zA-Z0-9]{5,8})&file=(\d+)-uv$/) {
                        my $file = "$tmp_dir/$1/RRDWeather_$2_uv.png";
                        graph_uv($graphs[$2]{seconds}, $file, $graphs[$2]{title});
                        send_image($file);
                }
                else {
                        print_html;
                }
        }
}

main;
